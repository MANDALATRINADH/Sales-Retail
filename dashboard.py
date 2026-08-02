import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

# Load data
df = pd.read_csv('data/train.csv', parse_dates=['Date'])
sales_data = df.groupby('Date')[['Weekly_Sales']].sum().reset_index()

app.layout = html.Div([
    html.H1("📊 Retail Sales Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.Div([
        html.Div([
            html.H3("Total Sales", style={'textAlign': 'center'}),
            html.H2(f"", style={'color': '#3498db', 'textAlign': 'center'})
        ], className='metric-box'),
        html.Div([
            html.H3("Average Weekly Sales", style={'textAlign': 'center'}),
            html.H2(f"", style={'color': '#2ecc71', 'textAlign': 'center'})
        ], className='metric-box'),
        html.Div([
            html.H3("Max Weekly Sales", style={'textAlign': 'center'}),
            html.H2(f"", style={'color': '#e74c3c', 'textAlign': 'center'})
        ], className='metric-box')
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),
    dcc.Graph(
        id='sales-chart',
        figure={
            'data': [go.Scatter(x=sales_data['Date'], y=sales_data['Weekly_Sales'], mode='lines', name='Sales')],
            'layout': go.Layout(title='Sales Over Time', xaxis={'title': 'Date'}, yaxis={'title': 'Weekly Sales ($)'})
        }
    ),
    dcc.Graph(
        id='distribution',
        figure={
            'data': [go.Histogram(x=sales_data['Weekly_Sales'], nbinsx=30, name='Distribution')],
            'layout': go.Layout(title='Sales Distribution', xaxis={'title': 'Sales'}, yaxis={'title': 'Frequency'})
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
