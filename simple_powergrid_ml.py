# SIMPLE VERSION - POWERGRID ML Project for Absolute Beginners
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
