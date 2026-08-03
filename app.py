from flask import Flask
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Create Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server)

# Create sample data
dates = pd.date_range(start='2020-01-01', periods=100, freq='W')
np.random.seed(42)
sales = 10000 + np.linspace(0, 5000, 100) + 3000*np.sin(np.arange(100)*2*np.pi/12) + np.random.normal(0, 1000, 100)
df = pd.DataFrame({'Date': dates, 'Weekly_Sales': sales})

# Dashboard layout
app.layout = html.Div([
    html.Div([
        html.H1("📊 Retail Sales Dashboard", style={
            'textAlign': 'center',
            'color': 'white',
            'padding': '30px',
            'margin': '0'
        }),
        html.P("Interactive Sales Analytics", style={
            'textAlign': 'center',
            'color': '#e0e0e0',
            'fontSize': '18px'
        })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'borderRadius': '0 0 20px 20px',
        'marginBottom': '20px'
    }),

    # KPI Cards
    html.Div([
        html.Div([
            html.H4("💰 Total Sales", style={'color': '#666', 'margin': '0'}),
            html.H2(f"", style={'color': '#2c3e50', 'margin': '10px 0'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'textAlign': 'center',
            'borderLeft': '4px solid #3498db'
        }),
        html.Div([
            html.H4("📈 Average Sales", style={'color': '#666', 'margin': '0'}),
            html.H2(f"", style={'color': '#2c3e50', 'margin': '10px 0'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'textAlign': 'center',
            'borderLeft': '4px solid #2ecc71'
        }),
        html.Div([
            html.H4("🏆 Max Sales", style={'color': '#666', 'margin': '0'}),
            html.H2(f"", style={'color': '#2c3e50', 'margin': '10px 0'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'textAlign': 'center',
            'borderLeft': '4px solid #e74c3c'
        })
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 20px 20px 20px'}),

    # Charts
    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure={
                'data': [go.Scatter(
                    x=df['Date'],
                    y=df['Weekly_Sales'],
                    mode='lines+markers',
                    name='Sales',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#764ba2')
                )],
                'layout': go.Layout(
                    title='Sales Over Time',
                    xaxis_title='Date',
                    yaxis_title='Weekly Sales ($)',
                    template='plotly_white',
                    height=400
                )
            }
        )
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'margin': '20px'
    }),

    html.Div([
        dcc.Graph(
            id='distribution',
            figure={
                'data': [go.Histogram(
                    x=df['Weekly_Sales'],
                    nbinsx=20,
                    marker_color='#667eea',
                    opacity=0.7
                )],
                'layout': go.Layout(
                    title='Sales Distribution',
                    xaxis_title='Sales Amount ($)',
                    yaxis_title='Frequency',
                    template='plotly_white',
                    height=350
                )
            }
        )
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'margin': '20px'
    }),

    html.Div([
        html.P("🚀 Dashboard Deployed on Vercel", style={'textAlign': 'center', 'color': '#95a5a6', 'padding': '20px'})
    ])
], style={'backgroundColor': '#f5f6fa', 'minHeight': '100vh'})

# This is the WSGI application for Vercel
application = app.server

if __name__ == '__main__':
    application.run(debug=True, port=8050)
