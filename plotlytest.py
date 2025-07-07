import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. Generate Sample Data (same as above) ---
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
cohorts = ['A', 'B', 'C']
data = []

for cohort in cohorts:
    actual = np.cumsum(np.random.randn(100) * 0.5 + 5) + (10 if cohort == 'A' else (20 if cohort == 'B' else 30))
    predicted = actual + np.random.randn(100) * 2 - 1

    df_cohort = pd.DataFrame({
        'Date': dates,
        'Cohort': cohort,
        'Value': actual,
        'Type': 'Actual'
    })
    data.append(df_cohort)

    df_pred_cohort = pd.DataFrame({
        'Date': dates,
        'Cohort': cohort,
        'Value': predicted,
        'Type': 'Predicted'
    })
    data.append(df_pred_cohort)

df = pd.concat(data)

# --- 2. Plotting with Plotly Express Faceting ---
fig = px.line(
    df,
    x="Date",
    y="Value",
    color="Type",       # Color lines by 'Type' (Actual/Predicted)
    line_dash="Type",   # Use different line styles for 'Type'
    facet_col="Cohort", # Create columns for each cohort
    facet_col_wrap=2,   # Wrap to 2 columns if you have many cohorts
    title="Actual vs. Predicted Values for Various Cohorts",
    labels={"Value": "Observed/Predicted Value"},
    height=500,
    width=900
)

# You can further customize the layout
fig.update_layout(
    hovermode="x unified", # Shows all values for a given date on hover
    legend_title_text="Series Type",
    margin=dict(l=20, r=20, t=60, b=20) # Adjust margins
)

# Update subplot titles
fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Cohort=", "Cohort ")))

fig.show()