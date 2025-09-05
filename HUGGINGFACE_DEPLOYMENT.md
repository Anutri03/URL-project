# 🤗 Hugging Face Spaces Deployment Guide

## Why Hugging Face Spaces?

✅ **FREE** - No cost for public spaces  
✅ **Fast** - Optimized for ML applications  
✅ **Easy** - Simple deployment process  
✅ **Reliable** - Great uptime and performance  
✅ **Community** - Share with the ML community  
✅ **Automatic** - Auto-deploys from GitHub  

## 🚀 Quick Deployment Steps

### Step 1: Prepare Your Repository

Your project is already configured for Hugging Face! You have:
- ✅ `README_HF.md` with proper metadata
- ✅ `Dockerfile` configured for port 7860
- ✅ `deploy.py` for model training
- ✅ All necessary files

### Step 2: Create Hugging Face Space

1. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
2. **Click "Create new Space"**
3. **Fill in the details:**
   - **Space name**: `url-phishing-detector` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU Basic (FREE)
   - **Visibility**: Public

4. **Connect your GitHub repository:**
   - Click "Import from GitHub"
   - Select your repository
   - Or upload files manually

### Step 3: Configure Space Settings

In your Space settings, ensure:
- **SDK**: Docker
- **Hardware**: CPU Basic
- **App Port**: 7860 (already configured)

### Step 4: Deploy

Your Space will automatically build and deploy! The process includes:
1. Building Docker image
2. Training the model (`python save_model.py`)
3. Starting the Flask API
4. Making it available at `https://your-username-url-phishing-detector.hf.space`

## 🔧 Integration with dhaal.io

### Your API URL will be:
```
https://your-username-url-phishing-detector.hf.space
```

### JavaScript Integration:
```javascript
class PhishingDetector {
    constructor() {
        this.apiUrl = 'https://your-username-url-phishing-detector.hf.space';
    }

    async checkUrl(url) {
        try {
            const response = await fetch(`${this.apiUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Error checking URL:', error);
            return { error: 'Failed to check URL' };
        }
    }
}

// Usage
const detector = new PhishingDetector();
detector.checkUrl('https://example.com').then(result => {
    if (result.prediction === 'phishing') {
        alert('⚠️ This URL appears suspicious!');
    } else {
        console.log('✅ URL appears safe');
    }
});
```

### React Component for dhaal.io:
```jsx
import React, { useState } from 'react';

const PhishingChecker = () => {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const API_URL = 'https://your-username-url-phishing-detector.hf.space';

    const checkUrl = async () => {
        if (!url) return;
        
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });
            
            const data = await response.json();
            setResult(data);
        } catch (error) {
            setResult({ error: 'Failed to check URL' });
        }
        setLoading(false);
    };

    return (
        <div className="phishing-checker">
            <h3>🛡️ URL Safety Checker</h3>
            <div className="input-group">
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter URL to check..."
                    className="url-input"
                />
                <button onClick={checkUrl} disabled={loading}>
                    {loading ? 'Checking...' : 'Check URL'}
                </button>
            </div>
            
            {result && !result.error && (
                <div className={`result ${result.prediction}`}>
                    <div className="status">
                        {result.prediction === 'phishing' ? '🚨' : '✅'}
                        <strong>
                            {result.prediction === 'phishing' ? 'Suspicious URL' : 'Safe URL'}
                        </strong>
                    </div>
                    <div className="confidence">
                        Confidence: {(result.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="probability">
                        Probability: {(result.probability * 100).toFixed(1)}%
                    </div>
                </div>
            )}
            
            {result && result.error && (
                <div className="error">
                    ❌ {result.error}
                </div>
            )}
        </div>
    );
};

export default PhishingChecker;
```

## 📊 API Endpoints

### 1. Health Check
```bash
GET https://your-username-url-phishing-detector.hf.space/
```

### 2. Single URL Prediction
```bash
POST https://your-username-url-phishing-detector.hf.space/predict
Content-Type: application/json

{
    "url": "https://example.com"
}
```

### 3. Batch Prediction
```bash
POST https://your-username-url-phishing-detector.hf.space/predict_batch
Content-Type: application/json

{
    "urls": [
        "https://google.com",
        "https://suspicious-site.com"
    ]
}
```

### 4. Feature Extraction
```bash
POST https://your-username-url-phishing-detector.hf.space/features
Content-Type: application/json

{
    "url": "https://example.com"
}
```

## 🎯 Example Responses

### Successful Prediction:
```json
{
    "url": "https://example.com",
    "prediction": "safe",
    "probability": 0.23,
    "confidence": 0.77,
    "status": "success"
}
```

### Phishing Detection:
```json
{
    "url": "https://suspicious-site.com",
    "prediction": "phishing",
    "probability": 0.87,
    "confidence": 0.87,
    "status": "success"
}
```

## 🔒 Security Features

- **Input Validation**: All URLs are validated before processing
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Graceful error responses
- **HTTPS**: All communications encrypted

## 📈 Performance

- **Model Accuracy**: 89.3%
- **ROC-AUC Score**: 96.2%
- **Response Time**: < 100ms for single URL
- **Batch Processing**: Up to 100 URLs per request

## 🛠️ Troubleshooting

### Common Issues:

1. **Space not building**: Check Dockerfile syntax
2. **Model not loading**: Ensure `url_dataset_balanced.csv` is present
3. **API not responding**: Check port configuration (7860)
4. **CORS errors**: Add CORS headers if needed

### Debug Commands:
```bash
# Check if your Space is running
curl https://your-username-url-phishing-detector.hf.space/

# Test prediction
curl -X POST https://your-username-url-phishing-detector.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

## 🚀 Advanced Features

### Custom Domain (Optional):
- Upgrade to Pro for custom domains
- Better for production use

### Monitoring:
- Built-in logs in Hugging Face Spaces
- Performance metrics available
- Error tracking included

## 📞 Support

1. **Hugging Face Documentation**: [hf.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
2. **Community Forum**: [discuss.huggingface.co](https://discuss.huggingface.co)
3. **GitHub Issues**: For code-related problems

## 🎉 You're Ready!

Your URL phishing detection API will be:
- ✅ **FREE** to host
- ✅ **Fast** and reliable
- ✅ **Easy** to integrate with dhaal.io
- ✅ **Scalable** for your needs
- ✅ **Community** accessible

Deploy now and start protecting your users! 🛡️
