"""
Deployment script for Hugging Face Spaces
This script will train the model during deployment
"""

import os
import sys
import subprocess

def main():
    """Main deployment function"""
    print("🚀 Starting deployment process...")
    
    try:
        # Check if dataset exists
        if not os.path.exists("url_dataset_balanced.csv"):
            print("❌ Dataset file 'url_dataset_balanced.csv' not found!")
            print("Please ensure the dataset file is present in the repository.")
            sys.exit(1)
        
        # Train and save the model
        print("📊 Training model...")
        subprocess.run([sys.executable, "save_model.py"], check=True)
        
        print("✅ Deployment process completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during model training: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during deployment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
