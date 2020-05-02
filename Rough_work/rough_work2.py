import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dataframe_populator_rough import dataframe_populator,trend_name_populator,trend_tweet_populator
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import sys

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
        html.Div(id='graphOutput'),

        html.Div([
                html.P('This is where custom inputs go'),

                dcc.Dropdown(id='Graph_Selector1',
                    options=[
                        {'label': 'Hour of Tweet', 'value': 'HOUR'},
                        {'label': 'Day of Tweet', 'value': 'DAY'},
                        {'label': 'No of Tweets', 'value': 'NOTWEETS'},                        
                    ],
                placeholder="Select a feature - x axis",clearable=True, style={
                    'width':'50%',
                    'position':'relative',
                    'float':'left',
                    'display': 'inline-block'                    
                }),

                dcc.Dropdown(id='Graph_Selector2',
                    options=[
                        #Contents will be dynamically populated based on Input from above selector
                    ],
                placeholder="Select a feature - y-axis",clearable=True,style={
                    'width':'50%',
                    'position':'relative',
                    'float':'left',
                    'display': 'inline-block'                    
                }),

                dcc.RadioItems(id='typeOfPlot',
                  options=[
                    {'label': 'Scatter Plot', 'value': 'SCT'},
                    {'label': 'Line Plot', 'value': 'LINE'}                    
                    ],
                    labelStyle={'display': 'inline-block'}
                ), 

                html.Button('Plot graph!', id='plotGraphBtn',n_clicks=0),

                html.Div(id='userGraphOutput')
        ],                              
        id='customUserInputs')

        

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
                html.P('Trending hashtags')
                
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
        trend_tweets_1=[]
        trend_tweets_2=[]
        trend_tweets_3=[]
        trend_tweets_4=[]
        trend_tweets_5=[]

        trend_list = trend_name_populator(woe_id)

        trend_tweets_1 = trend_tweet_populator(str(trend_list[0]))
        trend_tweets_2 = trend_tweet_populator(str(trend_list[1]))
        trend_tweets_3 = trend_tweet_populator(str(trend_list[2]))
        trend_tweets_4 = trend_tweet_populator(str(trend_list[3]))
        trend_tweets_5 = trend_tweet_populator(str(trend_list[4]))

        return(
               dcc.Tabs(id='tabsTrends', value='tab-1', vertical=True ,children=[
                    
                    dcc.Tab(label=trend_list[0], value='tab-1', children=[
                        html.P(trend_tweets_1[0]),                        
                        html.P(trend_tweets_1[1]),
                        html.P(trend_tweets_1[2]),
                        html.P(trend_tweets_1[3])                                        
                    ]),
                    
                    dcc.Tab(label=trend_list[1], value='tab-2', children=[                        
                        html.P(trend_tweets_2[0]),
                        html.P(trend_tweets_2[1]),
                        html.P(trend_tweets_2[2]),
                        html.P(trend_tweets_2[3])  
                    ]),

                    dcc.Tab(label=trend_list[2], value='tab-3', children=[
                        html.P(trend_tweets_3[0]),
                        html.P(trend_tweets_3[1]),
                        html.P(trend_tweets_3[2]),
                        html.P(trend_tweets_3[3]) 
                    ]),

                    dcc.Tab(label=trend_list[3], value='tab-4', children=[
                        html.P(trend_tweets_4[0]),
                        html.P(trend_tweets_4[1]),
                        html.P(trend_tweets_4[2]),
                        html.P(trend_tweets_4[3]) 
                    ]),

                    dcc.Tab(label=trend_list[4], value='tab-5', children=[
                        html.P(trend_tweets_5[0]),
                        html.P(trend_tweets_5[1]),
                        html.P(trend_tweets_5[2]),
                        html.P(trend_tweets_5[3]) 
                    ])
                ])
        )


#User custom graphs
@app.callback(
    Output('Graph_Selector2','options'),
    [Input('Graph_Selector1','value')]
)

def dropdownUpdater(clickData):
    if(clickData == 'HOUR' or 'DAY'): 
        #print(clickData, file=sys.stderr)        
        return({'label': 'No of Tweets', 'value': 'NOTWEETS'},{'label': 'No of Re-Tweets', 'value': 'NORETWEETS'},{'label': 'Favourites', 'value': 'FAVOURITES'})

@app.callback(
    Output('userGraphOutput','children'),
    [Input('plotGraphBtn','n_clicks'),
    Input('Graph_Selector1', 'value'),
    Input('typeOfPlot','value'),
    Input('Graph_Selector2', 'value')]
)
def userGraphUpdater(n_clicks,value1,value2,value3):
    if(n_clicks):
        print(n_clicks,value1,value2, file=sys.stderr)
        return(n_clicks,value1,value2)

if __name__ == '__main__':
    app.run_server(debug=True)