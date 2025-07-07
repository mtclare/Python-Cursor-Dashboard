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

# Generate enhanced business data with more realistic trends
def generate_sales_data(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_trend = np.linspace(120, 180, 100)  # Stronger upward trend
    seasonal = 15 * np.sin(2 * np.pi * np.arange(100) / 30)  # Enhanced seasonality
    noise = np.random.normal(0, 8, 100)
    data = base_trend + seasonal + noise
    return time, data

def generate_website_traffic(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base = 6000 + np.linspace(0, 3000, 100)  # Higher growth
    weekly_pattern = 1200 * np.sin(2 * np.pi * np.arange(100) / 7)
    noise = np.random.normal(0, 300, 100)
    data = base + weekly_pattern + noise
    return time, data

def generate_conversion_rate(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_rate = 3.2 + np.linspace(0, 1.5, 100)  # Higher conversion rates
    weekly_variation = 0.8 * np.sin(2 * np.pi * np.arange(100) / 7)
    noise = np.random.normal(0, 0.3, 100)
    data = base_rate + weekly_variation + noise
    return time, data

def generate_customer_satisfaction(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_score = 4.4 + np.linspace(0, 0.4, 100)  # Higher satisfaction
    monthly_fluctuation = 0.15 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 0.08, 100)
    data = base_score + monthly_fluctuation + noise
    return time, data

def generate_revenue_data(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_trend = np.linspace(500, 850, 100)  # Revenue in millions
    seasonal = 25 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 15, 100)
    data = base_trend + seasonal + noise
    return time, data

def generate_profit_margins(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_margin = 18 + np.linspace(0, 5, 100)  # Improving margins
    seasonal = 2 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 1, 100)
    data = base_margin + seasonal + noise
    return time, data

app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
])
server = app.server

# Executive summary metrics
summary_metrics = [
    {
        'title': 'Total Revenue',
        'value': '$847.2M',
        'change': '+12.4%',
        'trend': 'up',
        'color': '#1e40af',
        'icon': '📈'
    },
    {
        'title': 'Profit Margin',
        'value': '23.1%',
        'change': '+2.8%',
        'trend': 'up',
        'color': '#059669',
        'icon': '💰'
    },
    {
        'title': 'Customer Growth',
        'value': '+18.7%',
        'change': '+3.2%',
        'trend': 'up',
        'color': '#dc2626',
        'icon': '👥'
    },
    {
        'title': 'Market Share',
        'value': '34.2%',
        'change': '+1.5%',
        'trend': 'up',
        'color': '#7c3aed',
        'icon': '🎯'
    }
]

# Enhanced charts data with professional color scheme
charts_data = [
    {
        'title': 'Revenue Performance',
        'subtitle': 'Monthly revenue growth and trend analysis',
        'data_func': generate_revenue_data,
        'color': '#1e40af',
        'yaxis_title': 'Revenue ($M)',
        'seed': 1
    },
    {
        'title': 'Profit Margin Trends',
        'subtitle': 'Operational efficiency and cost management',
        'data_func': generate_profit_margins,
        'color': '#059669',
        'yaxis_title': 'Margin (%)',
        'seed': 2
    },
    {
        'title': 'Customer Acquisition',
        'subtitle': 'New customer growth and retention metrics',
        'data_func': generate_website_traffic,
        'color': '#dc2626',
        'yaxis_title': 'New Customers',
        'seed': 3
    },
    {
        'title': 'Customer Satisfaction',
        'subtitle': 'NPS scores and customer experience metrics',
        'data_func': generate_customer_satisfaction,
        'color': '#7c3aed',
        'yaxis_title': 'Satisfaction Score',
        'seed': 4
    },
    {
        'title': 'Sales Performance',
        'subtitle': 'Regional sales distribution and growth',
        'data_func': generate_sales_data,
        'color': '#ea580c',
        'yaxis_title': 'Sales ($K)',
        'seed': 5
    },
    {
        'title': 'Conversion Optimization',
        'subtitle': 'Lead to customer conversion efficiency',
        'data_func': generate_conversion_rate,
        'color': '#0891b2',
        'yaxis_title': 'Conversion Rate (%)',
        'seed': 6
    },
    {
        'title': 'Product Performance',
        'subtitle': 'Top-selling product line analytics',
        'data_func': generate_sales_data,
        'color': '#be185d',
        'yaxis_title': 'Units Sold',
        'seed': 7
    },
    {
        'title': 'Market Expansion',
        'subtitle': 'Geographic market penetration rates',
        'data_func': generate_customer_satisfaction,
        'color': '#16a34a',
        'yaxis_title': 'Market Share (%)',
        'seed': 8
    }
]

# Generate enhanced charts
charts = []
for i, chart_data in enumerate(charts_data):
    time, data = chart_data['data_func'](seed=chart_data['seed'])
    
    # Create the main line with enhanced styling
    trace = go.Scatter(
        x=time, 
        y=data, 
        mode='lines+markers',
        name=chart_data['title'],
        line=dict(color=chart_data['color'], width=4),
        marker=dict(size=6, color=chart_data['color']),
        hovertemplate='<b>%{x|%B %d, %Y}</b><br>' +
                     f'{chart_data["yaxis_title"]}: %{{y:,.1f}}<extra></extra>'
    )
    
    # Add area fill with enhanced opacity
    area_trace = go.Scatter(
        x=time,
        y=data,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor=hex_to_rgba(chart_data['color'], 0.15),
        showlegend=False,
        hoverinfo='skip'
    )
    
    fig = go.Figure(data=[area_trace, trace])
    
    # Enhanced professional layout
    fig.update_layout(
        title=dict(
            text=chart_data['title'],
            font=dict(size=20, color='#1f2937', family='Inter'),
            x=0.05,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            zeroline=False,
            showline=True,
            linecolor='#d1d5db',
            linewidth=1,
            tickfont=dict(size=12, color='#6b7280'),
            title_font=dict(size=14, color='#374151')
        ),
        yaxis=dict(
            title=chart_data['yaxis_title'],
            title_font=dict(size=14, color='#374151'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            zeroline=False,
            showline=True,
            linecolor='#d1d5db',
            linewidth=1,
            tickfont=dict(size=12, color='#6b7280')
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='#d1d5db',
            font_size=13,
            font_family='Inter'
        )
    )
    
    charts.append(dcc.Graph(
        id=f'chart-{i+1}', 
        figure=fig,
        config={'displayModeBar': False}
    ))

# Create executive summary cards
summary_cards = []
for metric in summary_metrics:
    trend_color = '#059669' if metric['trend'] == 'up' else '#dc2626'
    trend_arrow = '↗️' if metric['trend'] == 'up' else '↘️'
    
    summary_cards.append(html.Div([
        html.Div([
            html.Span(metric['icon'], style={'fontSize': '24px', 'marginRight': '12px'}),
            html.Div([
                html.H3(metric['title'], 
                       style={'fontSize': '14px', 'fontWeight': '500', 'color': '#6b7280', 'margin': '0 0 4px 0'}),
                html.H2(metric['value'], 
                       style={'fontSize': '28px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 4px 0'}),
                html.Div([
                    html.Span(trend_arrow, style={'fontSize': '14px', 'marginRight': '4px'}),
                    html.Span(metric['change'], 
                             style={'fontSize': '14px', 'fontWeight': '600', 'color': trend_color})
                ])
            ])
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '16px',
        'padding': '24px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'border': f'2px solid {metric["color"]}20',
        'flex': '1'
    }))

# Create the enhanced grid layout
grid = []
for row in range(4):
    grid.append(html.Div([
        html.Div([
            html.H3(charts_data[row*2]['title'], 
                   style={'fontSize': '20px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 8px 0'}),
            html.P(charts_data[row*2]['subtitle'], 
                  style={'fontSize': '14px', 'color': '#6b7280', 'margin': '0 0 20px 0', 'lineHeight': '1.5'}),
            charts[row*2]
        ], style={
            'flex': '1', 
            'backgroundColor': 'white', 
            'borderRadius': '16px', 
            'padding': '28px', 
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'border': '1px solid #e5e7eb'
        }),
        html.Div([
            html.H3(charts_data[row*2+1]['title'], 
                   style={'fontSize': '20px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 8px 0'}),
            html.P(charts_data[row*2+1]['subtitle'], 
                  style={'fontSize': '14px', 'color': '#6b7280', 'margin': '0 0 20px 0', 'lineHeight': '1.5'}),
            charts[row*2+1]
        ], style={
            'flex': '1', 
            'backgroundColor': 'white', 
            'borderRadius': '16px', 
            'padding': '28px', 
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'border': '1px solid #e5e7eb'
        })
    ], style={'display': 'flex', 'gap': '32px', 'marginBottom': '32px'}))

# Enhanced main app layout
app.layout = html.Div([
    # Professional header with gradient
    html.Div([
        html.Div([
            html.H1('Executive Business Dashboard', 
                   style={'fontSize': '40px', 'fontWeight': '800', 'color': 'white', 'margin': '0 0 12px 0', 'fontFamily': 'Inter'}),
            html.P('Q4 2023 Performance Review - Board Meeting', 
                  style={'fontSize': '18px', 'color': '#e5e7eb', 'margin': '0 0 16px 0', 'fontFamily': 'Inter'}),
            html.Div([
                html.Span('Prepared by: Executive Analytics Team', 
                         style={'fontSize': '14px', 'color': '#d1d5db', 'marginRight': '24px'}),
                html.Span('Board Meeting: December 15, 2023', 
                         style={'fontSize': '14px', 'color': '#d1d5db'})
            ])
        ], style={'textAlign': 'center', 'padding': '40px 0'})
    ], style={
        'background': 'linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)',
        'marginBottom': '40px',
        'borderRadius': '0 0 20px 20px'
    }),
    
    # Executive summary section
    html.Div([
        html.H2('Key Performance Indicators', 
               style={'fontSize': '24px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 24px 0', 'textAlign': 'center'}),
        html.Div(summary_cards, style={'display': 'flex', 'gap': '24px', 'marginBottom': '48px'})
    ], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '0 20px'}),
    
    # Dashboard content
    html.Div(grid, style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '0 20px'}),
    
    # Professional footer
    html.Div([
        html.Div([
            html.Span('Data Source: Enterprise Analytics Platform', 
                     style={'fontSize': '12px', 'color': '#6b7280', 'marginRight': '24px'}),
            html.Span(f'Last Updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', 
                     style={'fontSize': '12px', 'color': '#6b7280', 'marginRight': '24px'}),
            html.Span('Confidential - Board Use Only', 
                     style={'fontSize': '12px', 'color': '#dc2626', 'fontWeight': '600'})
        ], style={'textAlign': 'center', 'padding': '20px 0', 'borderTop': '1px solid #e5e7eb'})
    ], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '0 20px'})
    
], style={
    'backgroundColor': '#f8fafc',
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif',
    'padding': '0 0 40px 0'
})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8050')