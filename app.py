from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import os

app = Flask(__name__)

def load_model():
    """Load the trained model"""
    
    model_path = 'model/random_forest_model.pkl'
    
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully: {type(model).__name__}")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
    
try:
    with app.app_context():
        model = load_model()
except Exception as e:
    print(f"Failed to load model at startup: {e}")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get JSON data from request
        data = request.get_json()

        data = pd.DataFrame([data])  # Convert to DataFrame for consistency
            
        # Make prediction
        predictions = model.predict(data)
        
        # Format response
        response = {
            'predictions': predictions[0].tolist(),
            'success': True
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        info = {
            'model_type': type(model).__name__,
            'success': True
        }
        
        # Add feature count if available
        if hasattr(model, 'n_features_in_'):
            info['n_features'] = model.n_features_in_
        
        # Add classes if it's a classifier
        if hasattr(model, 'classes_'):
            info['classes'] = model.classes_.tolist()
        
        return jsonify(info)
    
    except Exception as e:
        print(f"Model info error: {str(e)}")
        return jsonify({
            'error': f'Failed to get model info: {str(e)}',
            'success': False
        }), 500