from flask import Flask
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Generate realistic data
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=156, freq='W')
trend = np.linspace(10000, 20000, 156)
seasonal = 5000 * np.sin(np.arange(156) * 2 * np.pi / 52)
holiday = 3000 * np.sin(np.arange(156) * 2 * np.pi / 52 + 0.5)
noise = np.random.normal(0, 1000, 156)
sales = trend + seasonal + holiday + noise
sales = np.maximum(sales, 5000)

df = pd.DataFrame({
    'Date': dates,
    'Sales': sales,
    'Year': dates.year,
    'Month': dates.month,
    'Quarter': dates.quarter
})

# Metrics
total_sales = df['Sales'].sum()
avg_sales = df['Sales'].mean()
max_sales = df['Sales'].max()
growth = ((df['Sales'].iloc[-1] - df['Sales'].iloc[0]) / df['Sales'].iloc[0]) * 100

# Layout
app.layout = html.Div([
    html.Div([
        html.H1('📊 Sales Intelligence Platform', style={
            'textAlign': 'center', 'color': 'white', 'padding': '30px',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'borderRadius': '0 0 20px 20px', 'margin': '0'
        }),
        html.P('Interactive Analytics Dashboard', style={
            'textAlign': 'center', 'color': '#e0e0e0', 'fontSize': '18px'
        })
    ]),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.H4('💰 Total Revenue', style={'color': '#666'}),
            html.H2(f'', style={'color': '#2c3e50'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                  'flex': '1', 'margin': '10px', 'textAlign': 'center',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderLeft': '4px solid #3498db'}),
        
        html.Div([
            html.H4('📈 Average Weekly', style={'color': '#666'}),
            html.H2(f'', style={'color': '#2c3e50'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                  'flex': '1', 'margin': '10px', 'textAlign': 'center',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderLeft': '4px solid #2ecc71'}),
        
        html.Div([
            html.H4('📈 Growth Rate', style={'color': '#666'}),
            html.H2(f'{growth:.1f}%', style={'color': '#2c3e50'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                  'flex': '1', 'margin': '10px', 'textAlign': 'center',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderLeft': '4px solid #f39c12'}),
        
        html.Div([
            html.H4('🏆 Peak Sales', style={'color': '#666'}),
            html.H2(f'', style={'color': '#2c3e50'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                  'flex': '1', 'margin': '10px', 'textAlign': 'center',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'borderLeft': '4px solid #e74c3c'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '20px'}),

    # Filters
    html.Div([
        html.Div([
            html.Label('📅 Year', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())],
                value=None,
                placeholder='All Years',
                style={'width': '150px'}
            )
        ], style={'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label('📊 Quarter', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='quarter-filter',
                options=[{'label': f'Q{q}', 'value': q} for q in range(1, 5)],
                value=None,
                placeholder='All Quarters',
                style={'width': '150px'}
            )
        ], style={'display': 'inline-block'})
    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'margin': '20px'}),

    # Charts
    html.Div([
        dcc.Graph(id='main-chart')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'margin': '20px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='distribution-chart')
        ], style={'flex': '1', 'margin': '10px'}),
        html.Div([
            dcc.Graph(id='heatmap-chart')
        ], style={'flex': '1', 'margin': '10px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 10px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='boxplot-chart')
        ], style={'flex': '1', 'margin': '10px'}),
        html.Div([
            dcc.Graph(id='forecast-chart')
        ], style={'flex': '1', 'margin': '10px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 10px 20px 10px'})
], style={'backgroundColor': '#f5f6fa', 'minHeight': '100vh'})

# Callbacks
@app.callback(
    [Output('main-chart', 'figure'),
     Output('distribution-chart', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('boxplot-chart', 'figure'),
     Output('forecast-chart', 'figure')],
    [Input('year-filter', 'value'),
     Input('quarter-filter', 'value')]
)
def update_charts(selected_year, selected_quarter):
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_quarter:
        filtered_df = filtered_df[filtered_df['Quarter'] == selected_quarter]
    
    # Main Chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6, color='#764ba2')
    ))
    fig1.update_layout(
        title='📊 Sales Performance',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        template='plotly_white',
        height=400
    )
    
    # Distribution
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(
        x=filtered_df['Sales'],
        nbinsx=25,
        marker_color='#667eea',
        opacity=0.7
    ))
    fig2.update_layout(
        title='📊 Sales Distribution',
        xaxis_title='Sales ($)',
        yaxis_title='Frequency',
        template='plotly_white',
        height=400
    )
    
    # Heatmap
    heatmap_data = filtered_df.pivot_table(
        values='Sales',
        index='Year',
        columns='Month',
        aggfunc='mean'
    )
    fig3 = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        y=heatmap_data.index,
        colorscale='Viridis'
    ))
    fig3.update_layout(
        title='🌡️ Monthly Sales Heatmap',
        xaxis_title='Month',
        yaxis_title='Year',
        template='plotly_white',
        height=400
    )
    
    # Box Plot
    fig4 = go.Figure()
    for year in filtered_df['Year'].unique():
        yearly_data = filtered_df[filtered_df['Year'] == year]
        fig4.add_trace(go.Box(
            y=yearly_data['Sales'],
            name=str(year),
            boxmean='sd'
        ))
    fig4.update_layout(
        title='📦 Year-over-Year Comparison',
        xaxis_title='Year',
        yaxis_title='Sales ($)',
        template='plotly_white',
        height=400
    )
    
    # Forecast
    if len(filtered_df) >= 52:
        last_year = filtered_df.tail(52)
        forecast = last_year['Sales'].values
        future_dates = pd.date_range(
            start=filtered_df['Date'].max() + timedelta(days=7),
            periods=13,
            freq='W'
        )
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Sales'],
            mode='lines',
            name='Historical',
            line=dict(color='#667eea', width=2)
        ))
        fig5.add_trace(go.Scatter(
            x=future_dates,
            y=forecast[-13:],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#4ade80', width=2, dash='dash'),
            marker=dict(size=8, color='#4ade80')
        ))
        fig5.update_layout(
            title='🔮 13-Week Forecast',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            template='plotly_white',
            height=400
        )
    
    return fig1, fig2, fig3, fig4, fig5

application = app.server

if __name__ == '__main__':
    application.run(debug=True, port=8050)
