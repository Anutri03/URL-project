"""
Script to train and save the URL phishing detection model
This script will be run during deployment to create the model file
"""

import pandas as pd
import numpy as np
import re
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

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

def train_model():
    """Train the LightGBM model"""
    print("Loading dataset...")
    df = pd.read_csv("url_dataset_balanced.csv")
    print(f"Dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")
    
    # Extract features
    print("Extracting features...")
    features = df['url'].apply(extract_features)
    X = pd.DataFrame(features.tolist())
    y = df['label']
    
    # Train-test split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train LightGBM model
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
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, model.predict(X_test))
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, extract_features

def save_model(model, extract_features_func, filename="phishing_model.pkl"):
    """Save the trained model and feature extractor"""
    package = {
        "model": model,
        "extract_features": extract_features_func
    }
    joblib.dump(package, filename)
    print(f"✅ Model saved as {filename}")

def main():
    """Main function"""
    try:
        print("🚀 Starting model training...")
        model, extract_features_func = train_model()
        save_model(model, extract_features_func)
        print("✅ Model training and saving completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during model training: {e}")
        raise e

if __name__ == "__main__":
    main()
