import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

my_new_dataset = pd.read_csv('stemmed_senti.csv')
my_new_dataset['Sentiment'] = my_new_dataset['Sentiment'].apply(lambda x:round(x,2) * 100) 


my_figure = px.line(my_new_dataset, y=my_new_dataset['Sentiment'], hover_data=["Tweet","Created_at","Retweets"])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    #Div containing Logo and title text
    html.Div(id='tempOutput'),

    #dcc.Graph(
    #    id='Sentiment',
    #        figure= my_figure      
    #    )

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'y': my_new_dataset['Sentiment'], 'type': 'line'},                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'height':'400',
                'width':'500',
                'hoverData':my_new_dataset['Tweet'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)