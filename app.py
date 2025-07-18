import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
from color_palette import (
    COLOR_PALETTE, CATEGORICAL_PALETTE, SEQUENTIAL_SCALES, DIVERGING_SCALES,
    hex_to_rgba, get_chart_colors, CHART_THEME, DEFAULT_CHART_CONFIG,
    is_accessible, get_accessible_variant
)
from filters import (
    create_date_range_filter, create_category_filter, create_range_slider,
    create_filter_panel, create_active_filters_display, create_filter_tag
)

# Generate enhanced business data with more realistic trends
def generate_sales_data(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base_trend = np.linspace(120, 180, periods)  # Stronger upward trend
    seasonal = 15 * np.sin(2 * np.pi * np.arange(periods) / 30)  # Enhanced seasonality
    noise = np.random.normal(0, 8, periods)
    data = base_trend + seasonal + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'category': np.random.choice(['Product A', 'Product B', 'Product C'], size=periods),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'category' in categories:
        df = df[df['category'].isin(categories['category'])]
    if categories is not None and 'region' in categories:
        df = df[df['region'].isin(categories['region'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

def generate_website_traffic(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base = 6000 + np.linspace(0, 3000, periods)  # Higher growth
    weekly_pattern = 1200 * np.sin(2 * np.pi * np.arange(periods) / 7)
    noise = np.random.normal(0, 300, periods)
    data = base + weekly_pattern + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'source': np.random.choice(['Organic', 'Direct', 'Social', 'Referral'], size=periods),
        'device': np.random.choice(['Desktop', 'Mobile', 'Tablet'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'source' in categories:
        df = df[df['source'].isin(categories['source'])]
    if categories is not None and 'device' in categories:
        df = df[df['device'].isin(categories['device'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

def generate_conversion_rate(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base_rate = 3.2 + np.linspace(0, 1.5, periods)  # Higher conversion rates
    weekly_variation = 0.8 * np.sin(2 * np.pi * np.arange(periods) / 7)
    noise = np.random.normal(0, 0.3, periods)
    data = base_rate + weekly_variation + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'channel': np.random.choice(['Email', 'Social', 'Search', 'Direct'], size=periods),
        'campaign': np.random.choice(['Spring', 'Summer', 'Fall', 'Winter'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'channel' in categories:
        df = df[df['channel'].isin(categories['channel'])]
    if categories is not None and 'campaign' in categories:
        df = df[df['campaign'].isin(categories['campaign'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

def generate_customer_satisfaction(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base_score = 4.4 + np.linspace(0, 0.4, periods)  # Higher satisfaction
    monthly_fluctuation = 0.15 * np.sin(2 * np.pi * np.arange(periods) / 30)
    noise = np.random.normal(0, 0.08, periods)
    data = base_score + monthly_fluctuation + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'segment': np.random.choice(['New', 'Returning', 'Premium'], size=periods),
        'product': np.random.choice(['Product A', 'Product B', 'Product C'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'segment' in categories:
        df = df[df['segment'].isin(categories['segment'])]
    if categories is not None and 'product' in categories:
        df = df[df['product'].isin(categories['product'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

def generate_revenue_data(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base_trend = np.linspace(500, 850, periods)  # Revenue in millions
    seasonal = 25 * np.sin(2 * np.pi * np.arange(periods) / 30)
    noise = np.random.normal(0, 15, periods)
    data = base_trend + seasonal + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'division': np.random.choice(['Retail', 'Enterprise', 'SMB'], size=periods),
        'region': np.random.choice(['North America', 'Europe', 'Asia', 'Other'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'division' in categories:
        df = df[df['division'].isin(categories['division'])]
    if categories is not None and 'region' in categories:
        df = df[df['region'].isin(categories['region'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

def generate_profit_margins(seed=0, start_date=None, end_date=None, categories=None, value_range=None):
    np.random.seed(seed)
    
    # Default date range if not specified
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = '2023-04-10'  # 100 days from start
    
    # Generate time series
    time = pd.date_range(start=start_date, end=end_date, freq='D')
    periods = len(time)
    
    # Generate base data
    base_margin = 18 + np.linspace(0, 5, periods)  # Improving margins
    seasonal = 2 * np.sin(2 * np.pi * np.arange(periods) / 30)
    noise = np.random.normal(0, 1, periods)
    data = base_margin + seasonal + noise
    
    # Apply value range filter if specified
    if value_range is not None:
        min_val, max_val = value_range
        data = np.clip(data, min_val, max_val)
    
    # Create DataFrame for easier filtering
    df = pd.DataFrame({
        'date': time,
        'value': data,
        'product_line': np.random.choice(['Hardware', 'Software', 'Services'], size=periods),
        'market': np.random.choice(['Consumer', 'Business', 'Government'], size=periods)
    })
    
    # Apply category filter if specified
    if categories is not None and 'product_line' in categories:
        df = df[df['product_line'].isin(categories['product_line'])]
    if categories is not None and 'market' in categories:
        df = df[df['market'].isin(categories['market'])]
    
    # Return filtered time and data
    return df['date'].values, df['value'].values

app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
])

# Add custom CSS for animations and effects
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .kpi-card {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
            }
            
            /* Filter component styling */
            .custom-range-slider .rc-slider-track {
                background-color: #3b82f6;
            }
            
            .custom-range-slider .rc-slider-handle {
                border-color: #3b82f6;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .custom-range-slider .rc-slider-handle:hover,
            .custom-range-slider .rc-slider-handle:active {
                border-color: #1e40af;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }
            
            /* Dropdown styling */
            .Select-control {
                border-color: #e5e7eb !important;
                border-radius: 6px !important;
            }
            
            .Select-control:hover {
                border-color: #d1d5db !important;
            }
            
            .is-focused:not(.is-open) > .Select-control {
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 1px #3b82f6 !important;
            }
            
            /* Date picker styling */
            .DateInput_input {
                font-family: 'Inter', sans-serif !important;
                font-size: 14px !important;
                border-radius: 4px !important;
            }
            
            .DateRangePickerInput {
                border-radius: 6px !important;
                border-color: #e5e7eb !important;
            }
            
            .DateRangePickerInput:hover {
                border-color: #d1d5db !important;
            }
            
            .CalendarDay__selected, 
            .CalendarDay__selected:hover {
                background: #3b82f6 !important;
                border: 1px double #3b82f6 !important;
            }
            
            .CalendarDay__selected_span {
                background: #93c5fd !important;
                border: 1px double #93c5fd !important;
                color: #1e3a8a !important;
            }
            
            .CalendarDay__hovered_span, 
            .CalendarDay__hovered_span:hover {
                background: #dbeafe !important;
                border: 1px double #dbeafe !important;
                color: #1e3a8a !important;
            }
            
            /* Button hover effects */
            #apply-filters-button:hover {
                background-color: #2563eb;
                transform: translateY(-1px);
                box-shadow: 0 6px 10px -2px rgba(59, 130, 246, 0.3);
            }
            
            #reset-filters-button:hover {
                background-color: rgba(59, 130, 246, 0.1);
            }
            
            /* Filter tag animations */
            #active-filters-content > div {
                animation: fadeIn 0.3s ease-in-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-5px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Smooth transitions for all interactive elements */
            button, .Select-control, .DateRangePickerInput, .rc-slider-handle {
                transition: all 0.2s ease-in-out;
            }
            
            @media (prefers-reduced-motion: reduce) {
                .kpi-card, .kpi-card:hover {
                    transition: none;
                    transform: none;
                }
                
                @keyframes gradientShift {
                    0%, 50%, 100% { background-position: 0% 50%; }
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
server = app.server

# Generate sparkline data for KPI cards
def generate_sparkline_data(seed=0, points=20, trend='up'):
    np.random.seed(seed)
    if trend == 'up':
        base = np.linspace(10, 20, points)
        noise = np.random.normal(0, 1, points)
    else:
        base = np.linspace(20, 10, points)
        noise = np.random.normal(0, 1, points)
    return base + noise

# Executive summary metrics with colors from our palette
summary_metrics = [
    {
        'title': 'Total Revenue',
        'value': '$847.2M',
        'change': '+12.4%',
        'trend': 'up',
        'color': COLOR_PALETTE['primary'][0],  # Deep blue
        'icon': '📈',
        'sparkline_data': generate_sparkline_data(seed=42, trend='up')
    },
    {
        'title': 'Profit Margin',
        'value': '23.1%',
        'change': '+2.8%',
        'trend': 'up',
        'color': COLOR_PALETTE['secondary'][0],  # Green
        'icon': '💰',
        'sparkline_data': generate_sparkline_data(seed=43, trend='up')
    },
    {
        'title': 'Customer Growth',
        'value': '+18.7%',
        'change': '+3.2%',
        'trend': 'up',
        'color': COLOR_PALETTE['accent'][0],  # Red
        'icon': '👥',
        'sparkline_data': generate_sparkline_data(seed=44, trend='up')
    },
    {
        'title': 'Market Share',
        'value': '34.2%',
        'change': '+1.5%',
        'trend': 'up',
        'color': COLOR_PALETTE['primary'][3],  # Purple
        'icon': '🎯',
        'sparkline_data': generate_sparkline_data(seed=45, trend='up')
    }
]

# Enhanced charts data with accessible color palette
# Using categorical palette for consistent and accessible colors
chart_colors = get_chart_colors(8, 'categorical')

charts_data = [
    {
        'title': 'Revenue Performance',
        'subtitle': 'Monthly revenue growth and trend analysis',
        'data_func': generate_revenue_data,
        'color': chart_colors[0],  # Primary blue
        'yaxis_title': 'Revenue ($M)',
        'seed': 1
    },
    {
        'title': 'Profit Margin Trends',
        'subtitle': 'Operational efficiency and cost management',
        'data_func': generate_profit_margins,
        'color': chart_colors[1],  # Secondary green
        'yaxis_title': 'Margin (%)',
        'seed': 2
    },
    {
        'title': 'Customer Acquisition',
        'subtitle': 'New customer growth and retention metrics',
        'data_func': generate_website_traffic,
        'color': chart_colors[2],  # Accent red
        'yaxis_title': 'New Customers',
        'seed': 3
    },
    {
        'title': 'Customer Satisfaction',
        'subtitle': 'NPS scores and customer experience metrics',
        'data_func': generate_customer_satisfaction,
        'color': chart_colors[3],  # Purple
        'yaxis_title': 'Satisfaction Score',
        'seed': 4
    },
    {
        'title': 'Sales Performance',
        'subtitle': 'Regional sales distribution and growth',
        'data_func': generate_sales_data,
        'color': chart_colors[4],  # Orange
        'yaxis_title': 'Sales ($K)',
        'seed': 5
    },
    {
        'title': 'Conversion Optimization',
        'subtitle': 'Lead to customer conversion efficiency',
        'data_func': generate_conversion_rate,
        'color': chart_colors[5],  # Cyan
        'yaxis_title': 'Conversion Rate (%)',
        'seed': 6
    },
    {
        'title': 'Product Performance',
        'subtitle': 'Top-selling product line analytics',
        'data_func': generate_sales_data,
        'color': chart_colors[6],  # Pink
        'yaxis_title': 'Units Sold',
        'seed': 7
    },
    {
        'title': 'Market Expansion',
        'subtitle': 'Geographic market penetration rates',
        'data_func': generate_customer_satisfaction,
        'color': chart_colors[7],  # Green
        'yaxis_title': 'Market Share (%)',
        'seed': 8
    }
]

# Verify color accessibility and adjust if needed
for chart in charts_data:
    # Check if color is accessible on white background (chart background)
    if not is_accessible(chart['color'], CHART_THEME['background'], 'AA'):
        # Get an accessible variant of the color
        chart['color'] = get_accessible_variant(chart['color'], CHART_THEME['background'], 'AA')

# Generate enhanced charts
charts = []
for i, chart_data in enumerate(charts_data):
    time, data = chart_data['data_func'](seed=chart_data['seed'])
    
    # Create the main line with enhanced styling and improved tooltips
    
    # Calculate additional metrics for contextual information in tooltips
    # For example, calculate percent change from previous point
    pct_change = []
    for i in range(len(data)):
        if i == 0:
            pct_change.append(0)
        else:
            change = ((data[i] - data[i-1]) / data[i-1]) * 100 if data[i-1] != 0 else 0
            pct_change.append(change)
    
    # Format the tooltip with more contextual information
    hover_text = []
    for i, (t, val, pct) in enumerate(zip(time, data, pct_change)):
        # Convert numpy.datetime64 to pandas Timestamp for strftime
        if isinstance(t, np.datetime64):
            t = pd.Timestamp(t)
            
        # Format the value based on the type of data
        if "Revenue" in chart_data["yaxis_title"] or "Sales" in chart_data["yaxis_title"]:
            formatted_val = f"${val:,.1f}M"
        elif "%" in chart_data["yaxis_title"]:
            formatted_val = f"{val:.2f}%"
        elif "Score" in chart_data["yaxis_title"]:
            formatted_val = f"{val:.2f}/5.0"
        else:
            formatted_val = f"{val:,.1f}"
        
        # Add trend indicator and contextual information
        if i > 0:
            trend = "▲" if pct > 0 else "▼" if pct < 0 else "◆"
            trend_color = COLOR_PALETTE['secondary'][0] if pct > 0 else COLOR_PALETTE['accent'][0] if pct < 0 else "#6b7280"
            
            # Add period-over-period comparison
            if i >= 7:  # If we have enough data for week-over-week
                wow_change = ((val - data[i-7]) / data[i-7]) * 100 if data[i-7] != 0 else 0
                wow_text = f"WoW: {wow_change:+.1f}%"
            else:
                wow_text = ""
                
            hover_text.append(
                f"<b>{t.strftime('%B %d, %Y')}</b><br>" +
                f"<b>{chart_data['yaxis_title']}:</b> {formatted_val}<br>" +
                f"<span style='color:{trend_color}'>{trend} {pct:+.1f}% from previous day</span><br>" +
                (f"{wow_text}" if wow_text else "")
            )
        else:
            hover_text.append(
                f"<b>{t.strftime('%B %d, %Y')}</b><br>" +
                f"<b>{chart_data['yaxis_title']}:</b> {formatted_val}"
            )
    
    trace = go.Scatter(
        x=time, 
        y=data, 
        mode='lines+markers',
        name=chart_data['title'],
        line=dict(
            color=chart_data['color'], 
            width=4,
            shape='spline',  # Smoother line transitions
            smoothing=1.3    # Enhance smoothing
        ),
        marker=dict(
            size=6, 
            color=chart_data['color'],
            line=dict(width=1, color='white')  # Add white border to markers
        ),
        hoverinfo='text',
        hovertext=hover_text,
        hoverlabel=dict(
            bgcolor='white',
            bordercolor=chart_data['color'],
            font=dict(family='Inter', size=13, color=CHART_THEME['text_color'])
        )
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
    
    # Enhanced professional layout using CHART_THEME for consistency
    # Enhanced professional layout with improved interactions
    fig.update_layout(
        title=dict(
            text=chart_data['title'],
            font=dict(size=20, color=CHART_THEME['title_color'], family='Inter'),
            x=0.05,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=CHART_THEME['grid_color'],
            zeroline=False,
            showline=True,
            linecolor=CHART_THEME['axis_color'],
            linewidth=1,
            tickfont=dict(size=12, color=CHART_THEME['subtitle_color']),
            title_font=dict(size=14, color=CHART_THEME['text_color']),
            # Add smooth transitions for axis interactions
            rangeslider=dict(visible=False),
            # Format date ticks nicely
            tickformat='%b %d',
            hoverformat='%B %d, %Y'
        ),
        yaxis=dict(
            title=chart_data['yaxis_title'],
            title_font=dict(size=14, color=CHART_THEME['text_color']),
            showgrid=True,
            gridwidth=1,
            gridcolor=CHART_THEME['grid_color'],
            zeroline=False,
            showline=True,
            linecolor=CHART_THEME['axis_color'],
            linewidth=1,
            tickfont=dict(size=12, color=CHART_THEME['subtitle_color']),
            # Format numbers with commas for thousands
            tickformat=',',
            # Add smooth transitions for axis interactions
            fixedrange=False
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        height=400,
        plot_bgcolor=CHART_THEME['plot_bgcolor'],
        paper_bgcolor=CHART_THEME['paper_bgcolor'],
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor=CHART_THEME['tooltip_bgcolor'],
            bordercolor=CHART_THEME['tooltip_bordercolor'],
            font_size=13,
            font_family='Inter'
        ),
        # Add smooth transitions for all chart interactions
        transition_duration=300,
        # Add annotations for important data points (if applicable)
        annotations=[],
        # Improve legend interaction
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Inter", size=12, color=CHART_THEME['text_color'])
        ),
        # Add modebar customization
        modebar=dict(
            bgcolor='rgba(255, 255, 255, 0.8)',
            color=CHART_THEME['text_color'],
            activecolor=chart_data['color']
        )
    )
    
    # Add custom hover effects and interactions
    fig.update_traces(
        hovertemplate=None,  # Use the custom hovertext we defined
        # Add smooth hover transitions
        hoveron='points+fills',
        hoverinfo='text',
        # Add selection styling
        selected=dict(
            marker=dict(
                color=chart_data['color'],
                size=10,
                opacity=1
            )
        ),
        unselected=dict(
            marker=dict(
                opacity=0.5
            ),
            textfont=dict(
                color='rgba(150, 150, 150, 0.5)'
            )
        )
    )
    
    charts.append(dcc.Graph(
        id=f'chart-{i+1}', 
        figure=fig,
        config=DEFAULT_CHART_CONFIG
    ))

# Create executive summary cards
summary_cards = []
for metric in summary_metrics:
    # Use consistent colors from our palette for trend indicators
    trend_color = COLOR_PALETTE['secondary'][0] if metric['trend'] == 'up' else COLOR_PALETTE['accent'][0]
    trend_arrow = '↗️' if metric['trend'] == 'up' else '↘️'
    
    summary_cards.append(html.Div([
        # Background gradient accent
        html.Div(style={
            'position': 'absolute',
            'top': 0,
            'left': 0,
            'right': 0,
            'height': '6px',
            'background': f'linear-gradient(90deg, {metric["color"]} 0%, {metric["color"]}80 100%)',
            'borderRadius': '6px 6px 0 0',
            'opacity': 0.8
        }),
        
        html.Div([
            # Icon with enhanced styling
            html.Div(
                html.Span(metric['icon'], style={'fontSize': '28px'}),
                style={
                    'backgroundColor': f'{metric["color"]}15',
                    'color': metric["color"],
                    'borderRadius': '12px',
                    'width': '56px',
                    'height': '56px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginRight': '16px'
                }
            ),
            html.Div([
                html.H3(metric['title'], 
                       style={'fontSize': '15px', 'fontWeight': '500', 'color': CHART_THEME['subtitle_color'], 'margin': '0 0 6px 0'}),
                html.H2(metric['value'], 
                       style={'fontSize': '30px', 'fontWeight': '700', 'color': CHART_THEME['title_color'], 'margin': '0 0 6px 0', 'letterSpacing': '-0.5px'}),
                html.Div([
                    html.Span(trend_arrow, style={'fontSize': '14px', 'marginRight': '4px'}),
                    html.Span(metric['change'], 
                             style={'fontSize': '15px', 'fontWeight': '600', 'color': trend_color})
                ]),
                # Add sparkline mini-chart
                html.Div([
                    dcc.Graph(
                        figure={
                            'data': [{
                                'x': list(range(len(metric['sparkline_data']))),
                                'y': metric['sparkline_data'],
                                'type': 'scatter',
                                'mode': 'lines',
                                'line': {'color': metric['color'], 'width': 2, 'shape': 'spline', 'smoothing': 1.3},
                                'fill': 'tozeroy',
                                'fillcolor': hex_to_rgba(metric['color'], 0.2)
                            }],
                            'layout': {
                                'height': 40,
                                'width': 120,
                                'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0, 'pad': 0},
                                'xaxis': {'visible': False, 'showgrid': False, 'zeroline': False},
                                'yaxis': {'visible': False, 'showgrid': False, 'zeroline': False},
                                'showlegend': False,
                                'plot_bgcolor': 'rgba(0,0,0,0)',
                                'paper_bgcolor': 'rgba(0,0,0,0)',
                                'hovermode': False
                            }
                        },
                        config={'displayModeBar': False, 'responsive': True}
                    )
                ], style={'marginTop': '8px'})
            ])
        ], style={'display': 'flex', 'alignItems': 'center', 'position': 'relative', 'zIndex': 2})
    ], className='kpi-card', style={
        'backgroundColor': 'white',
        'borderRadius': '16px',
        'padding': '28px',
        'boxShadow': '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
        'border': '1px solid rgba(255, 255, 255, 0.2)',
        'backdropFilter': 'blur(10px)',
        'position': 'relative',
        'overflow': 'hidden',
        'flex': '1'
    }))

# Create the enhanced grid layout with better spacing
grid = []
for row in range(4):
    grid.append(html.Div([
        html.Div([
            html.H3(charts_data[row*2]['title'], 
                   style={'fontSize': '18px', 'fontWeight': '700', 'color': CHART_THEME['title_color'], 'margin': '0 0 6px 0'}),
            html.P(charts_data[row*2]['subtitle'], 
                  style={'fontSize': '13px', 'color': CHART_THEME['subtitle_color'], 'margin': '0 0 16px 0', 'lineHeight': '1.4'}),
            charts[row*2]
        ], style={
            'flex': '1', 
            'backgroundColor': CHART_THEME['background'], 
            'borderRadius': '12px', 
            'padding': '20px', 
            'boxShadow': '0 2px 4px -1px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
            'minHeight': '420px'
        }),
        html.Div([
            html.H3(charts_data[row*2+1]['title'], 
                   style={'fontSize': '18px', 'fontWeight': '700', 'color': CHART_THEME['title_color'], 'margin': '0 0 6px 0'}),
            html.P(charts_data[row*2+1]['subtitle'], 
                  style={'fontSize': '13px', 'color': CHART_THEME['subtitle_color'], 'margin': '0 0 16px 0', 'lineHeight': '1.4'}),
            charts[row*2+1]
        ], style={
            'flex': '1', 
            'backgroundColor': CHART_THEME['background'], 
            'borderRadius': '12px', 
            'padding': '20px', 
            'boxShadow': '0 2px 4px -1px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
            'minHeight': '420px'
        })
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}))

# Create filter components
# Date range filter
date_filter = create_date_range_filter(id_prefix="date-filter")

# Category filters for different charts
revenue_filters = create_category_filter(
    id_prefix="revenue-filter",
    title="Division",
    options=[
        {'label': 'Retail', 'value': 'Retail'},
        {'label': 'Enterprise', 'value': 'Enterprise'},
        {'label': 'SMB', 'value': 'SMB'}
    ]
)

region_filters = create_category_filter(
    id_prefix="region-filter",
    title="Region",
    options=[
        {'label': 'North America', 'value': 'North America'},
        {'label': 'Europe', 'value': 'Europe'},
        {'label': 'Asia', 'value': 'Asia'},
        {'label': 'Other', 'value': 'Other'}
    ]
)

product_filters = create_category_filter(
    id_prefix="product-filter",
    title="Product Line",
    options=[
        {'label': 'Hardware', 'value': 'Hardware'},
        {'label': 'Software', 'value': 'Software'},
        {'label': 'Services', 'value': 'Services'}
    ]
)

market_filters = create_category_filter(
    id_prefix="market-filter",
    title="Market",
    options=[
        {'label': 'Consumer', 'value': 'Consumer'},
        {'label': 'Business', 'value': 'Business'},
        {'label': 'Government', 'value': 'Government'}
    ]
)

# Value range filter
value_range_filter = create_range_slider(
    id_prefix="value-filter",
    title="Value Range",
    min_val=0,
    max_val=1000,
    step=50,
    default_range=[0, 1000]
)

# Assemble filter panel
filter_panel = create_filter_panel([
    date_filter,
    revenue_filters,
    region_filters,
    product_filters,
    market_filters,
    value_range_filter
])

# Create active filters display
active_filters_display = create_active_filters_display()

# Store for filter state
filter_store = dcc.Store(id='filter-store', data={
    'date_range': {'start': '2023-01-01', 'end': '2023-04-10'},
    'categories': {},
    'value_range': [0, 1000]
})

# Enhanced main app layout
app.layout = html.Div([
    # Store for filter state
    filter_store,
    
    # Enhanced header with modern gradient and animations
    html.Div([
        # Subtle pattern overlay for visual depth
        html.Div(className='pattern-overlay', style={
            'position': 'absolute',
            'top': 0,
            'left': 0,
            'right': 0,
            'bottom': 0,
            'backgroundImage': 'url("data:image/svg+xml,%3Csvg width=\'20\' height=\'20\' viewBox=\'0 0 20 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.05\' fill-rule=\'evenodd\'%3E%3Ccircle cx=\'3\' cy=\'3\' r=\'3\'/%3E%3Ccircle cx=\'13\' cy=\'13\' r=\'3\'/%3E%3C/g%3E%3C/svg%3E")',
            'opacity': 0.1,
            'pointerEvents': 'none'
        }),
        
        html.Div([
            html.H1('Executive Business Dashboard', 
                   style={'fontSize': '42px', 'fontWeight': '800', 'color': 'white', 'margin': '0 0 12px 0', 'fontFamily': 'Inter', 
                          'textShadow': '0 2px 10px rgba(0, 0, 0, 0.15)'}),
            html.P('Q4 2023 Performance Review - Board Meeting', 
                  style={'fontSize': '18px', 'color': '#e5e7eb', 'margin': '0 0 20px 0', 'fontFamily': 'Inter',
                         'letterSpacing': '0.5px'}),
            html.Div([
                html.Span('Prepared by: Executive Analytics Team', 
                         style={'fontSize': '14px', 'color': '#d1d5db', 'marginRight': '24px'}),
                html.Span('Board Meeting: December 15, 2023', 
                         style={'fontSize': '14px', 'color': '#d1d5db'})
            ])
        ], style={'textAlign': 'center', 'padding': '48px 0', 'position': 'relative', 'zIndex': 2})
    ], style={
        'background': f'linear-gradient(135deg, {COLOR_PALETTE["primary"][0]} 0%, {COLOR_PALETTE["primary"][1]} 50%, {COLOR_PALETTE["primary"][2]} 100%)',
        'backgroundSize': '200% 200%',
        'animation': 'gradientShift 10s ease infinite',
        'marginBottom': '40px',
        'borderRadius': '0 0 24px 24px',
        'boxShadow': f'0 10px 25px -5px {hex_to_rgba(COLOR_PALETTE["primary"][1], 0.3)}',
        'position': 'relative',
        'overflow': 'hidden'
    }),
    
    # Executive summary section
    html.Div([
        html.H2('Key Performance Indicators', 
               style={'fontSize': '24px', 'fontWeight': '700', 'color': '#1f2937', 'margin': '0 0 24px 0', 'textAlign': 'center'}),
        html.Div(summary_cards, style={'display': 'flex', 'gap': '24px', 'marginBottom': '48px'})
    ], style={'width': '100%', 'padding': '0 64px 0 24px', 'margin': '0 auto'}),
    
    # Dashboard content with filters
    html.Div([
        # Active filters display
        active_filters_display,
        
        # Main content with filters and charts
        html.Div([
            # Left sidebar with filters - made narrower and better styled
            html.Div([
                filter_panel
            ], style={
                'width': '220px', 
                'marginRight': '24px',
                'flexShrink': '0'
            }),
            
            # Main content area with charts - improved spacing
            html.Div(grid, style={
                'flex': '1',
                'minWidth': '0',
                'maxWidth': 'calc(100% - 244px)'  # Account for filter panel width + margin
            })
        ], style={
            'display': 'flex', 
            'alignItems': 'flex-start',
            'width': '100%',
            'maxWidth': '1600px',
            'margin': '0 auto'
        }),
    ], style={'width': '100%', 'padding': '0 20px'}),
    
    # Professional footer with consistent theme colors
    html.Div([
        html.Div([
            html.Span('Data Source: Enterprise Analytics Platform', 
                     style={'fontSize': '12px', 'color': CHART_THEME['subtitle_color'], 'marginRight': '24px'}),
            html.Span(f'Last Updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', 
                     style={'fontSize': '12px', 'color': CHART_THEME['subtitle_color'], 'marginRight': '24px'}),
            html.Span('Confidential - Board Use Only', 
                     style={'fontSize': '12px', 'color': COLOR_PALETTE['accent'][0], 'fontWeight': '600'})
        ], style={'textAlign': 'center', 'padding': '20px 0', 'borderTop': f'1px solid {CHART_THEME["legend_bordercolor"]}'})
    ], style={'width': '100%', 'padding': '0 64px 0 24px', 'margin': '0 auto'})
    
], style={
    'backgroundColor': '#f8fafc',
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif',
    'padding': '0 0 40px 0'
})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8050')

# Callback to update filter store when filters change
@app.callback(
    Output('filter-store', 'data'),
    [Input('apply-filters-button', 'n_clicks')],
    [
        State('date-filter-range', 'start_date'),
        State('date-filter-range', 'end_date'),
        State('revenue-filter-dropdown', 'value'),
        State('region-filter-dropdown', 'value'),
        State('product-filter-dropdown', 'value'),
        State('market-filter-dropdown', 'value'),
        State('value-filter-slider', 'value'),
        State('filter-store', 'data')
    ]
)
def update_filter_store(n_clicks, start_date, end_date, division, region, product_line, market, value_range, current_data):
    # Initialize with current data
    if current_data is None:
        current_data = {
            'date_range': {'start': '2023-01-01', 'end': '2023-04-10'},
            'categories': {},
            'value_range': [0, 1000]
        }
    
    # Only update if apply button was clicked
    if n_clicks is not None:
        # Update date range
        current_data['date_range'] = {'start': start_date, 'end': end_date}
        
        # Update categories
        categories = {}
        if division is not None:
            categories['division'] = division
        if region is not None:
            categories['region'] = region
        if product_line is not None:
            categories['product_line'] = product_line
        if market is not None:
            categories['market'] = market
        
        current_data['categories'] = categories
        
        # Update value range
        current_data['value_range'] = value_range
    
    return current_data

# Callback to reset filters
@app.callback(
    [
        Output('date-filter-range', 'start_date'),
        Output('date-filter-range', 'end_date'),
        Output('revenue-filter-dropdown', 'value'),
        Output('region-filter-dropdown', 'value'),
        Output('product-filter-dropdown', 'value'),
        Output('market-filter-dropdown', 'value'),
        Output('value-filter-slider', 'value')
    ],
    [Input('reset-filters-button', 'n_clicks')],
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    # Default values
    start_date = (datetime.now() - timedelta(days=100)).date()
    end_date = datetime.now().date()
    
    return [
        start_date,
        end_date,
        ['Retail', 'Enterprise', 'SMB'],  # All divisions
        ['North America', 'Europe', 'Asia', 'Other'],  # All regions
        ['Hardware', 'Software', 'Services'],  # All product lines
        ['Consumer', 'Business', 'Government'],  # All markets
        [0, 1000]  # Full value range
    ]

# Callback to update active filters display
@app.callback(
    [
        Output('active-filters-container', 'style'),
        Output('active-filters-content', 'children')
    ],
    [Input('filter-store', 'data')]
)
def update_active_filters(filter_data):
    if filter_data is None:
        # No filters applied yet
        return {'display': 'none'}, [html.Span("No active filters", style={'fontSize': '14px', 'color': CHART_THEME['subtitle_color'], 'fontStyle': 'italic'})]
    
    # Check if any filters are active
    has_filters = False
    filter_tags = []
    
    # Date range filter
    if 'date_range' in filter_data and filter_data['date_range']:
        start = filter_data['date_range'].get('start')
        end = filter_data['date_range'].get('end')
        if start and end:
            has_filters = True
            filter_tags.append(create_filter_tag("Date Range", f"{start} to {end}", "date-range"))
    
    # Category filters
    if 'categories' in filter_data and filter_data['categories']:
        for category, values in filter_data['categories'].items():
            if values and len(values) > 0:
                has_filters = True
                if isinstance(values, list):
                    if len(values) < 3:  # Only show individual values if there aren't too many
                        filter_tags.append(create_filter_tag(category.title(), ", ".join(values), f"category-{category}"))
                    else:
                        filter_tags.append(create_filter_tag(category.title(), f"{len(values)} selected", f"category-{category}"))
                else:
                    filter_tags.append(create_filter_tag(category.title(), values, f"category-{category}"))
    
    # Value range filter
    if 'value_range' in filter_data and filter_data['value_range']:
        min_val, max_val = filter_data['value_range']
        if min_val > 0 or max_val < 1000:  # Only show if not the default range
            has_filters = True
            filter_tags.append(create_filter_tag("Value Range", f"{min_val} - {max_val}", "value-range"))
    
    if not has_filters:
        return {'display': 'none'}, [html.Span("No active filters", style={'fontSize': '14px', 'color': CHART_THEME['subtitle_color'], 'fontStyle': 'italic'})]
    
    return {
        'marginBottom': '24px',
        'padding': '12px 16px',
        'backgroundColor': hex_to_rgba(COLOR_PALETTE['primary'][1], 0.05),
        'borderRadius': '8px',
        'border': f'1px solid {hex_to_rgba(COLOR_PALETTE["primary"][1], 0.2)}',
        'display': 'block'
    }, filter_tags

# Callback to update charts based on filters
@app.callback(
    [Output(f'chart-{i+1}', 'figure') for i in range(len(charts_data))],
    [Input('filter-store', 'data')]
)
def update_charts(filter_data):
    if filter_data is None:
        # No filters applied yet, return original charts
        return [chart.figure for chart in charts]
    
    # Extract filter values
    start_date = filter_data.get('date_range', {}).get('start')
    end_date = filter_data.get('date_range', {}).get('end')
    categories = filter_data.get('categories', {})
    value_range = filter_data.get('value_range')
    
    # Update each chart with filtered data
    updated_figures = []
    
    for i, chart_data in enumerate(charts_data):
        # Generate filtered data
        time, data = chart_data['data_func'](
            seed=chart_data['seed'],
            start_date=start_date,
            end_date=end_date,
            categories=categories,
            value_range=value_range
        )
        
        # Calculate percent change for tooltips
        pct_change = []
        for j in range(len(data)):
            if j == 0:
                pct_change.append(0)
            else:
                change = ((data[j] - data[j-1]) / data[j-1]) * 100 if data[j-1] != 0 else 0
                pct_change.append(change)
        
        # Format tooltips
        hover_text = []
        for j, (t, val, pct) in enumerate(zip(time, data, pct_change)):
            # Convert numpy.datetime64 to pandas Timestamp for strftime
            if isinstance(t, np.datetime64):
                t = pd.Timestamp(t)
                
            # Format the value based on the type of data
            if "Revenue" in chart_data["yaxis_title"] or "Sales" in chart_data["yaxis_title"]:
                formatted_val = f"${val:,.1f}M"
            elif "%" in chart_data["yaxis_title"]:
                formatted_val = f"{val:.2f}%"
            elif "Score" in chart_data["yaxis_title"]:
                formatted_val = f"{val:.2f}/5.0"
            else:
                formatted_val = f"{val:,.1f}"
            
            # Add trend indicator and contextual information
            if j > 0:
                trend = "▲" if pct > 0 else "▼" if pct < 0 else "◆"
                trend_color = COLOR_PALETTE['secondary'][0] if pct > 0 else COLOR_PALETTE['accent'][0] if pct < 0 else "#6b7280"
                
                # Add period-over-period comparison
                if j >= 7 and j < len(data):  # If we have enough data for week-over-week
                    wow_change = ((val - data[j-7]) / data[j-7]) * 100 if data[j-7] != 0 else 0
                    wow_text = f"WoW: {wow_change:+.1f}%"
                else:
                    wow_text = ""
                    
                hover_text.append(
                    f"<b>{t.strftime('%B %d, %Y')}</b><br>" +
                    f"<b>{chart_data['yaxis_title']}:</b> {formatted_val}<br>" +
                    f"<span style='color:{trend_color}'>{trend} {pct:+.1f}% from previous day</span><br>" +
                    (f"{wow_text}" if wow_text else "")
                )
            else:
                hover_text.append(
                    f"<b>{t.strftime('%B %d, %Y')}</b><br>" +
                    f"<b>{chart_data['yaxis_title']}:</b> {formatted_val}"
                )
        
        # Create updated traces
        trace = go.Scatter(
            x=time, 
            y=data, 
            mode='lines+markers',
            name=chart_data['title'],
            line=dict(
                color=chart_data['color'], 
                width=4,
                shape='spline',
                smoothing=1.3
            ),
            marker=dict(
                size=6, 
                color=chart_data['color'],
                line=dict(width=1, color='white')
            ),
            hoverinfo='text',
            hovertext=hover_text,
            hoverlabel=dict(
                bgcolor='white',
                bordercolor=chart_data['color'],
                font=dict(family='Inter', size=13, color=CHART_THEME['text_color'])
            )
        )
        
        # Add area fill
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
        
        # Get the original figure to preserve layout settings
        fig = charts[i].figure
        
        # Update with new data
        fig.data = [area_trace, trace]
        
        # Add animation for smooth transitions
        fig.update_layout(transition_duration=500)
        
        updated_figures.append(fig)
    
    return updated_figures

# Callback to update min/max value display for range slider
@app.callback(
    [
        Output('value-filter-min-value', 'children'),
        Output('value-filter-max-value', 'children')
    ],
    [Input('value-filter-slider', 'value')]
)
def update_range_values(value_range):
    if value_range is None:
        return "0", "1000"
    return str(value_range[0]), str(value_range[1])