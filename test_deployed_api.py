import requests
import json

def test_deployed_api(base_url):
    """Test the deployed API on Render"""
    print(f"Testing deployed API at: {base_url}")
    print("=" * 50)
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    print()
    
    # Test single prediction
    print("2. Testing single URL prediction...")
    try:
        test_url = "https://www.google.com"
        payload = {"url": test_url}
        response = requests.post(f"{base_url}/predict", json=payload, timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   URL: {result['url']}")
            print(f"   Prediction: {result['prediction']}")
            print(f"   Probability: {result['probability']:.4f}")
            print(f"   Confidence: {result['confidence']:.4f}")
            print("   ✅ Single prediction passed")
        else:
            print(f"   Response: {response.text}")
            print("   ❌ Single prediction failed")
    except Exception as e:
        print(f"   ❌ Single prediction error: {e}")
    print()
    
    # Test batch prediction
    print("3. Testing batch prediction...")
    try:
        test_urls = ["https://www.google.com", "https://www.github.com"]
        payload = {"urls": test_urls}
        response = requests.post(f"{base_url}/predict_batch", json=payload, timeout=20)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Total processed: {result['total_processed']}")
            for i, res in enumerate(result['results']):
                print(f"   URL {i+1}: {res['url']} -> {res['prediction']} ({res['probability']:.4f})")
            print("   ✅ Batch prediction passed")
        else:
            print(f"   Response: {response.text}")
            print("   ❌ Batch prediction failed")
    except Exception as e:
        print(f"   ❌ Batch prediction error: {e}")
    print()
    
    # Test feature extraction
    print("4. Testing feature extraction...")
    try:
        test_url = "https://www.example.com"
        payload = {"url": test_url}
        response = requests.post(f"{base_url}/features", json=payload, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   URL: {result['url']}")
            print(f"   Features extracted: {len(result['features'])}")
            print("   ✅ Feature extraction passed")
        else:
            print(f"   Response: {response.text}")
            print("   ❌ Feature extraction failed")
    except Exception as e:
        print(f"   ❌ Feature extraction error: {e}")
    print()
    
    print("=" * 50)
    print("API testing completed!")

if __name__ == "__main__":
    # Replace with your actual Render URL
    render_url = input("Enter your Render API URL (e.g., https://url-phishing-detector-xyz.onrender.com): ").strip()
    
    if not render_url:
        print("No URL provided. Exiting.")
        exit(1)
    
    if not render_url.startswith('http'):
        render_url = 'https://' + render_url
    
    test_deployed_api(render_url)
