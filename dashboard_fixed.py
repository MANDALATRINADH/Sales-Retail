import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os

# Create data if it doesn't exist
if not os.path.exists('data/train.csv'):
    os.makedirs('data', exist_ok=True)
    dates = pd.date_range(start='2020-01-01', periods=100, freq='W')
    np.random.seed(42)
    sales = 10000 + np.linspace(0, 5000, 100) + 3000*np.sin(np.arange(100)*2*np.pi/12) + np.random.normal(0, 1000, 100)
    df = pd.DataFrame({'Date': dates, 'Weekly_Sales': sales})
    df.to_csv('data/train.csv', index=False)
    print('✅ Created sample data!')

# Load data
df = pd.read_csv('data/train.csv', parse_dates=['Date'])
sales_data = df.groupby('Date')[['Weekly_Sales']].sum().reset_index()

# Create app
app = dash.Dash(__name__)

# Create figures
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=sales_data['Date'],
    y=sales_data['Weekly_Sales'],
    mode='lines+markers',
    name='Weekly Sales',
    line=dict(color='#667eea', width=3),
    marker=dict(size=8, color='#764ba2')
))
fig1.update_layout(
    title='Sales Over Time',
    xaxis_title='Date',
    yaxis_title='Weekly Sales ($)',
    template='plotly_white',
    height=400
)

fig2 = go.Figure()
fig2.add_trace(go.Histogram(
    x=sales_data['Weekly_Sales'],
    nbinsx=20,
    marker_color='#667eea',
    opacity=0.7
))
fig2.update_layout(
    title='Sales Distribution',
    xaxis_title='Sales Amount ($)',
    yaxis_title='Frequency',
    template='plotly_white',
    height=400
)

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Retail Sales Dashboard", style={
            'textAlign': 'center', 
            'color': 'white', 
            'padding': '30px',
            'margin': '0'
        }),
        html.P("Real-time Sales Analytics", style={
            'textAlign': 'center',
            'color': '#e0e0e0',
            'fontSize': '18px'
        })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'borderRadius': '0 0 20px 20px',
        'marginBottom': '30px'
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
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 20px'}),
    
    # Charts
    html.Div([
        dcc.Graph(figure=fig1)
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'margin': '20px'
    }),
    
    html.Div([
        dcc.Graph(figure=fig2)
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'margin': '20px'
    })
], style={'backgroundColor': '#f5f6fa', 'minHeight': '100vh'})

if __name__ == '__main__':
    print("🚀 Starting dashboard at http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
