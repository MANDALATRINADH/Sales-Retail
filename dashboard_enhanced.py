import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize app
app = dash.Dash(__name__, title="Retail Sales Dashboard")

# Load data
df = pd.read_csv('data/train.csv', parse_dates=['Date'])
sales_data = df.groupby('Date')[['Weekly_Sales']].sum().reset_index()

# Add date features for filtering
sales_data['Year'] = sales_data['Date'].dt.year
sales_data['Month'] = sales_data['Date'].dt.month
sales_data['Quarter'] = sales_data['Date'].dt.quarter
sales_data['DayOfWeek'] = sales_data['Date'].dt.day_name()
sales_data['Week'] = sales_data['Date'].dt.isocalendar().week

# Calculate metrics
total_sales = sales_data['Weekly_Sales'].sum()
avg_sales = sales_data['Weekly_Sales'].mean()
max_sales = sales_data['Weekly_Sales'].max()
min_sales = sales_data['Weekly_Sales'].min()
sales_growth = ((sales_data['Weekly_Sales'].iloc[-1] - sales_data['Weekly_Sales'].iloc[0]) / sales_data['Weekly_Sales'].iloc[0]) * 100

# App layout with modern styling
app.layout = html.Div([
    # Header with gradient background
    html.Div([
        html.H1("📊 Retail Sales Intelligence Dashboard", 
                style={'textAlign': 'center', 'color': 'white', 'padding': '30px 0', 'margin': 0}),
        html.P("Real-time Sales Analytics & Forecasting", 
               style={'textAlign': 'center', 'color': '#e0e0e0', 'fontSize': '18px'})
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'borderRadius': '0 0 30px 30px',
        'marginBottom': '30px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    }),
    
    # Filters Section
    html.Div([
        html.Div([
            html.Label("Select Year:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': str(year), 'value': year} for year in sales_data['Year'].unique()],
                value=None,
                placeholder="All Years",
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block', 'marginRight': '30px'}),
        
        html.Div([
            html.Label("Select Quarter:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='quarter-filter',
                options=[{'label': f'Q{q}', 'value': q} for q in range(1, 5)],
                value=None,
                placeholder="All Quarters",
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block'})
    ], style={
        'padding': '20px', 
        'backgroundColor': 'white', 
        'borderRadius': '10px',
        'margin': '0 20px 20px 20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.Div([
                html.H4("💰 Total Revenue", style={'margin': '0', 'color': '#666'}),
                html.H2(f"", style={'margin': '10px 0', 'color': '#2c3e50'}),
                html.P(f" avg per week", style={'margin': '0', 'color': '#95a5a6'})
            ], style={'padding': '20px'})
        ], className='kpi-card', style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'borderLeft': '4px solid #3498db'
        }),
        
        html.Div([
            html.Div([
                html.H4("📈 Average Sales", style={'margin': '0', 'color': '#666'}),
                html.H2(f"", style={'margin': '10px 0', 'color': '#2c3e50'}),
                html.P(f"per week", style={'margin': '0', 'color': '#95a5a6'})
            ], style={'padding': '20px'})
        ], className='kpi-card', style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'borderLeft': '4px solid #2ecc71'
        }),
        
        html.Div([
            html.Div([
                html.H4("📊 Sales Range", style={'margin': '0', 'color': '#666'}),
                html.H2(f" - ", style={'margin': '10px 0', 'color': '#2c3e50'}),
                html.P(f"min - max weekly sales", style={'margin': '0', 'color': '#95a5a6'})
            ], style={'padding': '20px'})
        ], className='kpi-card', style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'borderLeft': '4px solid #e74c3c'
        }),
        
        html.Div([
            html.Div([
                html.H4("📈 Growth Rate", style={'margin': '0', 'color': '#666'}),
                html.H2(f"{sales_growth:.1f}%", style={'margin': '10px 0', 'color': '#2c3e50'}),
                html.P(f"over entire period", style={'margin': '0', 'color': '#95a5a6'})
            ], style={'padding': '20px'})
        ], className='kpi-card', style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1',
            'margin': '10px',
            'borderLeft': '4px solid #f39c12'
        })
    ], style={
        'display': 'flex', 
        'flexWrap': 'wrap', 
        'margin': '0 20px 20px 20px'
    }),
    
    # Main Charts
    html.Div([
        # Time Series Chart
        html.Div([
            dcc.Graph(id='sales-chart')
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'margin': '10px',
            'flex': '2'
        }),
        
        # Weekly Pattern
        html.Div([
            dcc.Graph(id='weekly-pattern')
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'margin': '10px',
            'flex': '1'
        })
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 20px'}),
    
    # Bottom Charts
    html.Div([
        html.Div([
            dcc.Graph(id='distribution-chart')
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'margin': '10px',
            'flex': '1'
        }),
        
        html.Div([
            dcc.Graph(id='monthly-heatmap')
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'margin': '10px',
            'flex': '1'
        })
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 20px 20px 20px'}),
    
    # Footer
    html.Div([
        html.P("Built with Dash • Data updated in real-time", 
               style={'textAlign': 'center', 'color': '#95a5a6', 'padding': '20px 0'})
    ])
], style={'backgroundColor': '#f5f6fa', 'minHeight': '100vh'})

# Callbacks for interactivity
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('weekly-pattern', 'figure'),
     Output('distribution-chart', 'figure'),
     Output('monthly-heatmap', 'figure')],
    [Input('year-filter', 'value'),
     Input('quarter-filter', 'value')]
)
def update_charts(selected_year, selected_quarter):
    # Filter data
    filtered_data = sales_data.copy()
    
    if selected_year:
        filtered_data = filtered_data[filtered_data['Year'] == selected_year]
    
    if selected_quarter:
        filtered_data = filtered_data[filtered_data['Quarter'] == selected_quarter]
    
    # 1. Time Series Chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_data['Date'],
        y=filtered_data['Weekly_Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='#667eea', width=2),
        marker=dict(size=6, color='#764ba2')
    ))
    fig1.update_layout(
        title='Sales Over Time',
        xaxis_title='Date',
        yaxis_title='Weekly Sales ($)',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    # 2. Weekly Pattern (Day of Week)
    weekly_avg = filtered_data.groupby('DayOfWeek')['Weekly_Sales'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=weekly_avg.index,
        y=weekly_avg.values,
        marker_color=['#667eea', '#764ba2', '#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#95a5a6']
    ))
    fig2.update_layout(
        title='Average Sales by Day',
        xaxis_title='Day of Week',
        yaxis_title='Avg Sales ($)',
        template='plotly_white',
        height=400
    )
    
    # 3. Distribution Chart
    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=filtered_data['Weekly_Sales'],
        nbinsx=30,
        marker_color='#667eea',
        opacity=0.7
    ))
    fig3.add_trace(go.Violin(
        y=filtered_data['Weekly_Sales'],
        box_visible=True,
        line_color='#764ba2',
        name='Distribution',
        side='positive'
    ))
    fig3.update_layout(
        title='Sales Distribution',
        xaxis_title='Sales ($)',
        yaxis_title='Frequency',
        template='plotly_white',
        height=400
    )
    
    # 4. Monthly Heatmap
    monthly_data = filtered_data.groupby(['Year', 'Month'])['Weekly_Sales'].mean().reset_index()
    pivot_data = monthly_data.pivot(index='Year', columns='Month', values='Weekly_Sales')
    
    fig4 = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        text=pivot_data.values,
        texttemplate='',
        textfont={"size": 10},
        hoverongaps=False
    ))
    fig4.update_layout(
        title='Monthly Sales Heatmap',
        xaxis_title='Month',
        yaxis_title='Year',
        template='plotly_white',
        height=400,
        xaxis={'dtick': 1},
        yaxis={'dtick': 1}
    )
    
    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run(debug=True, port=8050)
