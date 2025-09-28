import plotly.graph_objects as go

# Data from provided JSON
factors = ["Material Cost Fluctuation", "Vendor Score", "Underground Cable Projects", "Regulatory Delays", "Hilly Terrain"]
importance = [0.285, 0.198, 0.156, 0.132, 0.105]

# Abbreviate factor names to meet 15 character limit
abbreviated_factors = ["Material Cost", "Vendor Score", "Underground", "Regulatory", "Hilly Terrain"]

# Brand colors from theme
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Create horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        x=importance,
        y=abbreviated_factors,
        orientation='h',
        marker_color=colors,
        text=[f'{val:.3f}' for val in importance],
        textposition='inside',
        textfont=dict(color='white', size=14)
    )
])

# Update layout
fig.update_layout(
    title='Top Cost Overrun Factors',
    xaxis_title='Importance',
    yaxis_title='Factor',
    showlegend=False
)

# Update traces for better display
fig.update_traces(cliponaxis=False)

# Update x-axis to show values with 3 decimal places
fig.update_xaxes(tickformat='.3f')

# Save as both PNG and SVG
fig.write_image('cost_overrun_factors.png')
fig.write_image('cost_overrun_factors.svg', format='svg')

print("Chart saved as cost_overrun_factors.png and cost_overrun_factors.svg")