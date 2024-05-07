import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# Step 1: Read data from Excel file
data = pd.read_csv('bmi.csv')

# Step 2: Prepare data
# Assume your Excel file has columns 'Height', 'Weight', 'Gender', and 'BMI'

# Clean the data if necessary
data.dropna(inplace=True)

# Extract features and target variable
X = data[['Gender','Height', 'Weight']]
y = data['Index']

# Step 3: Train a Machine Learning Model
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the model
model = LinearRegression()
model.fit(X_train, y_train)

with open('bmi_model.pkl', 'wb') as f:
        pickle.dump(model, f)

print("Model created")

# # Step 4: Make Predictions
# predictions = model.predict(X_test)

# # Evaluate the model
# mse = mean_squared_error(y_test, predictions)
# print("Mean Squared Error:", mse)

# # Example prediction for a new data point
# # Replace the values below with actual values from your dataset
# new_data_point = pd.DataFrame({'Gender': [0],'Height': [170], 'Weight': [75]})  # Female
# predicted_bmi = model.predict(new_data_point)
# print("Predicted BMI:", predicted_bmi[0])
