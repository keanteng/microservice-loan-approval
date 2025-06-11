import requests
import json

# API endpoint
API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/health")
    print("Health Check:", response.json())

def test_model_info():
    """Test model info endpoint"""
    response = requests.get(f"{API_URL}/model-info")
    print("Model Info:", response.json())

def test_single_prediction():
    """Test single prediction"""
    # Replace with your actual feature values
    data = {
            "person_age": -0.9535276419,
            "person_gender": 0,
            "person_education": 4,
            "person_income": -0.1096838991,
            "person_emp_exp": -0.7273538377,
            "person_home_ownership": 3,
            "loan_amnt": 4.0249087102,
            "loan_intent": 4,
            "loan_int_rate": 1.6830201042,
            "loan_percent_income": 4.0163495163,
            "cb_person_cred_hist_length": -0.7391003235,
            "credit_score": -1.4197983033,
            "previous_loan_defaults_on_file": 0
        }
    
    response = requests.post(f"{API_URL}/predict", json=data)
    print("Single Prediction:", response.json())

if __name__ == "__main__":
    print("Testing ML API...")
    
    try:
        test_health()
        test_model_info()
        test_single_prediction()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the service is running.")