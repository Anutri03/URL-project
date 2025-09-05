# URL Phishing Detection API

A machine learning API that detects phishing URLs using lexical features and LightGBM. The API analyzes URL characteristics to predict whether a URL is safe or potentially malicious.

## Features

- **Single URL Prediction**: Analyze individual URLs for phishing detection
- **Batch Prediction**: Process multiple URLs at once (up to 100)
- **Feature Extraction**: Get detailed lexical features for any URL
- **High Accuracy**: 89.3% accuracy with 96.2% ROC-AUC score
- **RESTful API**: Easy integration with any application

## Model Performance

- **Accuracy**: 89.3%
- **ROC-AUC Score**: 96.2%
- **Precision**: 91% (Safe), 88% (Phishing)
- **Recall**: 88% (Safe), 91% (Phishing)

## API Endpoints

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

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd url-phishing-detector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train and save the model**
   ```bash
   python save_model.py
   ```
   This will create the model files needed for the API.

4. **Run the API locally**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Testing the API

```bash
# Health check
curl http://localhost:5000/

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Batch prediction
curl -X POST http://localhost:5000/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.google.com", "https://suspicious-site.com"]}'
```

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Deploy**
   - Render will automatically deploy your service
   - The API will be available at your assigned Render URL

### Method 2: Manual Setup

1. **Create a new Web Service on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.0

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Important Notes for Render Deployment

1. **Model Files**: Make sure to include your trained model files (`model.txt` or `model.joblib`) in your repository
2. **File Size**: If your model files are large (>100MB), consider using a cloud storage service
3. **Environment Variables**: The API automatically uses the PORT environment variable provided by Render

## Model Details

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

## API Response Format

### Success Response
```json
{
    "url": "https://example.com",
    "prediction": "safe|phishing",
    "probability": 0.23,
    "confidence": 0.54,
    "status": "success"
}
```

### Error Response
```json
{
    "error": "Error message",
    "status": "error"
}
```

## Rate Limits

- **Single Prediction**: No limit
- **Batch Prediction**: Maximum 100 URLs per request
- **Feature Extraction**: No limit

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the API documentation above
2. Review the error messages in responses
3. Open an issue on GitHub

## Changelog

### v1.0.0
- Initial release
- Single and batch URL prediction
- Feature extraction endpoint
- Render deployment support
