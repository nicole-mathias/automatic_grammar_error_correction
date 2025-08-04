#!/usr/bin/env python3
"""
Alternative script to download trained models using environment variables
This allows you to set file IDs in Railway's environment variables
"""

import os
import requests
import zipfile
from pathlib import Path

def get_model_url(file_id):
    """Generate Google Drive download URL from file ID"""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def download_file(url, filename, dest_path):
    """Download a file from URL to destination path"""
    print(f"Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def setup_model_directories():
    """Create model directories"""
    directories = [
        'models/english',
        'models/czech', 
        'models/german',
        'models/italian',
        'models/swedish',
        't5_jfleg/saved_model/model'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def extract_t5_model(zip_path):
    """Extract T5 model from zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('t5_jfleg/saved_model/model/')
        print("✅ Extracted T5 model")
        return True
    except Exception as e:
        print(f"❌ Failed to extract T5 model: {e}")
        return False

def main():
    """Main function to download all models using environment variables"""
    print("🚀 Starting model download for Railway deployment...")
    
    # Get file IDs from environment variables
    model_ids = {
        'english': os.environ.get('ENGLISH_MODEL_ID'),
        'czech': os.environ.get('CZECH_MODEL_ID'),
        'german': os.environ.get('GERMAN_MODEL_ID'),
        'italian': os.environ.get('ITALIAN_MODEL_ID'),
        'swedish': os.environ.get('SWEDISH_MODEL_ID'),
        't5': os.environ.get('T5_MODEL_ID')
    }
    
    # Check if all IDs are provided
    missing_ids = [lang for lang, model_id in model_ids.items() if not model_id]
    if missing_ids:
        print(f"⚠️  Warning: Missing environment variables for: {', '.join(missing_ids)}")
        print("Models will not be downloaded. Set the environment variables in Railway dashboard.")
        return
    
    # Create directories
    setup_model_directories()
    
    # Download BERT models
    model_files = {
        'english': 'baseline_ft0_fce_3e.pt',
        'czech': 'ft1_cs_geccc_3e.pt',
        'german': 'ft2_de_falko-merlin_3e.pt',
        'italian': 'ft3_it_merlin_3e.pt',
        'swedish': 'ft4_sv_swell_3e.pt'
    }
    
    for language, filename in model_files.items():
        dest_path = f"models/{language}/{filename}"
        
        # Skip if file already exists
        if os.path.exists(dest_path):
            print(f"⏭️  {filename} already exists, skipping...")
            continue
            
        url = get_model_url(model_ids[language])
        success = download_file(url, filename, dest_path)
        if not success:
            print(f"⚠️  Warning: Failed to download {language} model")
    
    # Download and extract T5 model
    t5_dest = "t5_model.zip"
    if not os.path.exists("t5_jfleg/saved_model/model/pytorch_model.bin"):
        url = get_model_url(model_ids['t5'])
        success = download_file(url, "t5_model.zip", t5_dest)
        if success:
            extract_t5_model(t5_dest)
            # Clean up zip file
            if os.path.exists(t5_dest):
                os.remove(t5_dest)
        else:
            print("⚠️  Warning: Failed to download T5 model")
    else:
        print("⏭️  T5 model already exists, skipping...")
    
    print("✅ Model download process completed!")

if __name__ == "__main__":
    main() 