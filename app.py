import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

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
        outputValue = str(input_value)
        return outputValue


if __name__ == '__main__':
    app.run_server(debug=True)