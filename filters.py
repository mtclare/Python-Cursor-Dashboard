"""
Filter components for the Executive Dashboard
Provides interactive filtering capabilities for data exploration
"""
import dash
from dash import dcc, html
from datetime import datetime, timedelta
import pandas as pd
from color_palette import COLOR_PALETTE, hex_to_rgba, CHART_THEME

def create_date_range_filter(id_prefix="date", default_days=90):
    """
    Create a date range filter component
    
    Args:
        id_prefix: Prefix for component IDs
        default_days: Default number of days to show
        
    Returns:
        html.Div: Date range filter component
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=default_days)
    
    return html.Div([
        html.H4("Date Range", 
                style={'fontSize': '16px', 'fontWeight': '600', 'color': CHART_THEME['title_color'], 'marginBottom': '12px'}),
        dcc.DatePickerRange(
            id=f'{id_prefix}-range',
            start_date=start_date.date(),
            end_date=end_date.date(),
            display_format='MMM DD, YYYY',
            first_day_of_week=1,  # Monday
            min_date_allowed=end_date - timedelta(days=365*2),  # 2 years back
            max_date_allowed=end_date,
            initial_visible_month=end_date,
            clearable=False,
            updatemode='bothdates',
            style={
                'width': '100%',
                'zIndex': 1000
            }
        )
    ], style={
        'marginBottom': '24px',
        'padding': '16px',
        'backgroundColor': CHART_THEME['background'],
        'borderRadius': '8px',
        'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
        'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.05)'
    })

def create_category_filter(id_prefix, title, options, multi=True):
    """
    Create a category filter component with checkboxes or dropdown
    
    Args:
        id_prefix: Prefix for component IDs
        title: Filter title
        options: List of options as [{'label': 'Label', 'value': 'value'}, ...]
        multi: Whether multiple selection is allowed
        
    Returns:
        html.Div: Category filter component
    """
    return html.Div([
        html.H4(title, 
                style={'fontSize': '16px', 'fontWeight': '600', 'color': CHART_THEME['title_color'], 'marginBottom': '12px'}),
        dcc.Dropdown(
            id=f'{id_prefix}-dropdown',
            options=options,
            value=[opt['value'] for opt in options] if multi else options[0]['value'],
            multi=multi,
            clearable=False,
            style={
                'width': '100%',
                'borderRadius': '6px',
                'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
            }
        )
    ], style={
        'marginBottom': '24px',
        'padding': '16px',
        'backgroundColor': CHART_THEME['background'],
        'borderRadius': '8px',
        'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
        'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.05)'
    })

def create_range_slider(id_prefix, title, min_val, max_val, step=1, default_range=None):
    """
    Create a range slider filter component
    
    Args:
        id_prefix: Prefix for component IDs
        title: Filter title
        min_val: Minimum value
        max_val: Maximum value
        step: Step size
        default_range: Default range as [min, max]
        
    Returns:
        html.Div: Range slider component
    """
    if default_range is None:
        default_range = [min_val, max_val]
        
    return html.Div([
        html.H4(title, 
                style={'fontSize': '16px', 'fontWeight': '600', 'color': CHART_THEME['title_color'], 'marginBottom': '12px'}),
        dcc.RangeSlider(
            id=f'{id_prefix}-slider',
            min=min_val,
            max=max_val,
            step=step,
            value=default_range,
            marks={
                min_val: {'label': f'{min_val}', 'style': {'color': CHART_THEME['subtitle_color']}},
                max_val: {'label': f'{max_val}', 'style': {'color': CHART_THEME['subtitle_color']}}
            },
            tooltip={'placement': 'bottom', 'always_visible': False},
            allowCross=False,
            className='custom-range-slider'
        ),
        html.Div([
            html.Span(f"{default_range[0]}", id=f"{id_prefix}-min-value", 
                     style={'fontSize': '14px', 'color': CHART_THEME['subtitle_color']}),
            html.Span(f"{default_range[1]}", id=f"{id_prefix}-max-value", 
                     style={'fontSize': '14px', 'color': CHART_THEME['subtitle_color']})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '8px'})
    ], style={
        'marginBottom': '24px',
        'padding': '16px',
        'backgroundColor': CHART_THEME['background'],
        'borderRadius': '8px',
        'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
        'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.05)'
    })

def create_filter_panel(filter_components):
    """
    Create a filter panel with multiple filter components
    
    Args:
        filter_components: List of filter components
        
    Returns:
        html.Div: Filter panel component
    """
    return html.Div([
        html.Div([
            html.H3("Filters", 
                   style={'fontSize': '20px', 'fontWeight': '700', 'color': CHART_THEME['title_color'], 'margin': '0'}),
            html.Button(
                "Reset All",
                id="reset-filters-button",
                style={
                    'backgroundColor': 'transparent',
                    'color': COLOR_PALETTE['primary'][1],
                    'border': 'none',
                    'cursor': 'pointer',
                    'fontSize': '14px',
                    'fontWeight': '500',
                    'padding': '8px 12px',
                    'borderRadius': '6px',
                    'transition': 'background-color 0.2s',
                    'outline': 'none',
                }
            )
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '16px'}),
        html.Hr(style={'margin': '0 0 16px 0', 'borderTop': f'1px solid {CHART_THEME["legend_bordercolor"]}'}),
        *filter_components,
        html.Div([
            html.Button(
                "Apply Filters",
                id="apply-filters-button",
                style={
                    'backgroundColor': COLOR_PALETTE['primary'][1],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'padding': '12px 24px',
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'width': '100%',
                    'transition': 'background-color 0.2s',
                    'boxShadow': f'0 4px 6px -1px {hex_to_rgba(COLOR_PALETTE["primary"][1], 0.2)}'
                }
            )
        ], style={'marginTop': '8px'})
    ], style={
        'backgroundColor': CHART_THEME['background'],
        'borderRadius': '16px',
        'padding': '24px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
        'height': 'fit-content'
    })

def create_active_filters_display(id_prefix="active-filters"):
    """
    Create a component to display active filters
    
    Args:
        id_prefix: Prefix for component IDs
        
    Returns:
        html.Div: Active filters display component
    """
    return html.Div([
        html.Div(id=f"{id_prefix}-content", children=[
            html.Span("No active filters", 
                     style={'fontSize': '14px', 'color': CHART_THEME['subtitle_color'], 'fontStyle': 'italic'})
        ])
    ], style={
        'marginBottom': '24px',
        'padding': '12px 16px',
        'backgroundColor': hex_to_rgba(COLOR_PALETTE['primary'][1], 0.05),
        'borderRadius': '8px',
        'border': f'1px solid {hex_to_rgba(COLOR_PALETTE["primary"][1], 0.2)}',
        'display': 'none'  # Initially hidden
    }, id=f"{id_prefix}-container")

def create_filter_tag(filter_name, filter_value, tag_id=None):
    """
    Create a filter tag for the active filters display
    
    Args:
        filter_name: Name of the filter
        filter_value: Value of the filter
        tag_id: Optional ID for the tag
        
    Returns:
        html.Div: Filter tag component
    """
    return html.Div([
        html.Span(f"{filter_name}: ", 
                 style={'fontSize': '13px', 'fontWeight': '600', 'color': CHART_THEME['title_color']}),
        html.Span(f"{filter_value}", 
                 style={'fontSize': '13px', 'color': CHART_THEME['text_color']}),
        html.Button(
            "✕",
            id={"type": "remove-filter", "index": tag_id} if tag_id else None,
            style={
                'backgroundColor': 'transparent',
                'border': 'none',
                'color': CHART_THEME['subtitle_color'],
                'cursor': 'pointer',
                'fontSize': '12px',
                'padding': '0 0 0 6px',
                'marginLeft': '4px'
            }
        )
    ], style={
        'display': 'inline-flex',
        'alignItems': 'center',
        'backgroundColor': CHART_THEME['background'],
        'borderRadius': '16px',
        'padding': '4px 10px',
        'margin': '0 8px 8px 0',
        'border': f'1px solid {CHART_THEME["legend_bordercolor"]}',
    })