import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Data
models = ["Linear Regression", "Random Forest"]
mae_values = [12.5, 8.2]  # MAE in percentage
r2_values = [67, 82]  # R² converted to percentage (0.67 -> 67%, 0.82 -> 82%)

# Create DataFrame for easier plotting
df = pd.DataFrame({
    'Model': models + models,
    'Metric': ['MAE'] * 2 + ['R²'] * 2,
    'Value': mae_values + r2_values
})

# Create grouped bar chart
fig = go.Figure()

# Add MAE bars
fig.add_trace(go.Bar(
    name='MAE (Lower Better)',
    x=models,
    y=mae_values,
    marker_color='#DB4545',  # Red color for MAE (bad performance indicator)
    text=[f'{val}%' for val in mae_values],
    textposition='auto',
))

# Add R² bars
fig.add_trace(go.Bar(
    name='R² (Higher Better)',
    x=models,
    y=r2_values,
    marker_color='#1FB8CD',  # Cyan color for R² (good performance indicator)
    text=[f'{val}%' for val in r2_values],
    textposition='auto',
))

# Update layout
fig.update_layout(
    title='ML Model Accuracy Comparison',
    xaxis_title='Models',
    yaxis_title='Percentage (%)',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update traces
fig.update_traces(cliponaxis=False)

# Update x-axis labels to be shorter
fig.update_xaxes(ticktext=['Linear Reg', 'Random Forest'], tickvals=models)

# Save as PNG and SVG
fig.write_image('model_comparison.png')
fig.write_image('model_comparison.svg', format='svg')

fig.show()