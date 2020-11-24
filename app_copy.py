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
car_model = ["all",'C30', 'C70', 'S40', 'S60 Cross Country', 'S80', 'V50', 'XC70',
       'S60', 'S90', 'V60', 'V60 Cross Country', 'V90',
       'V90 Cross Country', 'XC40', 'XC60', 'XC90']
# df_plot = df.groupby('sentiment').size().reset_index(name='count')
# fig = px.bar(df_plot, y='count', x='sentiment', text='count')
# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
# fig.update_layout(
#     title=str('sentiment counts'),
#     xaxis_title=str('sentiment'),
#     width=700,
#     height=500,
#     )

# npt = nlplot.NLPlot(df, target_col='Review')
# npt_negative = nlplot.NLPlot(df.query('sentiment == "negative"'), target_col='Review')
# npt_neutral = nlplot.NLPlot(df.query('sentiment == "neutral"'), target_col='Review')
# npt_positive = nlplot.NLPlot(df.query('sentiment == "positive"'), target_col='Review')
# stopwords = npt.get_stopword(top_n=30, min_freq=0)

# # positive/neutral/negative
# fig_unigram_positive = npt_positive.bar_ngram(
#     title='uni-gram',
#     xaxis_label='word_count',
#     yaxis_label='word',
#     ngram=1,
#     top_n=50,
#     width=800,
#     height=1100,
#     stopwords=stopwords,
# )

# fig_unigram_neutral = npt_neutral.bar_ngram(
#     title='uni-gram',
#     xaxis_label='word_count',
#     yaxis_label='word',
#     ngram=1,
#     top_n=50,
#     width=800,
#     height=1100,
#     stopwords=stopwords,
# )

# fig_unigram_negative = npt_negative.bar_ngram(
#     title='uni-gram',
#     xaxis_label='word_count',
#     yaxis_label='word',
#     ngram=1,
#     top_n=50,
#     width=800,
#     height=1100,
#     stopwords=stopwords,
# )

# # subplot
# trace1 = fig_unigram_positive['data'][0]
# trace2 = fig_unigram_neutral['data'][0]
# trace3 = fig_unigram_negative['data'][0]

# fig = make_subplots(rows=1, cols=3, subplot_titles=('positive', 'neutral', 'negative'), shared_xaxes=False)
# fig.update_xaxes(title_text='word count', row=1, col=1)
# fig.update_xaxes(title_text='word count', row=1, col=2)
# fig.update_xaxes(title_text='word count', row=1, col=3)

# fig.update_layout(height=1100, width=1000, title_text='unigram positive vs neutral vs negative')
# fig.add_trace(trace1, row=1, col=1)
# fig.add_trace(trace2, row=1, col=2)
# fig.add_trace(trace3, row=1, col=3)



TOP_BIGRAM_COMPS = [
    dbc.CardHeader(html.H5("Comparison of Positive/Negative/Neutral for Uniary/Binary/Trinary words")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Choose car model and type of graph:"), md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="bigrams-comp_1",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in car_model
                                        ],
                                        value="all",
                                    )
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="bigrams-comp_2",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in ["uniary","binary","trinary"]
                                        ],
                                        value="uniary",
                                    )
                                ],
                                md=6,
                            ),
                        ]
                    ),
                    dcc.Graph(id="bigrams-comps"
                        ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

npt = nlplot.NLPlot(df, target_col='Review') 
stopwords = npt.get_stopword(top_n=30, min_freq=0)
treemap = npt.treemap(width=800, height=500,title='All sentiment Tree of Most Common Words',
    ngram=1,stopwords=stopwords)
npt.build_graph(stopwords=stopwords, min_edge_frequency=25)

sunburst = npt.sunburst(
    title='All sentiment sunburst chart',
    colorscale=True,
    color_continuous_scale='Oryel',
    width=800,
    height=500,
)

WORDCLOUD_PLOTS = [
    dbc.CardHeader(html.H5("Most frequently used words in complaints")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[dcc.Graph(id="bank-treemap",figure =treemap)],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Sunburst",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud",
                                                children=[
                                                    dcc.Graph(figure = sunburst)
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]


BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(WORDCLOUD_PLOTS)),], style={"marginTop": 30}),
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
])

@app.callback(
    [Output("bigrams-comps", "figure"),Output("no-data-alert-bank", "style")],
    [Input("bigrams-comp_1", "value"), Input("bigrams-comp_2", "value")],
)
def comp_bigram_comparisons(comp_first, comp_second):
    if comp_first == "all":
        df_here = df.copy()
    else:
        df_here = df[df["Vehicle_model"]==comp_first].copy()

    ngram = 0
    if comp_second == "uniary":
        ngram =1
    elif comp_second == "binary":
        ngram = 2
    else:
        ngram =3
    top_n = 0
    if len(df_here)< 30:
        top_n = len(df_here)
    else:
        top_n = 30
    alert_style = {"display": "none"}

    npt = nlplot.NLPlot(df_here, target_col='Review') 
    npt_negative = nlplot.NLPlot(df_here.query('sentiment == "negative"'), target_col='Review')
    npt_neutral = nlplot.NLPlot(df_here.query('sentiment == "neutral"'), target_col='Review')
    npt_positive = nlplot.NLPlot(df_here.query('sentiment == "positive"'), target_col='Review')
    stopwords = npt.get_stopword(top_n=top_n, min_freq=0)
    # positive/neutral/negative
    fig_unigram_positive = npt_positive.bar_ngram(
        title=str(comp_second)+'-gram',
        xaxis_label='word_count',
        yaxis_label='word',
        ngram=ngram,
        top_n=top_n,
        stopwords=stopwords,
    )

    fig_unigram_neutral = npt_neutral.bar_ngram(
        title=str(comp_second)+'-gram',
        xaxis_label='word_count',
        yaxis_label='word',
        ngram=ngram,
        top_n=top_n,
        stopwords=stopwords,
    )

    fig_unigram_negative = npt_negative.bar_ngram(
        title=str(comp_second)+'-gram',
        xaxis_label='word_count',
        yaxis_label='word',
        ngram=ngram,
        top_n=top_n,
        stopwords=stopwords,
    )

    # subplot
    trace1 = fig_unigram_positive['data'][0]
    trace2 = fig_unigram_neutral['data'][0]
    trace3 = fig_unigram_negative['data'][0]

    fig = make_subplots(rows=1, cols=3, subplot_titles=('positive', 'neutral', 'negative'), shared_xaxes=False)
    fig.update_xaxes(title_text='word count', row=1, col=1)
    fig.update_xaxes(title_text='word count', row=1, col=2)
    fig.update_xaxes(title_text='word count', row=1, col=3)

    fig.update_layout(height=1100, width=1000, title_text=str(comp_second)+'-gram positive vs neutral vs negative')
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=2)
    fig.add_trace(trace3, row=1, col=3)
    if (fig == {}):
        alert_style = {"display": "block"}

    return [fig,alert_style]



if __name__ == '__main__':
    app.run_server(debug=False)