import pandas as pd
from pymongo import MongoClient
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div([
        html.Div(
            dcc.Interval(
                id='interval-component',
                interval=10000, # in milliseconds
                n_intervals=0
                    ))]
, style={'width': '100%', 'display': 'inline-block'}
            ),
    html.Div([
        
        html.Div(
            dcc.Graph(
                id='stacked-bar',
                    ), style={'display': 'inline-block','width':'85%'})]
    , style={'width': '100%', 'display': 'inline-block'}
            )
    ])

@app.callback(Output('stacked-bar', 'figure'),
              [Input('interval-component', 'n_intervals')])
def stacked_bar(n):
    try:
        client = MongoClient('localhost', 27017)
        database = client['tweet']
        print("Connected successfully")
    except:  
        print("Could not connect to MongoDB")
    collection = database['tweet_info']
    tweets = pd.DataFrame(list(collection.find()))
    
    df = tweets.groupby('topic')['cat_senti'].apply(lambda x: x.value_counts()).reset_index()
    
    x = ["binance", "bitcoin", "ethereum", "solana", "tether"]

    data = [go.Bar(
                    name = 'Neutral',
                    x = x,
                    y = df[df['level_1']=='Neutral']['cat_senti'].to_list()
                  ),
            go.Bar(
                    name = 'Positive',
                    x = x,
                    y = df[df['level_1']=='Positive']['cat_senti'].to_list()
                  ),
            go.Bar(
                    name = 'Negative',
                    x = x,
                    y = df[df['level_1']=='Negative']['cat_senti'].to_list()
                  )]
    
    layout = go.Layout(
           title = "<b>A Real-Time Cryptocurrency Sentiment Analysis</b>",
           titlefont=dict(size=25),
           font=dict(size=16),
           height=800,
           barmode='stack')
    
    fig = go.Figure(data=data, layout=layout)
    for i in  fig['data'][:]:
        i.width = 0.4
    
    return fig

if __name__ == '__main__':
    app.run_server()