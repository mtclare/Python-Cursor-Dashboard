import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# --- 1. Generate Sample Data ---
# Let's create dummy data for 6 metrics over 4 years (e.g., daily data)
# Current year is 2025, so let's use 2021-2024 for 4 full years of historical data.
start_year = 2021
num_years = 4
num_days_per_year = 365 # Ignoring leap years for simplicity in this example

metrics = [f'Metric {i+1}' for i in range(6)]
data = []

for metric_name in metrics:
    for year_offset in range(num_years):
        current_year = start_year + year_offset
        dates = pd.date_range(start=f'{current_year}-01-01', periods=num_days_per_year, freq='D')
        # Simulate some trend and noise for each metric
        trend = np.linspace(0, 10 + np.random.rand() * 5, num_days_per_year)
        noise = np.random.randn(num_days_per_year) * (1 + np.random.rand() * 2)
        values = (trend + noise).cumsum() + np.random.rand() * 50 # Cumulative sum for a time-series look

        df_year = pd.DataFrame({
            'Date': dates,
            'Year': current_year,
            'Metric': metric_name,
            'Value': values
        })
        data.append(df_year)

df = pd.concat(data)

# Extract day of year for consistent x-axis across years
df['DayOfYear'] = df['Date'].dt.dayofyear


# --- 2. Initialize the Dash App ---
app = Dash(__name__)

# --- 3. Define the App Layout ---
app.layout = html.Div([
    html.H1("Multi-Metric Time Series Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    html.Div([
        html.Label("Select a Metric:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': m, 'value': m} for m in metrics],
            value=metrics[0],  # Default selected metric
            clearable=False,
            style={'width': '50%', 'minWidth': '200px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'}),

    dcc.Graph(id='time-series-plot')
])

# --- 4. Define Callbacks for Interactivity ---
@app.callback(
    Output('time-series-plot', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_graph(selected_metric):
    filtered_df = df[df['Metric'] == selected_metric].copy()

    # Create the Plotly Express line chart
    # We use DayOfYear for the x-axis to align the trends across years,
    # but display the actual date in the hover template.
    fig = px.line(
        filtered_df,
        x='DayOfYear', # Use DayOfYear for consistent x-axis across years
        y='Value',
        color='Year', # Each year gets a separate line with a different color
        title=f'{selected_metric} Performance Over 4 Years',
        labels={
            "DayOfYear": "Day of Year",
            "Value": "Value",
            "Year": "Year"
        }
    )

    # Customize hover info to show original date, not just DayOfYear
    fig.update_traces(
        mode='lines',
        hovertemplate="<b>%{data.name}</b><br>" + # Displays the year (from color)
                      "Date: %{customdata[0]|%b %d, %Y}<br>" + # customdata will hold the original date
                      "Value: %{y:.2f}<extra></extra>", # Remove default 'trace' name
        customdata=np.stack([filtered_df['Date']], axis=-1)
    )

    # Improve layout
    fig.update_layout(
        transition_duration=500, # Smooth transitions for changes
        hovermode="x unified",   # Show hover info for all lines at a given x-point
        xaxis_title="Day of Year",
        yaxis_title="Value",
        legend_title="Year",
        font=dict(family="Arial, sans-serif", size=12, color="#7f7f7f"),
        margin=dict(l=40, r=40, t=80, b=40), # Adjust margins for better fit
        # If you want to show actual month/day on x-axis (without year), you'd need more complex x-axis formatting.
        # For this example, DayOfYear is clear, and hover shows full date.
    )

    return fig

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True)