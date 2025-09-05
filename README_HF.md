---
title: URL Phishing Detection API
emoji: 🛡️
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# URL Phishing Detection API

A machine learning API that detects phishing URLs using lexical features and LightGBM. This API analyzes URL characteristics to predict whether a URL is safe or potentially malicious.

## 🚀 Features

- **Single URL Prediction**: Analyze individual URLs for phishing detection
- **Batch Prediction**: Process multiple URLs at once (up to 100)
- **Feature Extraction**: Get detailed lexical features for any URL
- **High Accuracy**: 89.3% accuracy with 96.2% ROC-AUC score
- **RESTful API**: Easy integration with any application

## 📊 Model Performance

- **Accuracy**: 89.3%
- **ROC-AUC Score**: 96.2%
- **Precision**: 91% (Safe), 88% (Phishing)
- **Recall**: 88% (Safe), 91% (Phishing)

## 🔧 API Endpoints

### Health Check
```
GET /
```
Returns API status and model loading information.

### Single URL Prediction
```
POST /predict
Content-Type: application/json

{
    "url": "https://example.com"
}
```

**Response:**
```json
{
    "url": "https://example.com",
    "prediction": "safe",
    "probability": 0.23,
    "confidence": 0.54,
    "status": "success"
}
```

### Batch URL Prediction
```
POST /predict_batch
Content-Type: application/json

{
    "urls": [
        "https://example.com",
        "https://suspicious-site.com"
    ]
}
```

### Feature Extraction
```
POST /features
Content-Type: application/json

{
    "url": "https://example.com"
}
```

## 🧠 Model Details

### Features Used
The model analyzes 15 lexical features from URLs:

- `url_length`: Total length of the URL
- `path_length`: Length of the path component
- `query_length`: Length of the query string
- `num_digits`: Count of digits in the URL
- `num_letters`: Count of letters in the URL
- `num_special`: Count of special characters
- `count_dot`: Count of dots (capped at 4)
- `count_dash`: Count of dashes
- `count_slash`: Count of forward slashes
- `count_at`: Count of @ symbols
- `count_qmark`: Count of question marks
- `count_percent`: Count of percent signs
- `count_equal`: Count of equal signs
- `has_https`: Whether URL uses HTTPS
- `has_ip`: Whether URL contains an IP address

### Training Data
- **Dataset**: 7,087,812 URLs (balanced)
- **Split**: 80% training, 20% testing
- **Algorithm**: LightGBM (Gradient Boosting)
- **Early Stopping**: 50 rounds

## 📝 Usage Examples

### Python
```python
import requests

# Single prediction
response = requests.post("https://your-space-url.hf.space/predict", 
                        json={"url": "https://www.google.com"})
result = response.json()
print(result)

# Batch prediction
response = requests.post("https://your-space-url.hf.space/predict_batch", 
                        json={"urls": ["https://www.google.com", "https://suspicious-site.com"]})
results = response.json()
print(results)
```

### cURL
```bash
# Health check
curl https://your-space-url.hf.space/

# Single prediction
curl -X POST https://your-space-url.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Batch prediction
curl -X POST https://your-space-url.hf.space/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.google.com", "https://suspicious-site.com"]}'
```

## 🔒 Rate Limits

- **Single Prediction**: No limit
- **Batch Prediction**: Maximum 100 URLs per request
- **Feature Extraction**: No limit

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the API documentation above
2. Review the error messages in responses
3. Open an issue on GitHub
