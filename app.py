import os
import re
import pandas as pd
import numpy as np
import joblib
import lightgbm as lgb
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

app = Flask(__name__)

# Global variables for model and feature extractor
model = None
extract_features = None

def extract_features_func(url):
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
    global model, extract_features
    
    try:
        # Try to load the saved model
        if os.path.exists("phishing_model.pkl"):
            package = joblib.load("phishing_model.pkl")
            model = package["model"]
            extract_features = package["extract_features"]
            print("✅ Model loaded successfully from phishing_model.pkl")
        else:
            # If no saved model, train a new one
            print("⚠️ No saved model found. Training new model...")
            train_and_save_model()
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("⚠️ Training new model...")
        train_and_save_model()

def train_and_save_model():
    """Train and save the model"""
    global model, extract_features
    
    try:
        # Load dataset
        df = pd.read_csv("url_dataset_balanced.csv")
        print(f"Dataset loaded: {df.shape}")
        
        # Extract features
        features = df['url'].apply(extract_features_func)
        X = pd.DataFrame(features.tolist())
        y = df['label']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train LightGBM model
        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test)
        
        params = {
            "objective": "binary",
            "metric": "binary_logloss",
            "boosting_type": "gbdt",
            "num_leaves": 64,
            "learning_rate": 0.05,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1,
        }
        
        model = lgb.train(
            params,
            train_data,
            valid_sets=[train_data, test_data],
            num_boost_round=1000,
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
        )
        
        # Save model
        package = {
            "model": model,
            "extract_features": extract_features_func
        }
        joblib.dump(package, "phishing_model.pkl")
        extract_features = extract_features_func
        
        print("✅ Model trained and saved successfully")
        
    except Exception as e:
        print(f"❌ Error training model: {e}")
        raise e

def predict_url(url):
    """Predict if URL is phishing or safe"""
    try:
        # Extract features
        features = extract_features(url)
        X_new = pd.DataFrame([features])
        
        # Predict probability
        prob = model.predict(X_new)[0]
        
        # Determine prediction
        prediction = "phishing" if prob > 0.5 else "safe"
        confidence = max(prob, 1 - prob)
        
        return {
            "url": url,
            "prediction": prediction,
            "probability": float(prob),
            "confidence": float(confidence),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Prediction failed: {str(e)}",
            "status": "error"
        }

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "URL Phishing Detection API is running",
        "model_loaded": model is not None,
        "endpoints": {
            "predict": "POST /predict - Single URL prediction",
            "predict_batch": "POST /predict_batch - Batch URL prediction",
            "features": "POST /features - Extract URL features"
        }
    })

@app.route("/predict", methods=["POST"])
def predict_single():
    """Single URL prediction endpoint"""
    try:
        data = request.get_json()
        
        if not data or "url" not in data:
            return jsonify({
                "error": "Missing 'url' field in request body",
                "status": "error"
            }), 400
        
        url = data["url"]
        
        if not isinstance(url, str) or not url.strip():
            return jsonify({
                "error": "URL must be a non-empty string",
                "status": "error"
            }), 400
        
        result = predict_url(url.strip())
        
        if result["status"] == "error":
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    """Batch URL prediction endpoint"""
    try:
        data = request.get_json()
        
        if not data or "urls" not in data:
            return jsonify({
                "error": "Missing 'urls' field in request body",
                "status": "error"
            }), 400
        
        urls = data["urls"]
        
        if not isinstance(urls, list):
            return jsonify({
                "error": "URLs must be a list",
                "status": "error"
            }), 400
        
        if len(urls) > 100:
            return jsonify({
                "error": "Maximum 100 URLs allowed per batch",
                "status": "error"
            }), 400
        
        if not urls:
            return jsonify({
                "error": "URLs list cannot be empty",
                "status": "error"
            }), 400
        
        results = []
        for url in urls:
            if not isinstance(url, str) or not url.strip():
                results.append({
                    "url": url,
                    "error": "URL must be a non-empty string",
                    "status": "error"
                })
            else:
                result = predict_url(url.strip())
                results.append(result)
        
        return jsonify({
            "results": results,
            "total": len(results),
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

@app.route("/features", methods=["POST"])
def extract_url_features():
    """Extract features from URL"""
    try:
        data = request.get_json()
        
        if not data or "url" not in data:
            return jsonify({
                "error": "Missing 'url' field in request body",
                "status": "error"
            }), 400
        
        url = data["url"]
        
        if not isinstance(url, str) or not url.strip():
            return jsonify({
                "error": "URL must be a non-empty string",
                "status": "error"
            }), 400
        
        features = extract_features(url.strip())
        
        return jsonify({
            "url": url.strip(),
            "features": features,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == "__main__":
    # Load model on startup
    load_model()
    
    # Get port from environment variable (for Hugging Face Spaces)
    port = int(os.environ.get("PORT", 7860))
    
    # Run the app
    app.run(host="0.0.0.0", port=port, debug=False)
