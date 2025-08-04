#!/usr/bin/env python3
"""
Test compression on existing models
"""

import os
import gzip
import shutil
from model_loader import get_model_size_mb

def compress_model_file(file_path):
    """Compress a model file to save space"""
    if not os.path.exists(file_path):
        return False
    
    compressed_path = file_path + '.gz'
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Get sizes
        original_size = os.path.getsize(file_path) / (1024 * 1024)
        compressed_size = os.path.getsize(compressed_path) / (1024 * 1024)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"✅ Compressed {file_path}")
        print(f"   Original: {original_size:.1f} MB")
        print(f"   Compressed: {compressed_size:.1f} MB")
        print(f"   Compression: {compression_ratio:.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Failed to compress {file_path}: {e}")
        return False

def main():
    """Test compression on all model files"""
    print("🧪 Testing model compression...")
    
    model_files = {
        'English': 'models/english/baseline_ft0_fce_3e.pt',
        'Czech': 'models/czech/ft1_cs_geccc_3e.pt',
        'German': 'models/german/ft2_de_falko-merlin_3e.pt',
        'Italian': 'models/italian/ft3_it_merlin_3e.pt',
        'Swedish': 'models/swedish/ft4_sv_swell_3e.pt',
        'T5': 't5_jfleg/saved_model/model/pytorch_model.bin'
    }
    
    total_original = 0
    total_compressed = 0
    
    for name, path in model_files.items():
        if os.path.exists(path):
            print(f"\n📦 Compressing {name} model...")
            if compress_model_file(path):
                original_size = os.path.getsize(path) / (1024 * 1024)
                compressed_size = os.path.getsize(path + '.gz') / (1024 * 1024)
                total_original += original_size
                total_compressed += compressed_size
        else:
            print(f"⚠️  {name} model not found: {path}")
    
    print(f"\n📊 Summary:")
    print(f"   Total Original: {total_original:.1f} MB")
    print(f"   Total Compressed: {total_compressed:.1f} MB")
    print(f"   Total Savings: {total_original - total_compressed:.1f} MB")
    print(f"   Overall Compression: {((1 - total_compressed / total_original) * 100):.1f}%")

if __name__ == "__main__":
    main() 