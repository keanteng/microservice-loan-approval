import joblib
import pandas as pd

model = joblib.load('model/random_forest_model.pkl')

# 1. Check if model has feature names (if trained with pandas DataFrame)
if hasattr(model, 'feature_names_in_'):
    print("Expected feature names:")
    print(model.feature_names_in_)

# 2. Check number of features expected
if hasattr(model, 'n_features_in_'):
    print(f"\nNumber of features expected: {model.n_features_in_}")

# 3. Get model parameters and info
print(f"\nModel type: {type(model)}")
print(f"Model parameters: {model.get_params()}")

# 4. If it's a RandomForest, get additional info
if hasattr(model, 'n_estimators'):
    print(f"Number of trees: {model.n_estimators}")
    print(f"Number of classes: {len(model.classes_) if hasattr(model, 'classes_') else 'N/A (regression)'}")

# 5. Create a sample input to test the expected format
# Replace with actual feature count and names if known
sample_input = [[0] * model.n_features_in_] if hasattr(model, 'n_features_in_') else [[0, 0, 0]]  # adjust size
print(f"\nSample prediction with {len(sample_input[0])} features:")
try:
    prediction = model.predict(sample_input)
    print(f"Prediction shape: {prediction.shape}")
    print(f"Sample prediction: {prediction}")
except Exception as e:
    print(f"Error: {e}")