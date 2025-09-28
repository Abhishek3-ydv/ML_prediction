# Create the complete beginner ML project code for POWERGRID cost prediction
project_code = '''# POWERGRID Project Cost and Timeline Prediction - ML Beginner Project
# Smart India Hackathon (SIH) Project

# Step 1: Import Required Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load the Dataset
print("Loading POWERGRID project dataset...")
df = pd.read_csv('powergrid_projects.csv')
print(f"Dataset loaded successfully! Shape: {df.shape}")

# Step 3: Explore the Data
print("\\nFirst 5 rows of data:")
print(df.head())

print("\\nDataset Info:")
print(df.info())

print("\\nBasic Statistics:")
print(df.describe())

# Step 4: Data Preprocessing
# Convert categorical variables to numbers
print("\\nPreprocessing data...")

# One-hot encoding for categorical variables
df_encoded = pd.get_dummies(df, columns=['Project_Type', 'Terrain', 'Weather_Risk'])

# Select features for prediction
feature_columns = [col for col in df_encoded.columns if col not in 
                  ['Project_ID', 'Final_Cost_Crores', 'Final_Timeline_Months', 
                   'Cost_Overrun_Percent', 'Timeline_Overrun_Percent']]

X = df_encoded[feature_columns]  # Features
y_cost = df_encoded['Cost_Overrun_Percent']  # Target for cost prediction
y_timeline = df_encoded['Timeline_Overrun_Percent']  # Target for timeline prediction

print(f"Features shape: {X.shape}")
print(f"Features selected: {feature_columns}")

# Step 5: Split Data into Training and Testing Sets
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42)

X_train_time, X_test_time, y_time_train, y_time_test = train_test_split(
    X, y_timeline, test_size=0.2, random_state=42)

print(f"\\nTraining set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

# Step 6: Train Machine Learning Models

print("\\n" + "="*50)
print("TRAINING MODELS FOR COST OVERRUN PREDICTION")
print("="*50)

# Model 1: Linear Regression for Cost
cost_lr_model = LinearRegression()
cost_lr_model.fit(X_train, y_cost_train)
cost_lr_pred = cost_lr_model.predict(X_test)

# Model 2: Random Forest for Cost
cost_rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
cost_rf_model.fit(X_train, y_cost_train)
cost_rf_pred = cost_rf_model.predict(X_test)

print("\\n" + "="*50)
print("TRAINING MODELS FOR TIMELINE OVERRUN PREDICTION")
print("="*50)

# Model 1: Linear Regression for Timeline
time_lr_model = LinearRegression()
time_lr_model.fit(X_train_time, y_time_train)
time_lr_pred = time_lr_model.predict(X_test_time)

# Model 2: Random Forest for Timeline
time_rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
time_rf_model.fit(X_train_time, y_time_train)
time_rf_pred = time_rf_model.predict(X_test_time)

# Step 7: Evaluate Model Performance
print("\\n" + "="*60)
print("MODEL EVALUATION RESULTS")
print("="*60)

print("\\nCOST OVERRUN PREDICTION:")
print("-" * 30)
cost_lr_mae = mean_absolute_error(y_cost_test, cost_lr_pred)
cost_lr_r2 = r2_score(y_cost_test, cost_lr_pred)
cost_rf_mae = mean_absolute_error(y_cost_test, cost_rf_pred)
cost_rf_r2 = r2_score(y_cost_test, cost_rf_pred)

print(f"Linear Regression - MAE: {cost_lr_mae:.2f}%, R²: {cost_lr_r2:.3f}")
print(f"Random Forest     - MAE: {cost_rf_mae:.2f}%, R²: {cost_rf_r2:.3f}")

print("\\nTIMELINE OVERRUN PREDICTION:")
print("-" * 32)
time_lr_mae = mean_absolute_error(y_time_test, time_lr_pred)
time_lr_r2 = r2_score(y_time_test, time_lr_pred)
time_rf_mae = mean_absolute_error(y_time_test, time_rf_pred)
time_rf_r2 = r2_score(y_time_test, time_rf_pred)

print(f"Linear Regression - MAE: {time_lr_mae:.2f}%, R²: {time_lr_r2:.3f}")
print(f"Random Forest     - MAE: {time_rf_mae:.2f}%, R²: {time_rf_r2:.3f}")

# Step 8: Feature Importance Analysis (Hotspot Identification)
print("\\n" + "="*60)
print("HOTSPOT ANALYSIS - MOST IMPORTANT FACTORS")
print("="*60)

# Get feature importance from Random Forest models
cost_importance = cost_rf_model.feature_importances_
time_importance = time_rf_model.feature_importances_

# Create feature importance dataframe
importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Cost_Importance': cost_importance,
    'Timeline_Importance': time_importance
})

# Sort by importance
cost_hotspots = importance_df.sort_values('Cost_Importance', ascending=False).head(5)
time_hotspots = importance_df.sort_values('Timeline_Importance', ascending=False).head(5)

print("\\nTOP 5 FACTORS AFFECTING COST OVERRUNS:")
print("-" * 40)
for i, row in cost_hotspots.iterrows():
    print(f"{row['Feature']:<30}: {row['Cost_Importance']:.3f}")

print("\\nTOP 5 FACTORS AFFECTING TIMELINE DELAYS:")
print("-" * 42)
for i, row in time_hotspots.iterrows():
    print(f"{row['Feature']:<30}: {row['Timeline_Importance']:.3f}")

# Step 9: Make Predictions on New Data
print("\\n" + "="*60)
print("SAMPLE PREDICTIONS FOR NEW PROJECTS")
print("="*60)

# Create a sample new project
sample_project = X_test.iloc[0:1].copy()  # Take first test sample
print("\\nSample Project Details:")
for col in feature_columns:
    if sample_project[col].iloc[0] == 1.0:
        print(f"{col}: Yes")
    elif sample_project[col].iloc[0] == 0.0:
        print(f"{col}: No")
    else:
        print(f"{col}: {sample_project[col].iloc[0]:.2f}")

# Make predictions
sample_cost_pred = cost_rf_model.predict(sample_project)[0]
sample_time_pred = time_rf_model.predict(sample_project)[0]

print(f"\\nPREDICTIONS:")
print(f"Expected Cost Overrun: {sample_cost_pred:.1f}%")
print(f"Expected Timeline Delay: {sample_time_pred:.1f}%")

# Risk Assessment
risk_level = "LOW"
if sample_cost_pred > 50 or sample_time_pred > 30:
    risk_level = "HIGH"
elif sample_cost_pred > 30 or sample_time_pred > 20:
    risk_level = "MEDIUM"

print(f"Overall Risk Level: {risk_level}")

print("\\n" + "="*60)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("The ML models are now ready to predict POWERGRID project risks!")
print("="*60)
'''

# Save the complete project code
with open('powergrid_ml_project.py', 'w') as f:
    f.write(project_code)

print("Complete ML project code saved as 'powergrid_ml_project.py'")
print("This file contains the full beginner-friendly ML project for POWERGRID cost and timeline prediction!")

# Also create a simple version for absolute beginners
simple_code = '''# SIMPLE VERSION - POWERGRID ML Project for Absolute Beginners
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv('powergrid_projects.csv')
print("Data loaded!")

# Prepare data (use only numeric columns)
X = df[['Original_Budget_Crores', 'Vendor_Score', 'Labor_Availability']]
y = df['Cost_Overrun_Percent']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Check accuracy
error = mean_absolute_error(y_test, predictions)
print(f"Average prediction error: {error:.1f}%")

# Predict for a new project
new_project = [[50, 3.5, 0.8]]  # Budget=50cr, Vendor=3.5/5, Labor=80%
prediction = model.predict(new_project)
print(f"Predicted cost overrun: {prediction[0]:.1f}%")
'''

with open('simple_powergrid_ml.py', 'w') as f:
    f.write(simple_code)

print("\nSimple version saved as 'simple_powergrid_ml.py'")
print("This is perfect for absolute ML beginners!")

print("\nFiles created:")
print("1. powergrid_projects.csv - Sample dataset")
print("2. powergrid_ml_project.py - Complete ML project")
print("3. simple_powergrid_ml.py - Simple version for beginners")