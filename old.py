# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

import numpy as np
import re
import bs4 as bs
from nltk.corpus import stopwords       # stopwords
from nltk.stem import PorterStemmer     # parsing/stemmer
from nltk.stem import WordNetLemmatizer # stem and context

import nlplot
from plotly.subplots import make_subplots
import string
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

# preprocessing
def conditions(s):
    if (s["Customer_Rating"] >=4):return "positive"
    elif (s["Customer_Rating"] <=2):return "negative"
    else:return "neutral"
ps = PorterStemmer()
wnl = WordNetLemmatizer()
eng_stopwords = set(stopwords.words("english"))

alphabet_string = string.ascii_lowercase

for e in ["volvo","car","xc","vehicle","bmw","audi"]+list(alphabet_string):
    eng_stopwords.add(e)

def review_cleaner(review, lemmatize=True, stem=False):
    if lemmatize == True and stem == True:
        raise RuntimeError("May not pass both lemmatize and stem flags")
    review = bs.BeautifulSoup(review).text    
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', review)    #2. Use regex to find emoticons
    review = re.sub("[^a-zA-Z]", " ",review)#3. Remove punctuation
    review = review.lower().split()#4. Tokenize into words (all lower case)
    clean_review=[]#5. Remove stopwords, Lemmatize, Stem
    for word in review:
        if word not in eng_stopwords:
            if lemmatize is True:
                word=wnl.lemmatize(word)
            elif stem is True:
                if word == 'oed':
                    continue
                word=ps.stem(word)
            clean_review.append(word)
    review_processed = ' '.join(clean_review)#6. Join the review to one sentence
    return review_processed

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="https://www.carlogos.org/car-logos/volvo-logo.png", height="100px")),
                    dbc.Col(
                        dbc.NavbarBrand("VolvoSocialMediaScrap Team 2", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/smeng3/VolvoSocialMediaScrap",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

df = pd.read_csv("data/Volvo_edmunds_10yrs.csv",lineterminator='\n').iloc[:,1:]
df['Review_Date'] = pd.to_datetime(df['Review_Date'],errors='coerce')
df["sentiment"] = df.apply(conditions, axis=1)
df["Review"] = df["Review"].apply(review_cleaner)

# df_plot = df.groupby('sentiment').size().reset_index(name='count')
# fig = px.bar(df_plot, y='count', x='sentiment', text='count')
# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
# fig.update_layout(
#     title=str('sentiment counts'),
#     xaxis_title=str('sentiment'),
#     width=700,
#     height=500,
#     )

npt = nlplot.NLPlot(df, target_col='Review')
npt_negative = nlplot.NLPlot(df.query('sentiment == "negative"'), target_col='Review')
npt_neutral = nlplot.NLPlot(df.query('sentiment == "neutral"'), target_col='Review')
npt_positive = nlplot.NLPlot(df.query('sentiment == "positive"'), target_col='Review')
stopwords = npt.get_stopword(top_n=30, min_freq=0)

fig_npt = []
colors = ["#636EFA","#2CA02C","#FF7F0E","#D62728"]
option = [npt,npt_positive,npt_neutral,npt_negative]
for i in range(len(option)):
    fig_npt.append(option[i].bar_ngram(
            title=str(type)+"-gram",
            xaxis_label='word',
            yaxis_label='word_count',
            ngram=1,
            top_n=50,
            width=1100,
            height=500,
            stopwords=stopwords,
            horizon = False,
            color = colors[i]
        )
    )

TOP_BIGRAM_COMPS = [
    dbc.CardHeader(html.H5("Comparison of bigrams for car models")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                    dbc.Col(html.P("Choose filters:"), md=12),

                    dbc.Col([
                                    dcc.Dropdown(
                                        id="car_model",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in ["all","positive","neutral","negative"]
                                        ],
                                        value="all",
                                    )
                                ],
                                md=6,
                            ),
                    dbc.Col([
                        dcc.Dropdown(
                            id="type_gram",
                            options=[
                            {"label": i, "value": i}
                            for i in ["uniary","binary","trinary"]
                            ],
                            value="uniary",
                             )
                        ],
                        md=6,
                    )
                    ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Tabs(
                                        id="tabs",
                                        children=[
                                            dcc.Tab(
                                                label="all",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-all",
                                                        children=[dcc.Graph(id="all_gram",figure=fig_npt[0])],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="positive",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-wordcloud",
                                                        children=[
                                                            dcc.Graph(id="pos_gram",figure=fig_npt[1])
                                                        ],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="neutral",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-neutral",
                                                        children=[
                                                            dcc.Graph(id="neu_gram",figure=fig_npt[2])
                                                        ],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="negative",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-negitive",
                                                        children=[
                                                            dcc.Graph(id="neg_gram",figure=fig_npt[3])
                                                        ],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                        ],
                                    )
                                ],
                                md=6,
                            ),   
                            
                        ]
                    ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30}),
        # dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_PLOT)),], style={"marginTop": 30}),
        # dbc.Row(
        #     [
        #         dbc.Col(LEFT_COLUMN, md=4, align="center"),
        #         dbc.Col(dbc.Card(TOP_BANKS_PLOT), md=8),
        #     ],
        #     style={"marginTop": 30},
        # ),
        # dbc.Card(WORDCLOUD_PLOTS),
        # dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    className="mt-12",
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Heroku deployment

app.layout = html.Div(children=[
    NAVBAR,BODY

    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

@app.callback(
    Output("all_gram", "figure"), [Input("type_gram", "value")],
)
def populate_bigram_scatter(types):

    fig_npt = []
    colors = ["#636EFA","#2CA02C","#FF7F0E","#D62728"]
    option = [npt,npt_positive,npt_neutral,npt_negative]
    ngram = 0
    if types == "uniary":
        ngram =1
    elif types == "binary":
        ngram = 2
    else:
        ngram =3
    for i in range(len(option)):
        fig_npt.append(option[i].bar_ngram(
            title=str(types)+"-gram",
            xaxis_label='word',
            yaxis_label='word_count',
            ngram=num,
            top_n=50,
            width=1100,
            height=500,
            stopwords=stopwords,
            horizon = False,
            color = colors[i]
            )
        )
    return fig_npt[0]


if __name__ == '__main__':
    app.run_server(debug=True)