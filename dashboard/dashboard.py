import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import redis
import json
import os


redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]
redis_key = os.environ["REDIS_KEY"] 
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

historical_data = {
    "timestamps": [],
    "network_egress": [],
    "memory_caching": [],
    "cpu_utilization": {f"CPU {i}": [] for i in range(16)}
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Serverless Monitoring Dashboard", style={'display': 'flex', 'justifyContent': 'center'}),
    dcc.Interval(id='update-interval', interval=5000, n_intervals=0),
    
    html.Div([
        html.Div([
            dcc.Graph(id='network-egress-graph')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),
        
        html.Div([
            dcc.Graph(id='memory-caching-graph')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    html.Div([
        html.H2("CPU Utilization (%)"),
        dcc.Graph(id='cpu-util-graph', style={'width': '80%'})
    ], style={
        'display': 'flex',  
        'flexDirection': 'column', 
        'alignItems': 'center',  
        'justifyContent': 'center',  
        'textAlign': 'center'
    }),                                                                                                 
])

@app.callback(
    [Output('network-egress-graph', 'figure'),
     Output('memory-caching-graph', 'figure'),
     Output('cpu-util-graph', 'figure')],
    [Input('update-interval', 'n_intervals')]
)
def update_graphs(n_intervals):
    try:
        raw_data = redis_client.get(redis_key)
        if not raw_data:
            raise ValueError("No data found for the specified key in Redis.")
        sample_data = json.loads(raw_data)
    except Exception as e:
        print(f"Error fetching data from Redis: {e}")
        sample_data = {
            "timestamp": str(datetime.now()),
            "percent_network_egress": 0,
            "percent_memory_caching": 0,
            **{f"avg_util_cpu{i}_60sec": 0 for i in range(16)}
        }

    timestamp = datetime.strptime(sample_data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")

    historical_data["timestamps"].append(timestamp)
    historical_data["network_egress"].append(sample_data["percent_network_egress"])
    historical_data["memory_caching"].append(sample_data["percent_memory_caching"])
    for i in range(16):
        historical_data["cpu_utilization"][f"CPU {i}"].append(sample_data[f"avg_util_cpu{i}_60sec"])

    network_egress_fig = go.Figure(
        data=[go.Scatter(
            x=historical_data["timestamps"], 
            y=historical_data["network_egress"], 
            mode="lines+markers", 
            name="Network Egress"
        )],
        layout=go.Layout(title="Network Egress (%)", title_x=0.5, yaxis={"title": "Percentage"}, xaxis={"title": "Timestamp"})
    )

    memory_caching_fig = go.Figure(
        data=[go.Scatter(
            x=historical_data["timestamps"], 
            y=historical_data["memory_caching"], 
            mode="lines+markers", 
            name="Memory Caching"
        )],
        layout=go.Layout(title="Memory Caching (%)", title_x=0.5, yaxis={"title": "Percentage"}, xaxis={"title": "Timestamp"})
    )

    cpu_util_fig = go.Figure(
        data=[
            go.Scatter(
                x=historical_data["timestamps"], 
                y=historical_data["cpu_utilization"][f"CPU {i}"], 
                mode="lines+markers", 
                name=f"CPU {i}"
            ) for i in range(16)
        ],
        layout=go.Layout(title="CPU Utilization (%)", title_x=0.5, yaxis={"title": "Utilization (%)"}, xaxis={"title": "Timestamp"})
    )

    return network_egress_fig, memory_caching_fig, cpu_util_fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=52033)