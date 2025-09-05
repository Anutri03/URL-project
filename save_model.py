"""
Script to save the trained LightGBM model for deployment
Run this after training your model to save it in the correct format
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

def train_and_save_model():
    """Train the model and save it for deployment"""
    print("Loading dataset...")
    df = pd.read_csv("url_dataset_balanced.csv")
    print(f"Dataset shape: {df.shape}")
    
    print("Extracting features...")
    features = df['url'].apply(extract_features)
    X = pd.DataFrame(features.tolist())
    y = df['label']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training LightGBM model...")
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
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=100)]
    )
    
    print("Saving model...")
    # Save model in LightGBM format
    model.save_model('model.txt')
    
    # Also save using joblib for compatibility
    joblib.dump(model, 'model.joblib')
    
    # Save feature names for reference
    feature_names = X_train.columns.tolist()
    joblib.dump(feature_names, 'feature_names.joblib')
    
    print("Model saved successfully!")
    print(f"Model files created:")
    print(f"- model.txt (LightGBM format)")
    print(f"- model.joblib (Joblib format)")
    print(f"- feature_names.joblib (Feature names)")
    
    # Test the saved model
    print("\nTesting saved model...")
    test_url = "https://www.plugintoai.com"
    features = extract_features(test_url)
    X_test = pd.DataFrame([features])
    probability = model.predict(X_test)[0]
    prediction = "phishing" if probability > 0.5 else "safe"
    print(f"Test URL: {test_url}")
    print(f"Prediction: {prediction} (Probability: {probability:.2f})")

if __name__ == "__main__":
    train_and_save_model()
