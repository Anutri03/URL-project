from flask import Flask, request, jsonify
import pandas as pd
import lightgbm as lgb
import re
import joblib
import os
from typing import Dict, Any

app = Flask(__name__)

# Global variable to store the model
model = None

def extract_features(url: str) -> Dict[str, Any]:
    """Extract lexical features from URL"""
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

def load_model():
    """Load the trained model"""
    global model
    try:
        print("Starting model loading...")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir('.')}")
        
        # Try to load from clean pickle first (most reliable)
        if os.path.exists('model_clean.pkl'):
            print("Loading model_clean.pkl...")
            model = joblib.load('model_clean.pkl')
            print(f"Model type: {type(model)}")
        # Try to load from phishing_model.pkl (as requested)
        elif os.path.exists('phishing_model.pkl'):
            print("Loading phishing_model.pkl...")
            try:
                model_dict = joblib.load('phishing_model.pkl')
                if isinstance(model_dict, dict) and 'model' in model_dict:
                    model = model_dict['model']
                    print(f"Extracted model type: {type(model)}")
                else:
                    model = model_dict
                    print(f"Model type: {type(model)}")
            except Exception as e:
                print(f"Error loading phishing_model.pkl: {e}")
                print("Falling back to model_clean.pkl...")
                if os.path.exists('model_clean.pkl'):
                    model = joblib.load('model_clean.pkl')
                    print(f"Fallback model type: {type(model)}")
                else:
                    raise e
        # Try to load from LightGBM format
        elif os.path.exists('model.txt'):
            print("Loading model.txt...")
            model = lgb.Booster(model_file='model.txt')
            print(f"Model type: {type(model)}")
        # Try to load from joblib format
        elif os.path.exists('model.joblib'):
            print("Loading model.joblib...")
            model = joblib.load('model.joblib')
            print(f"Model type: {type(model)}")
        else:
            raise FileNotFoundError("No model file found")
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        model = None

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        "message": "URL Phishing Detection API",
        "status": "running",
        "model_loaded": model is not None,
        "model_status": model_status,
        "available_files": {
            "model_clean.pkl": os.path.exists('model_clean.pkl'),
            "model.txt": os.path.exists('model.txt'),
            "phishing_model.pkl": os.path.exists('phishing_model.pkl')
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if a URL is phishing or safe"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                "error": "Model not loaded",
                "status": "error"
            }), 500
        
        # Get URL from request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                "error": "URL is required",
                "status": "error"
            }), 400
        
        url = data['url']
        
        # Validate URL format
        if not isinstance(url, str) or len(url.strip()) == 0:
            return jsonify({
                "error": "Invalid URL format",
                "status": "error"
            }), 400
        
        # Extract features
        features = extract_features(url)
        X_new = pd.DataFrame([features])
        
        # Make prediction
        probability = model.predict(X_new)[0]
        
        # Determine prediction
        is_phishing = probability > 0.5
        prediction = "phishing" if is_phishing else "safe"
        
        # Prepare response
        response = {
            "url": url,
            "prediction": prediction,
            "probability": float(probability),
            "confidence": float(abs(probability - 0.5) * 2),  # Confidence as distance from 0.5
            "status": "success"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Predict multiple URLs at once"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                "error": "Model not loaded",
                "status": "error"
            }), 500
        
        # Get URLs from request
        data = request.get_json()
        if not data or 'urls' not in data:
            return jsonify({
                "error": "URLs array is required",
                "status": "error"
            }), 400
        
        urls = data['urls']
        
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({
                "error": "URLs must be a non-empty array",
                "status": "error"
            }), 400
        
        # Limit batch size to prevent abuse
        if len(urls) > 100:
            return jsonify({
                "error": "Maximum 100 URLs allowed per batch",
                "status": "error"
            }), 400
        
        results = []
        for url in urls:
            try:
                if not isinstance(url, str) or len(url.strip()) == 0:
                    results.append({
                        "url": url,
                        "error": "Invalid URL format"
                    })
                    continue
                
                # Extract features
                features = extract_features(url)
                X_new = pd.DataFrame([features])
                
                # Make prediction
                probability = model.predict(X_new)[0]
                
                # Determine prediction
                is_phishing = probability > 0.5
                prediction = "phishing" if is_phishing else "safe"
                
                results.append({
                    "url": url,
                    "prediction": prediction,
                    "probability": float(probability),
                    "confidence": float(abs(probability - 0.5) * 2)
                })
                
            except Exception as e:
                results.append({
                    "url": url,
                    "error": f"Prediction failed: {str(e)}"
                })
        
        return jsonify({
            "results": results,
            "total_processed": len(results),
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Batch prediction failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/features', methods=['POST'])
def get_features():
    """Get extracted features for a URL (for debugging/analysis)"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                "error": "URL is required",
                "status": "error"
            }), 400
        
        url = data['url']
        
        if not isinstance(url, str) or len(url.strip()) == 0:
            return jsonify({
                "error": "Invalid URL format",
                "status": "error"
            }), 400
        
        features = extract_features(url)
        
        return jsonify({
            "url": url,
            "features": features,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Feature extraction failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/debug', methods=['GET'])
def debug():
    """Debug endpoint to check model loading status"""
    try:
        debug_info = {
            "model_loaded": model is not None,
            "model_type": str(type(model)) if model else None,
            "current_directory": os.getcwd(),
            "files_in_directory": os.listdir('.'),
            "model_files": {
                "model_clean.pkl": os.path.exists('model_clean.pkl'),
                "model.txt": os.path.exists('model.txt'),
                "phishing_model.pkl": os.path.exists('phishing_model.pkl')
            }
        }
        
        # Try to load model if not loaded
        if model is None:
            debug_info["loading_attempt"] = "Attempting to load model..."
            try:
                load_model()
                debug_info["loading_result"] = "Model loading attempted"
                debug_info["model_loaded_after_attempt"] = model is not None
            except Exception as e:
                debug_info["loading_error"] = str(e)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({
            "error": f"Debug failed: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
