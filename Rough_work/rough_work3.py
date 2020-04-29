import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dataframe_populator_rough import dataframe_populator,trend_name_populator
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

external_stylesheets = ['styles.css','custom_styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Read the data for globe
globe_data = pd.read_csv('final_woeid.csv')
globe_fig = px.scatter_geo(globe_data, locations='Alpha-3_code', hover_name='Location', projection="natural earth")


app.layout = html.Div([

#Div containing Logo and title text
    html.Div([
        html.Img(src='assets/twitter_logo.png',id='twitLogo'),
        html.H1(children='Twit-Viz', id='pageTitle')      
        
    ], style={
        'width':'100%',
        'position':'relative'
    }),


    dcc.Tabs([
        
#Tab containing search features
        dcc.Tab(label='Search', children=[   

    #Div containing input field from user
        html.Div([
            html.P('Enter user/profile name below', style={
                 'color':'#4d4d4d'
            }),
            dcc.Input(id='userInput', type='text'),

            html.Button('Get Viz', id='getVizBtn',n_clicks=0)
        ], id="inputContainerDiv" 
        ),
        
    #Display the graph in a Div
        html.Div(id='graphOutput')

        ], className='customtab',selected_className='customtabSelected'),


    #Tab containing global trends features
        dcc.Tab(label='Global Trends', children=[
            
    #Global trends go here
                html.Div([

                    html.H2('Click any point on the globe to get trending tweets of that location!', id='globeHeading'),

                    dcc.Graph(
                        id='globeFigure',
                        figure=globe_fig
                    )   
                ]),

    #Global Updates hashtags go below
            html.Div([
                
            ],id='globalUpdates')

        ], className='customtab', selected_className='customtabSelected'),       
            
], className='customtabsContainer')
])


##############################Call back functions start###############################

#Getting inputs from user
@app.callback(
    Output('graphOutput', 'children'),
    [Input('getVizBtn', 'n_clicks')],
    [State('userInput', 'value')]
)
def getInput(n_clicks,input_value):
    if (input_value):
        input_value = str(input_value)
            
        dataframe_orig = dataframe_populator(input_value)
        #output_value = list(dataframe_orig['Sentiment'])
        #viz_plot = px.line(dataframe_orig, y=dataframe_orig['Sentiment'], hover_data=["Tweet","Created_at","Retweets"],title='Sentiments',width=600,height=400)
        return(
                dcc.Graph(
                    id='example-graph-2',
                    figure={
                        'data': [
                            {'y': dataframe_orig['Sentiment'], 'type': 'line'},                
                        ],
                        'layout': {
                            'plot_bgcolor': '#f4f4f4',
                            'paper_bgcolor': 'white',
                            'height':'400',
                            'width':'500',
                            'hoverData':dataframe_orig['Tweet'],
                            'font': {
                                'color': '#1da1f2'
                            }
                        }
                    }
                )
        )

#Global Viz updates
#@app.callback(
    Output('globeOutput', 'children'),
    [Input('globeViz', 'n_clicks')],    
#)
#def drawGlobe(input_value):
    if (input_value):
        input_value = str(input_value)
        globe_data = pd.read_csv('final_woeid.csv')

        globe_fig = px.scatter_geo(globe_data, locations='Alpha-3_code', hover_name='Woe_Id')        

        return(
            dcc.Graph(
                id='globeFigure',
                figure=globe_fig
            )
        )

#Globe hashtag updates 
@app.callback(
    Output('globalUpdates','children'),    
    [Input('globeFigure','clickData')]  
)
def globe_data_update(clickData):
    if(clickData):
        country_name = str(clickData["points"][0]["hovertext"])
        woe_id = int(globe_data[globe_data['Country'] == country_name]['Woe_Id'])       
        trend_list=[]
        trend_list = trend_name_populator(woe_id)        
        return(type(trend_list))


if __name__ == '__main__':
    app.run_server(debug=True)