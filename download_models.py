#!/usr/bin/env python3
"""
Script to download trained models from Google Drive for Railway deployment
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

# Google Drive file IDs (you'll need to replace these with your actual file IDs)
MODEL_FILES = {
    'english': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_ENGLISH_MODEL_ID',
        'filename': 'baseline_ft0_fce_3e.pt'
    },
    'czech': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_CZECH_MODEL_ID',
        'filename': 'ft1_cs_geccc_3e.pt'
    },
    'german': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_GERMAN_MODEL_ID',
        'filename': 'ft2_de_falko-merlin_3e.pt'
    },
    'italian': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_ITALIAN_MODEL_ID',
        'filename': 'ft3_it_merlin_3e.pt'
    },
    'swedish': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_SWEDISH_MODEL_ID',
        'filename': 'ft4_sv_swell_3e.pt'
    },
    't5': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_T5_MODEL_ID',
        'filename': 't5_model.zip'
    }
}

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
    """Main function to download all models"""
    print("🚀 Starting model download for Railway deployment...")
    
    # Create directories
    setup_model_directories()
    
    # Download BERT models
    for language, model_info in MODEL_FILES.items():
        if language == 't5':
            continue
            
        dest_path = f"models/{language}/{model_info['filename']}"
        
        # Skip if file already exists
        if os.path.exists(dest_path):
            print(f"⏭️  {model_info['filename']} already exists, skipping...")
            continue
            
        success = download_file(model_info['url'], model_info['filename'], dest_path)
        if not success:
            print(f"⚠️  Warning: Failed to download {language} model")
    
    # Download and extract T5 model
    t5_dest = "t5_model.zip"
    if not os.path.exists("t5_jfleg/saved_model/model/pytorch_model.bin"):
        success = download_file(MODEL_FILES['t5']['url'], MODEL_FILES['t5']['filename'], t5_dest)
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