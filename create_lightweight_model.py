"""
Create a lightweight model for testing deployment
"""

import pandas as pd
import lightgbm as lgb
import joblib
import re
from sklearn.model_selection import train_test_split

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

def create_lightweight_model():
    """Create a small model for testing"""
    print("Creating lightweight model...")
    
    # Create a small synthetic dataset
    sample_urls = [
        "https://www.google.com",
        "https://www.github.com", 
        "https://www.stackoverflow.com",
        "https://suspicious-site.com",
        "https://phishing-example.net",
        "https://fake-bank.com",
        "https://www.microsoft.com",
        "https://www.apple.com",
        "https://malicious-link.org",
        "https://www.amazon.com"
    ]
    
    # Generate more samples by varying the URLs
    urls = []
    labels = []
    
    for url in sample_urls:
        urls.append(url)
        # Simple heuristic: if contains suspicious words, mark as phishing
        if any(word in url.lower() for word in ['suspicious', 'phishing', 'fake', 'malicious']):
            labels.append(1.0)
        else:
            labels.append(0.0)
    
    # Duplicate and vary the data
    for _ in range(100):  # Create 1000 samples total
        for i, url in enumerate(sample_urls):
            # Add some variation
            if i % 2 == 0:
                urls.append(url + "/path")
            else:
                urls.append(url + "?param=value")
            labels.append(labels[i])
    
    print(f"Created {len(urls)} samples")
    
    # Extract features
    features = [extract_features(url) for url in urls]
    X = pd.DataFrame(features)
    y = pd.Series(labels)
    
    # Train a small model
    train_data = lgb.Dataset(X, label=y)
    
    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "boosting_type": "gbdt",
        "num_leaves": 8,  # Much smaller
        "learning_rate": 0.1,
        "feature_fraction": 0.9,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": -1,
        "num_boost_round": 50  # Much fewer rounds
    }
    
    model = lgb.train(params, train_data, num_boost_round=50)
    
    # Save the lightweight model
    model.save_model('model_lightweight.txt')
    joblib.dump(model, 'model_lightweight.pkl')
    
    print("Lightweight model created!")
    print("Files created:")
    print("- model_lightweight.txt")
    print("- model_lightweight.pkl")
    
    # Test the model
    test_url = "https://www.google.com"
    features = extract_features(test_url)
    X_test = pd.DataFrame([features])
    probability = model.predict(X_test)[0]
    prediction = "phishing" if probability > 0.5 else "safe"
    print(f"Test: {test_url} -> {prediction} ({probability:.3f})")

if __name__ == "__main__":
    create_lightweight_model()
