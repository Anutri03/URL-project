# 🚀 Deployment Guide for URL Phishing Detection API

## Quick Deployment Options

### Option 1: Render.com (Recommended - FREE)

**Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in SSL certificates
- ✅ Easy scaling
- ✅ Perfect for Flask apps

**Steps:**

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` file
   - Click "Apply" to deploy

3. **Your API will be available at:**
   ```
   https://your-app-name.onrender.com
   ```

### Option 2: Railway.app (Alternative - FREE)

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Railway will auto-detect Python and deploy
4. Your API: `https://your-app-name.railway.app`

### Option 3: Heroku (Paid but reliable)

1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`

## 🔧 Integration with dhaal.io

### JavaScript Integration Example

```javascript
// Add this to your dhaal.io website
class PhishingDetector {
    constructor(apiUrl) {
        this.apiUrl = apiUrl; // Your deployed API URL
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

    async checkMultipleUrls(urls) {
        try {
            const response = await fetch(`${this.apiUrl}/predict_batch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ urls: urls })
            });
            
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Error checking URLs:', error);
            return { error: 'Failed to check URLs' };
        }
    }
}

// Usage example
const detector = new PhishingDetector('https://your-app-name.onrender.com');

// Check single URL
detector.checkUrl('https://example.com').then(result => {
    console.log('URL Check Result:', result);
    if (result.prediction === 'phishing') {
        alert('⚠️ This URL appears to be suspicious!');
    }
});

// Check multiple URLs
detector.checkMultipleUrls([
    'https://google.com',
    'https://suspicious-site.com'
]).then(results => {
    console.log('Batch Results:', results);
});
```

### React Component Example

```jsx
import React, { useState } from 'react';

const PhishingChecker = ({ apiUrl }) => {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const checkUrl = async () => {
        if (!url) return;
        
        setLoading(true);
        try {
            const response = await fetch(`${apiUrl}/predict`, {
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
            <h3>🔍 URL Safety Checker</h3>
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
            
            {result && (
                <div className={`result ${result.prediction}`}>
                    {result.prediction === 'phishing' ? '🚨' : '✅'}
                    <strong>{result.prediction === 'phishing' ? 'Suspicious' : 'Safe'}</strong>
                    <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                </div>
            )}
        </div>
    );
};

export default PhishingChecker;
```

### PHP Integration Example

```php
<?php
class PhishingDetector {
    private $apiUrl;
    
    public function __construct($apiUrl) {
        $this->apiUrl = $apiUrl;
    }
    
    public function checkUrl($url) {
        $data = json_encode(['url' => $url]);
        
        $options = [
            'http' => [
                'header' => "Content-Type: application/json\r\n",
                'method' => 'POST',
                'content' => $data
            ]
        ];
        
        $context = stream_context_create($options);
        $result = file_get_contents($this->apiUrl . '/predict', false, $context);
        
        return json_decode($result, true);
    }
}

// Usage
$detector = new PhishingDetector('https://your-app-name.onrender.com');
$result = $detector->checkUrl('https://example.com');

if ($result['prediction'] === 'phishing') {
    echo "⚠️ Warning: This URL appears suspicious!";
} else {
    echo "✅ This URL appears safe.";
}
?>
```

## 🎯 API Endpoints for dhaal.io

### 1. Single URL Check
```javascript
POST https://your-api-url.onrender.com/predict
Content-Type: application/json

{
    "url": "https://example.com"
}

// Response
{
    "url": "https://example.com",
    "prediction": "safe",
    "probability": 0.23,
    "confidence": 0.77,
    "status": "success"
}
```

### 2. Batch URL Check
```javascript
POST https://your-api-url.onrender.com/predict_batch
Content-Type: application/json

{
    "urls": [
        "https://google.com",
        "https://suspicious-site.com"
    ]
}
```

### 3. Health Check
```javascript
GET https://your-api-url.onrender.com/

// Response
{
    "status": "healthy",
    "message": "URL Phishing Detection API is running",
    "model_loaded": true
}
```

## 🔒 Security Considerations

1. **Rate Limiting**: Consider implementing rate limiting on your website
2. **Input Validation**: Always validate URLs before sending to API
3. **HTTPS**: Use HTTPS for all API calls
4. **Error Handling**: Implement proper error handling for API failures

## 📊 Monitoring Your API

### Health Check Script
```javascript
// Add this to monitor your API health
async function checkApiHealth() {
    try {
        const response = await fetch('https://your-api-url.onrender.com/');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('✅ API is healthy');
        } else {
            console.log('❌ API is not healthy');
        }
    } catch (error) {
        console.log('❌ API is unreachable');
    }
}

// Check every 5 minutes
setInterval(checkApiHealth, 5 * 60 * 1000);
```

## 🚀 Next Steps

1. **Deploy your API** using one of the options above
2. **Test the endpoints** to ensure they work
3. **Integrate with dhaal.io** using the provided examples
4. **Monitor performance** and adjust as needed

## 📞 Support

If you encounter any issues:
1. Check the API health endpoint
2. Review the error messages in responses
3. Check the deployment logs on your chosen platform
4. Ensure all dependencies are properly installed

Your API will be ready to protect your users from phishing URLs! 🛡️
