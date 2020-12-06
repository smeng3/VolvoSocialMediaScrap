#!/usr/bin/env python
# coding: utf-8

# # Webscraping Volvo's Car Review From Edmunds
# 

# ### 1. Import the required packages
# 

# In[2]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from requests import get
from urllib.request import urlopen
from bs4 import NavigableString
import re
import time
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
# from selenium import webdriver


# ### 2. Create a list that contains the desired Volvo's car models and years

# In[3]:


car_model = [
    '240',
    '740',
    '760',
    '780',
    '850',
    '940',
    '960',
    'C30',
    'C70',
    'Coupe',
    'S40',
    'S60 Cross Country',
    'S70',
    'S80',
    'V40',
    'V50',
    'V70',
    'XC',
    'XC70',
    'S60',
    'S90',
    'V60',
    'V60 Cross Country',
    'V90',
    'V90 Cross Country',
    'XC40',
    'XC60',
    'XC90',
]

car_year=['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']


# ### 3. Create empty lists to store scrapped data

# In[1]:


#Review info
Review_Title=[]
Helpful_weight = []
Customer_Rating = []
Vehicle_Name=[]
Review=[]
AuthorName=[]
Review_Date=[]

#Car Session
Vehicle_model = []
Vehicle_Year = []
Vehicle_Rating=[]


# ### 4. Loop through the models and years on Edmund's website to obtain data

# In[ ]:



for model in car_model:
    for year in car_year:
        for pages in range(1, 15):
            print(model+" - " + year + " - " + str(pages))
            try:
                #Command to request the data from 'https://www.edmunds.com/volvo/' + model + '/' + year + '/' + 'consumer-reviews/?pagenum=' + str(pages)
                #Store the content in the variable called `response`
                #Process if recieve a successful response (TTP status code = 200)
                time.sleep(1)
                url = 'https://www.edmunds.com/volvo/' + model + '/' +                     year + '/' + 'consumer-reviews/?pagenum=' + str(pages)
                response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                if response.status_code != 200:
                    break
    
                # Convert source.content to a beautifulsoup object 
                # beautifulsoup can parse (extract specific information) HTML code    
                html_soup = BeautifulSoup(response.text, "html.parser")
                
                # Find the widget that contains all the reviews
                review_widget = html_soup.find('div', attrs={'class': 'reviews-list'})                
                if len(review_widget) == 0:
                    break
                
                # individual_review_container contains all the information for each review
                individual_review_container = review_widget.find_all(class_='review-item text-gray-darker')
                
                # get vehicle_rating_overall
                vehicle_rating_overall = html_soup.find('div', attrs={'class': 'average-rating flex-first'}).find('span').text

                # loop through each individual_review_container
                # to get Vehicle_model, Vehicle_Year, Vehicle_Rating, Customer_Rating
                # and Review_Title, Helpful_weight, Vehicle_Name, Review
                for a in individual_review_container:
                    review = ''

                    Vehicle_model.append(model)
                    Vehicle_Year.append(year)
                    Vehicle_Rating.append(vehicle_rating_overall)

                    individual_overall_rating = a.find('span', attrs={'class': 'rating-stars text-primary-darker mr-0_25'})["aria-label"].split()[0]
                    Customer_Rating.append(individual_overall_rating)

                    review_title = a.find('h3').text 
                    Review_Title.append(review_title)

                    consumer_helpful_rating = a.find('div', {'class': 'xsmall mb-1_5'}).text
                    Helpful_weight.append(consumer_helpful_rating)

                    vehicle_title = a.find(class_='small text-gray mb-2').find_all('div')[1].text
                    Vehicle_Name.append(vehicle_title)


                    review_list = a.find_all('p')
                    for each in review_list:
                        review += (each.text+" ")
                    Review.append(review)

                    author_name_and_time = a.find(class_='small text-gray mb-2').find('div').text.split(",")
                    author_name = author_name_and_time[0]
                    author_date = author_name_and_time[-1]
                    AuthorName.append(author_name)
                    Review_Date.append(author_date)


            except Exception as e:
                # If the download for some reason fails (ex. 404) the script will continue downloading
                # the next article.
                print(e)
                print("continuing...")
                continue


# ### 5.Convert the lists with scrapped data into dataframe and a csv file

# In[260]:


df = pd.DataFrame(
    {'Vehicle_model' :Vehicle_model,
    'Vehicle_Year':Vehicle_Year,
    'Vehicle_Rating':Vehicle_Rating,
     'Review_Date': Review_Date,
     'Author_Name': AuthorName,
     'Vehicle_Name': Vehicle_Name,
     'Helpful_weight':Helpful_weight,
     'Review_Title': Review_Title,
     'Customer_Rating': Customer_Rating,
     'Review': Review
     })


# In[266]:


df.to_csv("Volvo_edmunds_10yrs.csv")


# In[272]:


df.columns


# In[274]:


df["Vehicle_model"].value_counts()


# In[ ]:




