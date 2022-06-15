#import necessary packages
import requests
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

#get the data from the api
api_url = "http://sam-user-activity.eu-west-1.elasticbeanstalk.com/"
response = requests.get(api_url)
#get json data from the url
data = response.json()
#create a pandas dataframe and populate with data from json
df = pd.DataFrame(list(data.items()), columns=['Date', 'Number of Active Users'])

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Dashboard to view the number of active users per day'),
                                html.Br(),
                                html.Div([
                                dcc.Dropdown(id='startDate', options=[
                                    {'label': i, 'value': i} for i in df.Date.unique()
                                ], placeholder='Filter by start date...'),
                                html.Br(),
                                dcc.Dropdown(id='endDate', options=[
                                    {'label': i, 'value': i} for i in df.Date.unique()
                                ], placeholder='Filter by end date...')], style={"width":"50%","margin-left":"auto","margin-right":"auto"}
                                ),

                                html.Div(dcc.Graph(id="line-graph"), style={"width": "95%", "padding": '10px'})])
def compute_info(start_date, end_date):
    #select range of data
    df_data_selected = df.loc[(df['Date'].between(start_date,end_date))]
    #debugging purposes
    print('Dates Selected: ', df_data_selected)
    return df_data_selected


@app.callback(Output(component_id='line-graph', component_property='figure'),
              [Input("startDate", "value"),
               Input(component_id="endDate", component_property="value")])

def get_graph(start_value, end_value):
    #get the data of the range of dates selected
    dataframe_range = compute_info(start_value, end_value)
    #debugging purposes
    print('Range Selected', dataframe_range)
    #create line graph with figures
    line_fig = px.line(dataframe_range, x='Date', y='Number of Active Users',
                       title='Number of Active Users Between 1-15 January 2022')
    return line_fig



if __name__ == '__main__':
    app.run_server(debug=True)