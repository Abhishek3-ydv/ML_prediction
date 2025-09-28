# Create a sample dataset for POWERGRID project cost prediction
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
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

# Create the dataset
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

# Create target variables with some realistic relationships
cost_multiplier = 1.0
timeline_multiplier = 1.0

for i in range(n_samples):
    # Cost overrun factors
    if data['Project_Type'][i] == 'Underground Cable':
        cost_multiplier += 0.2
    if data['Terrain'][i] == 'Hilly':
        cost_multiplier += 0.15
    if data['Weather_Risk'][i] == 'Extreme':
        cost_multiplier += 0.1
    if data['Vendor_Score'][i] < 2.5:
        cost_multiplier += 0.2
    
    # Timeline delay factors
    if data['Regulatory_Delays_Days'][i] > 50:
        timeline_multiplier += 0.3
    if data['Labor_Availability'][i] < 0.7:
        timeline_multiplier += 0.2
    if data['Material_Cost_Fluctuation'][i] > 0.1:
        timeline_multiplier += 0.15
    
    # Reset for next iteration
    cost_multiplier = 1.0
    timeline_multiplier = 1.0

# Calculate final costs and timelines with some noise
data['Final_Cost_Crores'] = data['Original_Budget_Crores'] * (1 + 
    (data['Project_Type'].map({'Substation': 0.1, 'Overhead Line': 0.05, 'Underground Cable': 0.25}) +
     data['Terrain'].map({'Plain': 0.0, 'Hilly': 0.15, 'Desert': 0.1, 'Coastal': 0.08}) +
     data['Weather_Risk'].map({'Normal': 0.0, 'Moderate': 0.05, 'Extreme': 0.15}) +
     (5 - data['Vendor_Score']) * 0.05 +
     np.abs(data['Material_Cost_Fluctuation']) * 0.5) + 
    np.random.normal(0, 0.1, n_samples))

data['Final_Timeline_Months'] = data['Original_Timeline_Months'] * (1 + 
    (data['Regulatory_Delays_Days'] / 365) +
    (1 - data['Labor_Availability']) * 0.3 +
    np.abs(data['Material_Cost_Fluctuation']) * 0.2 +
    np.random.normal(0, 0.05, n_samples))

# Calculate overrun percentages
data['Cost_Overrun_Percent'] = ((data['Final_Cost_Crores'] - data['Original_Budget_Crores']) / 
                                data['Original_Budget_Crores'] * 100)

data['Timeline_Overrun_Percent'] = ((data['Final_Timeline_Months'] - data['Original_Timeline_Months']) / 
                                   data['Original_Timeline_Months'] * 100)

# Create DataFrame
df = pd.DataFrame(data)

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
print(df.describe())

# Save the dataset
df.to_csv('powergrid_projects.csv', index=False)
print("\nDataset saved as 'powergrid_projects.csv'")