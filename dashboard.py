import dash
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Helper function to convert hex to rgba
def hex_to_rgba(hex_color, alpha=0.2):
    """Convert hex color to rgba format"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

# Generate realistic business data
def generate_sales_data(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_trend = np.linspace(100, 150, 100)  # Upward trend
    seasonal = 10 * np.sin(2 * np.pi * np.arange(100) / 30)  # Monthly seasonality
    noise = np.random.normal(0, 5, 100)
    data = base_trend + seasonal + noise
    return time, data

def generate_website_traffic(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base = 5000 + np.linspace(0, 2000, 100)  # Growing traffic
    weekly_pattern = 1000 * np.sin(2 * np.pi * np.arange(100) / 7)  # Weekly pattern
    noise = np.random.normal(0, 200, 100)
    data = base + weekly_pattern + noise
    return time, data

def generate_conversion_rate(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_rate = 2.5 + np.linspace(0, 1, 100)  # Improving conversion
    weekly_variation = 0.5 * np.sin(2 * np.pi * np.arange(100) / 7)
    noise = np.random.normal(0, 0.2, 100)
    data = base_rate + weekly_variation + noise
    return time, data

def generate_customer_satisfaction(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_score = 4.2 + np.linspace(0, 0.3, 100)  # Improving satisfaction
    monthly_fluctuation = 0.1 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 0.05, 100)
    data = base_score + monthly_fluctuation + noise
    return time, data

app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
])

# Create meaningful charts with business context
charts_data = [
    {
        'title': 'Monthly Sales Performance',
        'subtitle': 'Revenue growth across all product lines',
        'data_func': generate_sales_data,
        'color': '#2563eb',
        'yaxis_title': 'Sales ($K)',
        'seed': 1
    },
    {
        'title': 'Website Traffic Analytics',
        'subtitle': 'Daily visitor engagement metrics',
        'data_func': generate_website_traffic,
        'color': '#059669',
        'yaxis_title': 'Visitors',
        'seed': 2
    },
    {
        'title': 'Conversion Rate Trends',
        'subtitle': 'Lead to customer conversion efficiency',
        'data_func': generate_conversion_rate,
        'color': '#dc2626',
        'yaxis_title': 'Conversion Rate (%)',
        'seed': 3
    },
    {
        'title': 'Customer Satisfaction Score',
        'subtitle': 'NPS and satisfaction survey results',
        'data_func': generate_customer_satisfaction,
        'color': '#7c3aed',
        'yaxis_title': 'Satisfaction Score',
        'seed': 4
    },
    {
        'title': 'Regional Sales Distribution',
        'subtitle': 'Performance by geographic markets',
        'data_func': generate_sales_data,
        'color': '#ea580c',
        'yaxis_title': 'Sales ($K)',
        'seed': 5
    },
    {
        'title': 'Marketing Campaign ROI',
        'subtitle': 'Return on marketing investment',
        'data_func': generate_conversion_rate,
        'color': '#0891b2',
        'yaxis_title': 'ROI (%)',
        'seed': 6
    },
    {
        'title': 'Product Performance Metrics',
        'subtitle': 'Top-selling product analytics',
        'data_func': generate_sales_data,
        'color': '#be185d',
        'yaxis_title': 'Units Sold',
        'seed': 7
    },
    {
        'title': 'Customer Retention Rate',
        'subtitle': 'Monthly customer loyalty metrics',
        'data_func': generate_customer_satisfaction,
        'color': '#16a34a',
        'yaxis_title': 'Retention Rate (%)',
        'seed': 8
    }
]

# Generate charts
charts = []
for i, chart_data in enumerate(charts_data):
    time, data = chart_data['data_func'](seed=chart_data['seed'])
    
    # Create the main line
    trace = go.Scatter(
        x=time, 
        y=data, 
        mode='lines+markers',
        name=chart_data['title'],
        line=dict(color=chart_data['color'], width=3),
        marker=dict(size=4, color=chart_data['color']),
        hovertemplate='<b>%{x}</b><br>' +
                     f'{chart_data["yaxis_title"]}: %{{y:.1f}}<extra></extra>'
    )
    
    # Add area fill
    area_trace = go.Scatter(
        x=time,
        y=data,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor=hex_to_rgba(chart_data['color'], 0.2),
        showlegend=False,
        hoverinfo='skip'
    )
    
    fig = go.Figure(data=[area_trace, trace])
    
    # Enhanced layout
    fig.update_layout(
        title=dict(
            text=chart_data['title'],
            font=dict(size=16, color='#1f2937', family='Inter'),
            x=0.05,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            zeroline=False,
            showline=True,
            linecolor='#d1d5db',
            linewidth=1,
            tickfont=dict(size=10, color='#6b7280'),
            title_font=dict(size=12, color='#374151')
        ),
        yaxis=dict(
            title=chart_data['yaxis_title'],
            title_font=dict(size=12, color='#374151'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            zeroline=False,
            showline=True,
            linecolor='#d1d5db',
            linewidth=1,
            tickfont=dict(size=10, color='#6b7280')
        ),
        margin=dict(l=50, r=20, t=60, b=50),
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='#d1d5db',
            font_size=12,
            font_family='Inter'
        )
    )
    
    charts.append(dcc.Graph(
        id=f'chart-{i+1}', 
        figure=fig,
        config={'displayModeBar': False}
    ))

# Create the grid layout
grid = []
for row in range(4):
    grid.append(html.Div([
        html.Div([
            html.H3(charts_data[row*2]['title'], 
                   style={'fontSize': '18px', 'fontWeight': '600', 'color': '#1f2937', 'margin': '0 0 8px 0'}),
            html.P(charts_data[row*2]['subtitle'], 
                  style={'fontSize': '12px', 'color': '#6b7280', 'margin': '0 0 16px 0'}),
            charts[row*2]
        ], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '20px', 'boxShadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1)'}),
        html.Div([
            html.H3(charts_data[row*2+1]['title'], 
                   style={'fontSize': '18px', 'fontWeight': '600', 'color': '#1f2937', 'margin': '0 0 8px 0'}),
            html.P(charts_data[row*2+1]['subtitle'], 
                  style={'fontSize': '12px', 'color': '#6b7280', 'margin': '0 0 16px 0'}),
            charts[row*2+1]
        ], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '20px', 'boxShadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1)'})
    ], style={'display': 'flex', 'gap': '24px', 'marginBottom': '24px'}))

# Main app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Business Analytics Dashboard', 
               style={'fontSize': '32px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 8px 0', 'fontFamily': 'Inter'}),
        html.P('Comprehensive overview of key business metrics and performance indicators', 
              style={'fontSize': '16px', 'color': '#6b7280', 'margin': '0 0 32px 0', 'fontFamily': 'Inter'}),
        html.Div([
            html.Span('Last Updated: ', style={'fontSize': '14px', 'color': '#6b7280'}),
            html.Span(datetime.now().strftime('%B %d, %Y at %I:%M %p'), 
                     style={'fontSize': '14px', 'fontWeight': '500', 'color': '#374151'})
        ], style={'marginBottom': '32px'})
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),
    
    # Dashboard content
    html.Div(grid, style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '0 20px'})
    
], style={
    'backgroundColor': '#f9fafb',
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif',
    'padding': '40px 0'
})

if __name__ == '__main__':
    app.run(debug=True)