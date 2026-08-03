from flask import Flask
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Create Flask server
server = Flask(__name__)

# Health check endpoint
@server.route('/health')
def health():
    return 'OK'

# Initialize Dash app
app = dash.Dash(__name__, server=server)

# Create sample data
dates = pd.date_range(start='2020-01-01', periods=50, freq='W')
np.random.seed(42)
sales = 10000 + np.cumsum(np.random.randn(50) * 500)
df = pd.DataFrame({'Date': dates, 'Sales': sales})

# Dashboard layout
app.layout = html.Div([
    html.H1('📊 Retail Sales Dashboard', style={
        'textAlign': 'center',
        'color': '#2c3e50',
        'marginTop': '50px'
    }),
    html.P('Dashboard is working!', style={
        'textAlign': 'center',
        'fontSize': '20px',
        'color': '#666'
    }),
    dcc.Graph(
        figure={
            'data': [go.Scatter(
                x=df['Date'],
                y=df['Sales'],
                mode='lines+markers',
                name='Sales',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8, color='#764ba2')
            )],
            'layout': go.Layout(
                title='Sales Over Time',
                xaxis_title='Date',
                yaxis_title='Sales ($)',
                template='plotly_white',
                height=400
            )
        }
    )
])

# IMPORTANT: Vercel needs this exact variable name
application = app.server

# Also export app for compatibility
app = app

if __name__ == '__main__':
    application.run(debug=True, port=8050)
