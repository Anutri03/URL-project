"""
URL Phishing Detection API
A Flask API that detects phishing URLs using machine learning
"""

import os
import re
import pandas as pd
import lightgbm as lgb
import joblib
from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for model and feature names
model = None
feature_names = None

def extract_features(url):
    """Extract lexical features from URL"""
    try:
        return {
            "url_length": len(url),
            "path_length": len(url.split("//")[-1].split("/", 1)[-1]) if "/" in url.split("//")[-1] else 0,
            "query_length": len(url.split("?")[-1]) if "?" in url else 0,
            "num_digits": sum(c.isdigit() for c in url),
            "num_letters": sum(c.isalpha() for c in url),
            "num_special": sum(not c.isalnum() for c in url),
            "count_dot": min(url.count('.'), 4),  # capped at 4
            "count_dash": url.count('-'),
            "count_slash": url.count('/'),
            "count_at": url.count('@'),
            "count_qmark": url.count('?'),
            "count_percent": url.count('%'),
            "count_equal": url.count('='),
            "has_https": int("https" in url.lower()),
            "has_ip": int(re.match(r"^https?:\/\/\d+\.\d+\.\d+\.\d+", url) is not None)
        }
    except Exception as e:
        logger.error(f"Error extracting features from URL {url}: {str(e)}")
        return None

def load_model():
    """Load the trained model"""
    global model, feature_names
    
    try:
        # Try to load the main model first
        if os.path.exists('model.txt'):
            logger.info("Loading model.txt...")
            model = lgb.Booster(model_file='model.txt')
        elif os.path.exists('phishing_model.pkl'):
            logger.info("Loading phishing_model.pkl...")
            model = joblib.load('phishing_model.pkl')
        elif os.path.exists('model_clean.pkl'):
            logger.info("Loading model_clean.pkl...")
            model = joblib.load('model_clean.pkl')
        elif os.path.exists('model_lightweight.txt'):
            logger.info("Loading model_lightweight.txt...")
            model = lgb.Booster(model_file='model_lightweight.txt')
        elif os.path.exists('model_lightweight.pkl'):
            logger.info("Loading model_lightweight.pkl...")
            model = joblib.load('model_lightweight.pkl')
        else:
            logger.error("No model file found!")
            return False
            
        # Try to load feature names if available
        if os.path.exists('feature_names.joblib'):
            feature_names = joblib.load('feature_names.joblib')
            logger.info(f"Loaded feature names: {feature_names}")
        else:
            # Default feature names
            feature_names = [
                "url_length", "path_length", "query_length", "num_digits", "num_letters",
                "num_special", "count_dot", "count_dash", "count_slash", "count_at",
                "count_qmark", "count_percent", "count_equal", "has_https", "has_ip"
            ]
            logger.info("Using default feature names")
            
        logger.info("Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def predict_url(url):
    """Predict if a URL is phishing or safe"""
    global model, feature_names
    
    try:
        # Extract features
        features = extract_features(url)
        if features is None:
            return None
            
        # Convert to DataFrame
        X = pd.DataFrame([features])
        
        # Make prediction
        if hasattr(model, 'predict'):
            # LightGBM model
            probability = model.predict(X)[0]
        else:
            # Scikit-learn model
            probability = model.predict_proba(X)[0][1]
            
        # Determine prediction
        prediction = "phishing" if probability > 0.5 else "safe"
        confidence = abs(probability - 0.5) * 2  # Scale to 0-1
        
        return {
            "url": url,
            "prediction": prediction,
            "probability": float(probability),
            "confidence": float(confidence),
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error predicting URL {url}: {str(e)}")
        return None

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    global model
    
    model_status = "loaded" if model is not None else "not loaded"
    
    return jsonify({
        "status": "API is running",
        "model_status": model_status,
        "version": "1.0.0",
        "endpoints": {
            "/": "Health check",
            "/predict": "Single URL prediction",
            "/predict_batch": "Batch URL prediction",
            "/features": "Extract features from URL"
        }
    })

@app.route('/predict', methods=['POST'])
def predict_single():
    """Predict a single URL"""
    global model
    
    if model is None:
        return jsonify({
            "error": "Model not loaded",
            "status": "error"
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "Missing 'url' field in request",
                "status": "error"
            }), 400
            
        url = data['url']
        
        if not url or not isinstance(url, str):
            return jsonify({
                "error": "Invalid URL provided",
                "status": "error"
            }), 400
            
        result = predict_url(url)
        
        if result is None:
            return jsonify({
                "error": "Failed to process URL",
                "status": "error"
            }), 500
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in predict_single: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "error"
        }), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Predict multiple URLs"""
    global model
    
    if model is None:
        return jsonify({
            "error": "Model not loaded",
            "status": "error"
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                "error": "Missing 'urls' field in request",
                "status": "error"
            }), 400
            
        urls = data['urls']
        
        if not isinstance(urls, list):
            return jsonify({
                "error": "'urls' must be a list",
                "status": "error"
            }), 400
            
        if len(urls) > 100:
            return jsonify({
                "error": "Maximum 100 URLs allowed per request",
                "status": "error"
            }), 400
            
        results = []
        for url in urls:
            if not url or not isinstance(url, str):
                results.append({
                    "url": url,
                    "error": "Invalid URL",
                    "status": "error"
                })
                continue
                
            result = predict_url(url)
            if result is None:
                results.append({
                    "url": url,
                    "error": "Failed to process URL",
                    "status": "error"
                })
            else:
                results.append(result)
                
        return jsonify({
            "results": results,
            "total_processed": len(results),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error in predict_batch: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "error"
        }), 500

@app.route('/features', methods=['POST'])
def extract_url_features():
    """Extract features from a URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "Missing 'url' field in request",
                "status": "error"
            }), 400
            
        url = data['url']
        
        if not url or not isinstance(url, str):
            return jsonify({
                "error": "Invalid URL provided",
                "status": "error"
            }), 400
            
        features = extract_features(url)
        
        if features is None:
            return jsonify({
                "error": "Failed to extract features",
                "status": "error"
            }), 500
            
        return jsonify({
            "url": url,
            "features": features,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error in extract_url_features: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "error"
        }), 500

# Load model on startup
with app.app_context():
    if not load_model():
        logger.error("Failed to load model on startup!")
    else:
        logger.info("Model loaded successfully on startup!")

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
