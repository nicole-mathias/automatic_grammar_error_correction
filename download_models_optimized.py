#!/usr/bin/env python3
"""
Optimized script to download trained models with size management
Handles large models by downloading only essential files and using compression
"""

import os
import requests
import zipfile
import gzip
import shutil
from pathlib import Path
import time

def get_model_url(file_id):
    """Generate Google Drive download URL from file ID"""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def download_file_with_retry(url, filename, dest_path, max_retries=3):
    """Download a file with retry logic and progress tracking"""
    print(f"Downloading {filename}...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end='', flush=True)
            
            print(f"\n✅ Downloaded {filename} ({downloaded / (1024*1024):.1f} MB)")
            return True
            
        except Exception as e:
            print(f"\n❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"❌ Failed to download {filename} after {max_retries} attempts")
                return False
    
    return False

def compress_model_file(file_path):
    """Compress a model file to save space"""
    if not os.path.exists(file_path):
        return False
    
    compressed_path = file_path + '.gz'
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove original file
        os.remove(file_path)
        print(f"✅ Compressed {file_path} -> {compressed_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to compress {file_path}: {e}")
        return False

def decompress_model_file(compressed_path):
    """Decompress a model file"""
    original_path = compressed_path.replace('.gz', '')
    try:
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(original_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove compressed file
        os.remove(compressed_path)
        print(f"✅ Decompressed {compressed_path} -> {original_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to decompress {compressed_path}: {e}")
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

def check_disk_space():
    """Check available disk space"""
    try:
        stat = os.statvfs('.')
        free_space = stat.f_frsize * stat.f_bavail
        free_gb = free_space / (1024**3)
        print(f"Available disk space: {free_gb:.1f} GB")
        return free_gb
    except:
        print("Could not check disk space")
        return 10.0  # Assume 10GB if we can't check

def main():
    """Main function to download all models with optimization"""
    print("🚀 Starting optimized model download for Railway deployment...")
    
    # Check disk space
    free_space = check_disk_space()
    if free_space < 2.0:
        print("⚠️  Warning: Less than 2GB available space")
    
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
    
    # Download BERT models with compression
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
        if os.path.exists(dest_path) or os.path.exists(dest_path + '.gz'):
            print(f"⏭️  {filename} already exists, skipping...")
            continue
            
        url = get_model_url(model_ids[language])
        success = download_file_with_retry(url, filename, dest_path)
        if success:
            # Compress the model file to save space
            compress_model_file(dest_path)
        else:
            print(f"⚠️  Warning: Failed to download {language} model")
    
    # Download and extract T5 model
    t5_dest = "t5_model.zip"
    if not os.path.exists("t5_jfleg/saved_model/model/pytorch_model.bin"):
        url = get_model_url(model_ids['t5'])
        success = download_file_with_retry(url, "t5_model.zip", t5_dest)
        if success:
            extract_t5_model(t5_dest)
            # Clean up zip file
            if os.path.exists(t5_dest):
                os.remove(t5_dest)
        else:
            print("⚠️  Warning: Failed to download T5 model")
    else:
        print("⏭️  T5 model already exists, skipping...")
    
    print("✅ Optimized model download process completed!")

if __name__ == "__main__":
    main() 