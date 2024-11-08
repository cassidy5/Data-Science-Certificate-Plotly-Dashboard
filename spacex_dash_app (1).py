# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Load the data into a DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a Dash application
app = dash.Dash(__name__)


# Application layout
app.layout = html.Div(children=[
   html.H1('SpaceX Launch Records Dashboard',
           style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
  
   # Task 1: Launch Site Dropdown
   dcc.Dropdown(id='site-dropdown',
                options=[{'label': 'All Sites', 'value': 'ALL'}] +
                        [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                value='ALL',
                placeholder="Select a Launch Site",
                searchable=True
                ),
   html.Br(),


   # Task 2: Success Pie Chart
   html.Div(dcc.Graph(id='success-pie-chart')),
   html.Br(),


   # Task 3: Payload Range Slider
   html.P("Payload range (Kg):"),
   dcc.RangeSlider(id='payload-slider',
                   min=0, max=10000, step=1000,
                   marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                   value=[min_payload, max_payload]),
   html.Br(),


   # Task 4: Success-Payload Scatter Chart
   html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# Task 2: Callback for updating pie chart based on selected site
@app.callback(
   Output(component_id='success-pie-chart', component_property='figure'),
   Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
   if selected_site == 'ALL':
       fig = px.pie(spacex_df, values='class', names='Launch Site',
                    title='Total Success Launches by Site')
   else:
       filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
       fig = px.pie(filtered_df, names='class',
                    title=f'Total Success Launches for site {selected_site}')
   return fig


# Task 4: Callback for updating scatter plot based on selected site and payload range
@app.callback(
   Output(component_id='success-payload-scatter-chart', component_property='figure'),
   [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
   filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                           (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
  
   if selected_site != 'ALL':
       filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]


   fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                    title='Payload vs. Success for selected site',
                    labels={'class': 'Launch Outcome'})
   return fig


# Run the app
if __name__ == '__main__':
   app.run_server()
