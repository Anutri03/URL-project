# 🚀 Step-by-Step Deployment Guide

## Prerequisites Checklist ✅

Before deploying, ensure you have:
- [ ] GitHub account
- [ ] Hugging Face account (free)
- [ ] All project files in a GitHub repository
- [ ] `url_dataset_balanced.csv` file in your repository

## Step 1: Prepare Your GitHub Repository

### 1.1 Push Your Code to GitHub
```bash
# Navigate to your project directory
cd "E:\URL project"

# Initialize git if not already done
git init

# Add all files
git add .

# Commit your changes
git commit -m "Ready for Hugging Face deployment"

# Add your GitHub repository (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/url-phishing-detector.git

# Push to GitHub
git push -u origin main
```

### 1.2 Verify Required Files
Make sure these files are in your repository:
- ✅ `app.py`
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `save_model.py`
- ✅ `deploy.py`
- ✅ `url_dataset_balanced.csv`
- ✅ `README_HF.md`

## Step 2: Create Hugging Face Account

### 2.1 Sign Up/Login
1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" or "Login"
3. Complete the registration process
4. Verify your email if required

## Step 3: Create Hugging Face Space

### 3.1 Navigate to Spaces
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"** button

### 3.2 Configure Your Space
Fill in the following details:

**Space Configuration:**
- **Space name**: `url-phishing-detector` (or your preferred name)
- **License**: `MIT`
- **SDK**: `Docker` ⚠️ **IMPORTANT: Select Docker**
- **Hardware**: `CPU Basic` (FREE)
- **Visibility**: `Public`

### 3.3 Create the Space
1. Click **"Create Space"**
2. Wait for the space to be created
3. You'll be redirected to your new space

## Step 4: Connect Your Repository

### 4.1 Import from GitHub
1. In your new space, click **"Files and versions"** tab
2. Click **"Add file"** → **"Upload files"**
3. **OR** click **"Add file"** → **"Import from GitHub"**

### 4.2 If Importing from GitHub:
1. Select your repository: `YOUR_USERNAME/url-phishing-detector`
2. Click **"Import"**
3. Wait for files to be imported

### 4.3 If Uploading Manually:
Upload these files one by one:
- `app.py`
- `Dockerfile`
- `requirements.txt`
- `save_model.py`
- `deploy.py`
- `url_dataset_balanced.csv`
- `README_HF.md`

## Step 5: Configure Space Settings

### 5.1 Check Space Settings
1. Go to **"Settings"** tab in your space
2. Verify:
   - **SDK**: Docker
   - **Hardware**: CPU Basic
   - **App Port**: 7860 (should be auto-detected)

### 5.2 Update README (Optional)
Your `README_HF.md` should automatically become the space README. If not:
1. Go to **"Files and versions"**
2. Rename `README_HF.md` to `README.md`
3. Commit the change

## Step 6: Deploy Your API

### 6.1 Automatic Deployment
Once you upload/import your files, Hugging Face will automatically:
1. Build the Docker image
2. Install dependencies
3. Train the model (`python save_model.py`)
4. Start your Flask API

### 6.2 Monitor the Build Process
1. Go to **"Logs"** tab to watch the build process
2. Look for these key messages:
   ```
   ✅ Model trained and saved successfully
   ✅ Model loaded successfully from phishing_model.pkl
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:7860
   ```

### 6.3 Build Time
- **Expected time**: 5-15 minutes
- **Dependencies**: 2-3 minutes
- **Model training**: 3-10 minutes
- **API startup**: 1-2 minutes

## Step 7: Test Your Deployed API

### 7.1 Get Your API URL
Your API will be available at:
```
https://YOUR_USERNAME-url-phishing-detector.hf.space
```

### 7.2 Test Health Check
```bash
curl https://YOUR_USERNAME-url-phishing-detector.hf.space/
```

**Expected Response:**
```json
{
    "status": "healthy",
    "message": "URL Phishing Detection API is running",
    "model_loaded": true,
    "endpoints": {
        "predict": "POST /predict - Single URL prediction",
        "predict_batch": "POST /predict_batch - Batch URL prediction",
        "features": "POST /features - Extract URL features"
    }
}
```

### 7.3 Test URL Prediction
```bash
curl -X POST https://YOUR_USERNAME-url-phishing-detector.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Expected Response:**
```json
{
    "url": "https://www.google.com",
    "prediction": "safe",
    "probability": 0.23,
    "confidence": 0.77,
    "status": "success"
}
```

## Step 8: Integrate with dhaal.io

### 8.1 Update Your API URL
Replace `YOUR_USERNAME` with your actual Hugging Face username:

```javascript
// Update this URL in your dhaal.io website
const API_URL = 'https://YOUR_USERNAME-url-phishing-detector.hf.space';

// Example usage
async function checkUrl(url) {
    try {
        const response = await fetch(`${API_URL}/predict`, {
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
```

### 8.2 Test Integration
```javascript
// Test with your dhaal.io website
checkUrl('https://example.com').then(result => {
    console.log('URL Check Result:', result);
    if (result.prediction === 'phishing') {
        alert('⚠️ This URL appears to be suspicious!');
    } else {
        console.log('✅ URL appears safe');
    }
});
```

## Step 9: Monitor and Maintain

### 9.1 Check Logs Regularly
1. Go to **"Logs"** tab in your space
2. Monitor for any errors or issues
3. Check API performance

### 9.2 Update Your Model (Optional)
If you want to retrain the model:
1. Update your dataset
2. Push changes to GitHub
3. Hugging Face will automatically rebuild

## 🎉 Success! Your API is Live!

### Your API Endpoints:
- **Health Check**: `GET /`
- **Single Prediction**: `POST /predict`
- **Batch Prediction**: `POST /predict_batch`
- **Feature Extraction**: `POST /features`

### Example API Calls:
```bash
# Health check
curl https://YOUR_USERNAME-url-phishing-detector.hf.space/

# Single URL check
curl -X POST https://YOUR_USERNAME-url-phishing-detector.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Batch URL check
curl -X POST https://YOUR_USERNAME-url-phishing-detector.hf.space/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.google.com", "https://suspicious-site.com"]}'
```

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails**: Check logs for missing dependencies
2. **Model Not Loading**: Ensure `url_dataset_balanced.csv` is present
3. **API Not Responding**: Check if port 7860 is configured
4. **CORS Errors**: Add CORS headers if needed

### Debug Commands:
```bash
# Check if API is running
curl https://YOUR_USERNAME-url-phishing-detector.hf.space/

# Test with a simple URL
curl -X POST https://YOUR_USERNAME-url-phishing-detector.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

## 📞 Support

If you encounter issues:
1. Check the **"Logs"** tab in your Hugging Face space
2. Review error messages in API responses
3. Ensure all required files are uploaded
4. Verify your GitHub repository is public

**Your URL phishing detection API is now ready to protect your dhaal.io users!** 🛡️
