from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to store the model
model = None

def load_model():
    """Load the trained model"""
    global model
    import os
    
    model_path = 'random_forest_model.pkl'
    
    # Check if file exists
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at: {os.path.abspath(model_path)}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Files in current directory: {os.listdir('.')}")
        return False
    
    # Check file size
    file_size = os.path.getsize(model_path)
    logger.info(f"Model file size: {file_size} bytes")
    
    if file_size == 0:
        logger.error("Model file is empty")
        return False
    
    try:
        model = joblib.load(model_path)
        logger.info(f"Model loaded successfully: {type(model).__name__}")
        
        # Verify model has required methods
        if hasattr(model, 'predict'):
            logger.info("Model has predict method")
        else:
            logger.warning("Model doesn't have predict method")
            
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        return False
    
try:
    with app.app_context():
        load_model()
except Exception as e:
    logger.error(f"Failed to load model at startup: {e}")


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
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Handle different input formats
        if 'features' in data:
            # Single prediction: {"features": [1, 2, 3, 4]}
            features = np.array(data['features']).reshape(1, -1)
        elif 'data' in data:
            # Multiple predictions: {"data": [[1,2,3,4], [5,6,7,8]]}
            features = np.array(data['data'])
        elif isinstance(data, dict) and all(isinstance(v, (int, float)) for v in data.values()):
            # Handle key-value format like your input_data.json
            # Convert dict values to array in consistent order
            feature_names = sorted(data.keys())  # Sort for consistency
            features = np.array([data[key] for key in feature_names]).reshape(1, -1)
            logger.info(f"Processing dict input with features: {feature_names}")
        else:
            # Direct array: [[1,2,3,4]] or [1,2,3,4]
            features = np.array(data)
            if features.ndim == 1:
                features = features.reshape(1, -1)
        
        # Validate feature count if model supports it
        if hasattr(model, 'n_features_in_'):
            expected_features = model.n_features_in_
            if features.shape[1] != expected_features:
                return jsonify({
                    'error': f'Expected {expected_features} features, got {features.shape[1]}',
                    'success': False
                }), 400
        
        # Make prediction
        predictions = model.predict(features)
        
        # Get prediction probabilities if available (for classifiers)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            try:
                probabilities = model.predict_proba(features).tolist()
            except:
                pass
        
        # Format response
        response = {
            'predictions': predictions.tolist(),
            'success': True
        }
        
        if probabilities is not None:
            response['probabilities'] = probabilities
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
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
        logger.error(f"Model info error: {str(e)}")
        return jsonify({
            'error': f'Failed to get model info: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.error("Failed to load model. Exiting.")
        exit(1)