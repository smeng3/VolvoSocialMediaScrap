# VolvoSocialMediaScrap – Volvo Social Media Crawler & Predictor #2 (DATA-X)
#### *A repository for web scraping of Volvo car reviews* 

#### By: Sixu Meng, Zhecan Huang, Xiyu He, Kai Lun Chen, Shreyas Hariharan, Suyash Jaju


#### Overview: 
As we have now entered the era of data and information, traditional businesses have begun riding the wave of increasingly powerful data science tools to support their decision making and gather insight for strategic planning. Volvo, a global luxury automotive manufacturer from Sweden that produces more than 700,000 cars per year, is similarly looking to assemble all the raw data from the internet and leverage it to improve their business strategy and planning. Most customers and vehicle owners prefer using social media and forums to post reviews and comments about their newly purchased car rather than responding to surveys; thus, it is highly beneficial for Volvo’s business operation team to parse this raw data and extract meaningful information. Hence, this year, Volvo joined forces with 6 UC Berkeley students to build a comprehensive dashboard showcasing essential information extracted from car review websites, notably what customers like or dislike about their Volvos. 

Implementing the classic data analysis approach, the Berkeley team of students began with scraping a large amount of data on Volvo vehicle models from famous car reviews websites such as Edmunds and KBB. Then, the team subsequently modeled the scraped data with natural language processing tools to analyze customer sentiment by identifying common words and topics found across online reviews. The final results were displayed in a custom-built dashboard provided to Volvo for future use. The dashboard includes graphs and interactive components representing various insights derived from sentiment analysis, allowing Volvo to easily navigate and visualize key information. 


Read more about the project on our News Release: *[Click Here](https://docs.google.com/document/d/1__y8xFW6x_ceoO0J9vSxzERt0ygRiZAzwPgxR2AduFo/edit?usp=sharing)*


##### Visualizations: *[Click Here](https://smeng3.github.io/VolvoSocialMediaScrap/).*

##### Story of Project: *[Click Here](https://drive.google.com/file/d/1jNIdr0YYvRiAqAeUiLbnZIr0yQxRonUG/view?usp=sharing)*

#### Table of Contents: 
| File Name | Description |
| --- | ----------- |
| NLP Visualization.ipynb | Code for visualizing text data using NLPlot and Dash Plotly| 
| NLP Modeling.ipynb | Code for cleaning text data and conducting elementary topic analysis + generating word clouds | 
| Web Scraping.ipynb | Code used to web scrape customer reviews about Volvo from Edmund, a popular car review website| 
| data | Web Scraped Volvo Car Review Data from edmunds.com|
| extra data | Web Scraped Other Brands of Car Review Data from edmunds.com | 

#### Requirement
- [python package](https://github.com/smeng3/VolvoSocialMediaScrap/blob/main/requirements.txt)

## Part I: Web Scraping

We collects three sets of data from Edmunds.com. In our data folder, we have other_car_review_volvo.csv and Volvo_edmunds_10yrs.csv, which ars all the data that we were able to gather on Volvo which we used to help train and test our sentimental analysis model. This allows the Volvo team to continue using this model with any new reviews that they may get or any internal reviews as well.

For our dashboard and topic analysis, we only used data from the recent 10 years of Volvo cars(Volvo_edmunds_10yrs.csv)

In our extra_data folder, we were able to gather data on 49 other car brands to supplement our sentimental model to update our vocabulary, and conduct semi-supervised learning.


#### Dataset Collected（Volvo_edmunds_10yrs.csv）:
| Volvo Model Name | Reviews (counts) |
| --- | ----------- |
|XC60|244|
|S60|232|
|XC90|223|
|XC40|89|
|XC70|54|
|S90|53|
|V60|46|
|C70|33|
|C30|33|
|V60 Cross Country|26|
|S80|18|
|V90 Cross Country|11|
|V90|10|
|V50|4|
|S60 Cross Country|2|
|S40|1|
|Total|1079|

##### Webscraping file location: VolvoSocialMediaScrap/Web Scraping.ipynb


## Part II: NLP Modeling:

For the sentimental analysis and modeling part, we conduct semi-supervied random forest model. We used SMOTE (oversampling) to do oversampling for our data with lable 0. And we used extra datasets of other cars (unlabeled data) to help train model.

We get 0.95 accuracry for our validation set, and 0.74 recall rate for our minority group. 

##### Modeling file location: VolvoSocialMediaScrap/NLP Modeling.ipynb


## Part III: NLP Visualization:

Based on the analysis we have done on volvo's review, we made visualizations and a dashboard.

One of the many visualizations we created were word clouds. On the screen you can see the different words associated with positive, neutral and negative customer sentiments respectively which help Volvo identify the strengths and weaknesses based on customer experiences. 
For example, positives words that are highlighted in the word-cloud are “design and performance”, which indicate that customers love the way the car looks and drives. On the other hands, some negative words used to describe Volvo are  “service” and “dealer”. This could provide some clues that Volvo might be focusing more on their car products but not so much on the customer experience around maintenance and upkeep. Volvo could then derive a strategic plan to focus on improving the quality of maintenance services they provide to customers!

Another such visualization we created was a co-occurrence network to illustrate the potential word relationships from online reviews. Red highlights negative, yellow highlights neutral, and green highlights positive sentiment-relationships. 
This will help Volvo identify what words and problems might be related to one another. Volvo can then introduce new features by identifying patterns in the analysis and save costs by prioritizing improvements that target multiple problem-areas for maximum business impact.

To give a brief overview of the dashboard: The dashboard can give uniary, binary, or ternary combination of worlds that customers used to describe the positive, neuture, ad negative sides of volvo's car. We can also select specific car models to see the reviews. We also have a treemap which displays a sentiment tree of most common words used in customer complaints. And we also have these most common words are displayed in a sunburst chart used to describe hierarchical data. This will help Volvo identify the popular issues customers face, for example the word “interior”, that is highlighted in red on the right. The dashboard allows Volvo to learn how their vehicles reflect in the market and therefore build improved solutions faster for future car models. However, the access of the dashboard need an environment set up, so it currently only runs in our local computer.


##### Visualizations file location: VolvoSocialMediaScrap/NLP Visualization.ipynb


## Next Step
With more time, our team would like to: 
Scrape more data from car review websites like KBB to strengthen our modeling and analysis
Utilize Selenium to automate clicking through online reviews for dynamic websites with changing parameters 

Automate web-scraping and dashboard-updating when new reviews are added to the websites
Requires more time and effort but will improve process efficiency for Volvo




### Other

- Plotly is used to plot the figure
    - https://plotly.com/python/

- co-occurrence networks is used to calculate the co-occurrence network
    - https://networkx.github.io/documentation/stable/tutorial.html

- The following is used to plot pyLDAvis
    - https://github.com/bmabey/pyLDAvis

- wordcloud uses the following fonts
    - https://mplus-fonts.osdn.jp/about.html
