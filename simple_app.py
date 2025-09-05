from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Global variable to store the model
model = None

def extract_features(url):
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
        print("Loading model_clean.pkl...")
        model = joblib.load('model_clean.pkl')
        print(f"Model loaded successfully: {type(model)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "URL Phishing Detection API",
        "status": "running",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if a URL is phishing or safe"""
    try:
        if model is None:
            return jsonify({
                "error": "Model not loaded",
                "status": "error"
            }), 500
        
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
            "confidence": float(abs(probability - 0.5) * 2),
            "status": "success"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
