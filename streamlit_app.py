import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Executive Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper function to convert hex to rgba
def hex_to_rgba(hex_color, alpha=0.2):
    """Convert hex color to rgba format"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

# Generate enhanced business data
def generate_sales_data(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_trend = np.linspace(120, 180, 100)
    seasonal = 15 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 8, 100)
    data = base_trend + seasonal + noise
    return time, data

def generate_revenue_data(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_trend = np.linspace(500, 850, 100)
    seasonal = 25 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 15, 100)
    data = base_trend + seasonal + noise
    return time, data

def generate_profit_margins(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_margin = 18 + np.linspace(0, 5, 100)
    seasonal = 2 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 1, 100)
    data = base_margin + seasonal + noise
    return time, data

def generate_customer_satisfaction(seed=0):
    np.random.seed(seed)
    time = pd.date_range(start='2023-01-01', periods=100, freq='D')
    base_score = 4.4 + np.linspace(0, 0.4, 100)
    monthly_fluctuation = 0.15 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(0, 0.08, 100)
    data = base_score + monthly_fluctuation + noise
    return time, data

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

# Charts data
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
        'title': 'Sales Performance',
        'subtitle': 'Regional sales distribution and growth',
        'data_func': generate_sales_data,
        'color': '#dc2626',
        'yaxis_title': 'Sales ($K)',
        'seed': 3
    },
    {
        'title': 'Customer Satisfaction',
        'subtitle': 'NPS scores and customer experience metrics',
        'data_func': generate_customer_satisfaction,
        'color': '#7c3aed',
        'yaxis_title': 'Satisfaction Score',
        'seed': 4
    }
]

# Main app
def main():
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 2px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.5rem; font-weight: 800; margin: 0 0 0.5rem 0;">Executive Business Dashboard</h1>
        <p style="font-size: 1.2rem; margin: 0 0 1rem 0; opacity: 0.9;">Q4 2023 Performance Review - Board Meeting</p>
        <div style="font-size: 0.9rem; opacity: 0.8;">
            <span style="margin-right: 2rem;">Prepared by: Executive Analytics Team</span>
            <span>Board Meeting: December 15, 2023</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive summary section
    st.markdown("## Key Performance Indicators")
    
    # Create metric cards
    cols = st.columns(4)
    for i, metric in enumerate(summary_metrics):
        with cols[i]:
            trend_color = '#059669' if metric['trend'] == 'up' else '#dc2626'
            trend_arrow = '↗️' if metric['trend'] == 'up' else '↘️'
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{metric['icon']}</span>
                    <div>
                        <h3 style="font-size: 0.9rem; font-weight: 500; color: #6b7280; margin: 0 0 0.25rem 0;">{metric['title']}</h3>
                        <h2 style="font-size: 1.75rem; font-weight: 700; color: #1f2937; margin: 0 0 0.25rem 0;">{metric['value']}</h2>
                        <div style="font-size: 0.9rem; font-weight: 600; color: {trend_color};">
                            {trend_arrow} {metric['change']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown("## Performance Analytics")
    
    # Create charts in a 2x2 grid
    for i in range(0, len(charts_data), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(charts_data):
                chart_data = charts_data[i + j]
                time, data = chart_data['data_func'](seed=chart_data['seed'])
                
                with cols[j]:
                    st.markdown(f"""
                    <div class="chart-container">
                        <h3 style="font-size: 1.25rem; font-weight: 700; color: #1f2937; margin: 0 0 0.5rem 0;">{chart_data['title']}</h3>
                        <p style="font-size: 0.9rem; color: #6b7280; margin: 0 0 1rem 0;">{chart_data['subtitle']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create the chart
                    fig = go.Figure()
                    
                    # Add area fill
                    fig.add_trace(go.Scatter(
                        x=time,
                        y=data,
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor=hex_to_rgba(chart_data['color'], 0.15),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    # Add main line
                    fig.add_trace(go.Scatter(
                        x=time, 
                        y=data, 
                        mode='lines+markers',
                        name=chart_data['title'],
                        line=dict(color=chart_data['color'], width=4),
                        marker=dict(size=6, color=chart_data['color']),
                        hovertemplate='<b>%{x|%B %d, %Y}</b><br>' +
                                     f'{chart_data["yaxis_title"]}: %{{y:,.1f}}<extra></extra>'
                    ))
                    
                    # Enhanced layout
                    fig.update_layout(
                        title=None,
                        xaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='#f3f4f6',
                            zeroline=False,
                            showline=True,
                            linecolor='#d1d5db',
                            linewidth=1,
                            tickfont=dict(size=10, color='#6b7280')
                        ),
                        yaxis=dict(
                            title=chart_data['yaxis_title'],
                            titlefont=dict(size=12, color='#374151', weight=500),
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='#f3f4f6',
                            zeroline=False,
                            showline=True,
                            linecolor='#d1d5db',
                            linewidth=1,
                            tickfont=dict(size=10, color='#6b7280')
                        ),
                        margin=dict(l=50, r=20, t=20, b=50),
                        height=350,
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
                    
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: #6b7280; font-size: 0.8rem;">
        <span style="margin-right: 1.5rem;">Data Source: Enterprise Analytics Platform</span>
        <span style="margin-right: 1.5rem;">Last Updated: """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</span>
        <span style="color: #dc2626; font-weight: 600;">Confidential - Board Use Only</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 