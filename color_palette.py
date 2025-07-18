"""
Color Palette System for Executive Dashboard
Provides accessible color schemes with proper contrast ratios
"""
import colorsys
import math

# Enhanced color palette based on design document
COLOR_PALETTE = {
    'primary': ['#1e40af', '#3b82f6', '#6366f1', '#8b5cf6'],
    'secondary': ['#059669', '#10b981', '#34d399', '#6ee7b7'],
    'accent': ['#dc2626', '#ef4444', '#f87171', '#fca5a5'],
    'neutral': ['#374151', '#6b7280', '#9ca3af', '#d1d5db']
}

# Categorical palette for charts with many series
CATEGORICAL_PALETTE = [
    '#1e40af',  # Primary blue
    '#059669',  # Secondary green
    '#dc2626',  # Accent red
    '#7c3aed',  # Purple
    '#ea580c',  # Orange
    '#0891b2',  # Cyan
    '#be185d',  # Pink
    '#16a34a',  # Green
    '#4f46e5',  # Indigo
    '#b45309',  # Amber
    '#0369a1',  # Light blue
    '#9d174d',  # Rose
]

# Sequential color scales for heatmaps and continuous data
SEQUENTIAL_SCALES = {
    'blue': ['#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8', '#1e40af', '#1e3a8a'],
    'green': ['#d1fae5', '#a7f3d0', '#6ee7b7', '#34d399', '#10b981', '#059669', '#047857', '#065f46', '#064e3b'],
    'red': ['#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'],
    'purple': ['#ede9fe', '#ddd6fe', '#c4b5fd', '#a78bfa', '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95'],
}

# Diverging scales for data that has a meaningful center point
DIVERGING_SCALES = {
    'blue_red': ['#1e40af', '#3b82f6', '#93c5fd', '#dbeafe', '#f8fafc', '#fee2e2', '#fca5a5', '#ef4444', '#dc2626'],
    'green_purple': ['#059669', '#10b981', '#6ee7b7', '#d1fae5', '#f8fafc', '#ede9fe', '#c4b5fd', '#8b5cf6', '#7c3aed'],
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_rgba(hex_color, alpha=0.2):
    """Convert hex color to rgba format"""
    rgb = hex_to_rgb(hex_color)
    return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'

def get_luminance(hex_color):
    """Calculate relative luminance of a color for WCAG contrast calculations"""
    r, g, b = [x/255.0 for x in hex_to_rgb(hex_color)]
    
    # Convert sRGB to linear RGB
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    
    # Calculate luminance
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors according to WCAG"""
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)
    
    # Ensure the lighter color is first
    if lum1 < lum2:
        lum1, lum2 = lum2, lum1
        
    # Calculate contrast ratio
    return (lum1 + 0.05) / (lum2 + 0.05)

def is_accessible(color, background='#ffffff', level='AA'):
    """Check if color is accessible on given background
    
    Args:
        color: Foreground color in hex
        background: Background color in hex
        level: 'AA' (minimum 4.5:1) or 'AAA' (minimum 7:1)
    
    Returns:
        bool: Whether the contrast meets the specified level
    """
    ratio = get_contrast_ratio(color, background)
    if level == 'AA':
        return ratio >= 4.5
    elif level == 'AAA':
        return ratio >= 7.0
    return False

def get_accessible_variant(color, background='#ffffff', level='AA'):
    """Get an accessible variant of a color if it doesn't meet contrast requirements
    
    Args:
        color: Original color in hex
        background: Background color in hex
        level: 'AA' or 'AAA'
    
    Returns:
        str: Original color if accessible, or a modified version with better contrast
    """
    if is_accessible(color, background, level):
        return color
    
    # Convert to HSL for easier manipulation
    r, g, b = [x/255.0 for x in hex_to_rgb(color)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Determine if we should darken or lighten based on background
    bg_lum = get_luminance(background)
    
    if bg_lum > 0.5:  # Light background, darken the color
        step = 0.05
        max_steps = 10
        for i in range(max_steps):
            l = max(0, l - step)
            new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, s)
            new_color = rgb_to_hex((new_r*255, new_g*255, new_b*255))
            if is_accessible(new_color, background, level):
                return new_color
    else:  # Dark background, lighten the color
        step = 0.05
        max_steps = 10
        for i in range(max_steps):
            l = min(1, l + step)
            new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, s)
            new_color = rgb_to_hex((new_r*255, new_g*255, new_b*255))
            if is_accessible(new_color, background, level):
                return new_color
    
    # If we couldn't find a good variant, return a fallback
    return '#000000' if bg_lum > 0.5 else '#ffffff'

def get_chart_colors(num_colors, palette_type='categorical'):
    """Get a list of colors for chart elements
    
    Args:
        num_colors: Number of colors needed
        palette_type: 'categorical', 'sequential_blue', 'sequential_green', etc.
    
    Returns:
        list: List of hex color codes
    """
    if palette_type == 'categorical':
        # For categorical data, cycle through the categorical palette
        return [CATEGORICAL_PALETTE[i % len(CATEGORICAL_PALETTE)] for i in range(num_colors)]
    
    elif palette_type.startswith('sequential_'):
        # For sequential data, interpolate along the specified scale
        color_name = palette_type.split('_')[1]
        if color_name in SEQUENTIAL_SCALES:
            scale = SEQUENTIAL_SCALES[color_name]
            if num_colors <= len(scale):
                # If we need fewer colors than in the scale, select evenly
                indices = [int(i * (len(scale) - 1) / (num_colors - 1)) if num_colors > 1 else 0 for i in range(num_colors)]
                return [scale[i] for i in indices]
            else:
                # If we need more colors, interpolate
                return interpolate_colors(scale, num_colors)
    
    elif palette_type.startswith('diverging_'):
        # For diverging data, interpolate along the specified scale
        scale_name = palette_type.split('_', 1)[1]
        if scale_name in DIVERGING_SCALES:
            scale = DIVERGING_SCALES[scale_name]
            if num_colors <= len(scale):
                indices = [int(i * (len(scale) - 1) / (num_colors - 1)) if num_colors > 1 else 0 for i in range(num_colors)]
                return [scale[i] for i in indices]
            else:
                return interpolate_colors(scale, num_colors)
    
    # Default fallback
    return [CATEGORICAL_PALETTE[i % len(CATEGORICAL_PALETTE)] for i in range(num_colors)]

def interpolate_colors(color_scale, num_colors):
    """Interpolate between colors in a scale to get the desired number of colors"""
    result = []
    
    if num_colors <= 1:
        return [color_scale[0]]
    
    # Calculate how many segments we need between colors
    segments = num_colors - 1
    scale_segments = len(color_scale) - 1
    
    for i in range(num_colors):
        # Calculate position in the original scale (0 to scale_segments)
        pos = i * scale_segments / segments
        
        # Find the two colors to interpolate between
        idx1 = int(pos)
        idx2 = min(idx1 + 1, len(color_scale) - 1)
        
        # Calculate interpolation factor between the two colors (0 to 1)
        factor = pos - idx1
        
        if factor == 0:
            # Exact match with a color in the scale
            result.append(color_scale[idx1])
        else:
            # Interpolate between two colors
            rgb1 = hex_to_rgb(color_scale[idx1])
            rgb2 = hex_to_rgb(color_scale[idx2])
            
            r = rgb1[0] + factor * (rgb2[0] - rgb1[0])
            g = rgb1[1] + factor * (rgb2[1] - rgb1[1])
            b = rgb1[2] + factor * (rgb2[2] - rgb1[2])
            
            result.append(rgb_to_hex((r, g, b)))
    
    return result

# Theme configuration for charts
CHART_THEME = {
    'background': '#ffffff',
    'plot_bgcolor': '#ffffff',
    'paper_bgcolor': '#ffffff',
    'grid_color': '#f3f4f6',
    'axis_color': '#d1d5db',
    'text_color': '#374151',
    'title_color': '#1f2937',
    'subtitle_color': '#6b7280',
    'legend_bgcolor': '#ffffff',
    'legend_bordercolor': '#e5e7eb',
    'tooltip_bgcolor': '#ffffff',
    'tooltip_bordercolor': '#d1d5db',
}

# Default chart configuration
DEFAULT_CHART_CONFIG = {
    'displayModeBar': False,
    'responsive': True,
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'executive_chart',
        'height': 600,
        'width': 1000,
        'scale': 2
    }
}