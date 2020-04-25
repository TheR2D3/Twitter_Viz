import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dataframe_populator import dataframe_populator
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['styles.css','custom_styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    #Div containing Logo and title text
    html.Div([
        html.Img(src='assets/twitter_logo.png',id='twitLogo'),
        html.H1(children='Twit-Viz', id='pageTitle')      
        
    ], style={
        'width':'100%',
        'position':'relative'
    }),

    #Div containing buttons of two pages
    html.Div([
        html.Button('User Viz',type='submit', id='userVizBtn'),
        html.Button('HashTag Viz',type='submit', id='hashTagBtn')
    ], style={
            'width':'100%',
            'text-align':'center',
            'position':'relative'            
        }
    ),

    #Div containing input field from user
     html.Div([
         html.P('Enter user/profile name below', style={
             'color':'#4d4d4d'
         }),
         dcc.Input(id='userInput', type='text'),
         html.Button('Get Viz', id='getVizBtn',n_clicks=0)
    ], id="inputContainerDiv" 
    ),

    html.Div(id='tempOutput')
])

#Getting inputs from user
@app.callback(
    Output('tempOutput', 'children'),
    [Input('getVizBtn', 'n_clicks')],
    [State('userInput', 'value')]
)
def getInput(n_clicks,input_value):
    if (input_value):
        input_value = str(input_value)
            
        dataframe_orig = dataframe_populator(input_value)
        #output_value = list(dataframe_orig['Sentiment'])
        viz_plot = px.line(dataframe_orig, y=dataframe_orig['Sentiment'], hover_data=["Tweet","Created_at","Retweets"],title='Sentiments',width=600,height=400)
        return(
                dcc.Graph(
                    id='Sentiment',
                    figure=viz_plot  
                )
        )

if __name__ == '__main__':
    app.run_server(debug=True)