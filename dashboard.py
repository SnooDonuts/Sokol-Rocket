
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import time
import os

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Rocket Telemetry Dashboard"

# Define the layout of the app
app.layout = html.Div([
    html.H1("Rocket Telemetry Dashboard", style={'text-align': 'center'}),
    
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    ),
    
    html.Div(id='live-update-text'),
    
    dcc.Graph(id='live-update-graph')
])

# Function to read the latest data from the CSV file
def get_latest_data(csv_file_path):
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        df = pd.read_csv(csv_file_path)
        latest_data = df.iloc[-1]  # Get the last row
        return latest_data
    return None

# Update the text and graph at regular intervals
@app.callback(
    [Output('live-update-text', 'children'),
     Output('live-update-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    csv_file_path = './rocket_data.csv'
    latest_data = get_latest_data(csv_file_path)
    
    if latest_data is not None:
        # Update the text with the latest data
        text = [
            html.P(f"Timestamp: {latest_data['Timestamp']}"),
            html.P(f"Longitude: {latest_data['Longitude']}"),
            html.P(f"Latitude: {latest_data['Latitude']}"),
            html.P(f"AccelX: {latest_data['AccelX']} g"),
            html.P(f"AccelY: {latest_data['AccelY']} g"),
            html.P(f"AccelZ: {latest_data['AccelZ']} g"),
            html.P(f"GyroX: {latest_data['GyroX']} °/s"),
            html.P(f"GyroY: {latest_data['GyroY']} °/s"),
            html.P(f"GyroZ: {latest_data['GyroZ']} °/s"),
            html.P(f"Parachute Deployed: {latest_data['Parachute']}")
        ]

        # Update the graph with the latest acceleration data
        figure = {
            'data': [
                {'x': df['Timestamp'], 'y': df['AccelX'], 'type': 'line', 'name': 'AccelX'},
                {'x': df['Timestamp'], 'y': df['AccelY'], 'type': 'line', 'name': 'AccelY'},
                {'x': df['Timestamp'], 'y': df['AccelZ'], 'type': 'line', 'name': 'AccelZ'},
            ],
            'layout': {
                'title': 'Acceleration Data Over Time'
            }
        }
    else:
        text = [html.P("No data available.")]
        figure = {}

    return text, figure

# Async function to run the Dash app
def run_dashboard():
    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

if __name__ == "__main__":
    run_dashboard()
