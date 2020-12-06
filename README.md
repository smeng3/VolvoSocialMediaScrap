# VolvoSocialMediaScrap
## – Volvo Social Media Crawler & Predictor #2 (DATA-X)
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

#### Dataset Collected:
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

## Part II: NLP Modeling:


## Part III: NLP Visualization:


### Other

- Plotly is used to plot the figure
    - https://plotly.com/python/

- co-occurrence networks is used to calculate the co-occurrence network
    - https://networkx.github.io/documentation/stable/tutorial.html

- The following is used to plot pyLDAvis
    - https://github.com/bmabey/pyLDAvis

- wordcloud uses the following fonts
    - https://mplus-fonts.osdn.jp/about.html
