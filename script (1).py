# Create a sample dataset for POWERGRID project cost prediction
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data for POWERGRID projects
n_samples = 500

# Generate sample project data
project_types = ['Substation', 'Overhead Line', 'Underground Cable']
terrain_types = ['Plain', 'Hilly', 'Desert', 'Coastal']
weather_conditions = ['Normal', 'Extreme', 'Moderate']

# Create the basic dataset first
data = {
    'Project_ID': range(1, n_samples + 1),
    'Project_Type': np.random.choice(project_types, n_samples),
    'Terrain': np.random.choice(terrain_types, n_samples),
    'Weather_Risk': np.random.choice(weather_conditions, n_samples),
    'Original_Budget_Crores': np.random.normal(50, 20, n_samples),
    'Original_Timeline_Months': np.random.normal(24, 8, n_samples),
    'Vendor_Score': np.random.uniform(1, 5, n_samples),  # 1-5 rating
    'Material_Cost_Fluctuation': np.random.normal(0, 0.15, n_samples),  # % change
    'Labor_Availability': np.random.uniform(0.5, 1.0, n_samples),  # 0.5-1.0 scale
    'Regulatory_Delays_Days': np.random.exponential(30, n_samples),
}

# Create DataFrame first
df = pd.DataFrame(data)

# Now calculate final costs and timelines with realistic relationships
project_type_multiplier = df['Project_Type'].map({'Substation': 0.1, 'Overhead Line': 0.05, 'Underground Cable': 0.25})
terrain_multiplier = df['Terrain'].map({'Plain': 0.0, 'Hilly': 0.15, 'Desert': 0.1, 'Coastal': 0.08})
weather_multiplier = df['Weather_Risk'].map({'Normal': 0.0, 'Moderate': 0.05, 'Extreme': 0.15})
vendor_impact = (5 - df['Vendor_Score']) * 0.05
material_impact = np.abs(df['Material_Cost_Fluctuation']) * 0.5

# Calculate final costs with relationships and some noise
df['Final_Cost_Crores'] = df['Original_Budget_Crores'] * (1 + 
    project_type_multiplier + terrain_multiplier + weather_multiplier + 
    vendor_impact + material_impact + np.random.normal(0, 0.1, n_samples))

# Calculate final timeline with delays
regulatory_impact = df['Regulatory_Delays_Days'] / 365
labor_impact = (1 - df['Labor_Availability']) * 0.3
material_timeline_impact = np.abs(df['Material_Cost_Fluctuation']) * 0.2

df['Final_Timeline_Months'] = df['Original_Timeline_Months'] * (1 + 
    regulatory_impact + labor_impact + material_timeline_impact + 
    np.random.normal(0, 0.05, n_samples))

# Calculate overrun percentages
df['Cost_Overrun_Percent'] = ((df['Final_Cost_Crores'] - df['Original_Budget_Crores']) / 
                              df['Original_Budget_Crores'] * 100)

df['Timeline_Overrun_Percent'] = ((df['Final_Timeline_Months'] - df['Original_Timeline_Months']) / 
                                 df['Original_Timeline_Months'] * 100)

# Clean up negative values and extreme outliers
df = df[df['Original_Budget_Crores'] > 0]
df = df[df['Original_Timeline_Months'] > 0]
df = df[df['Final_Cost_Crores'] > 0]
df = df[df['Final_Timeline_Months'] > 0]

# Remove extreme outliers
df = df[df['Cost_Overrun_Percent'] < 200]  # Cap at 200% overrun
df = df[df['Timeline_Overrun_Percent'] < 200]

print("Sample POWERGRID Project Dataset Created!")
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset summary:")
print(df[['Original_Budget_Crores', 'Final_Cost_Crores', 'Cost_Overrun_Percent', 
          'Original_Timeline_Months', 'Final_Timeline_Months', 'Timeline_Overrun_Percent']].describe())

# Save the dataset
df.to_csv('powergrid_projects.csv', index=False)
print("\nDataset saved as 'powergrid_projects.csv'")