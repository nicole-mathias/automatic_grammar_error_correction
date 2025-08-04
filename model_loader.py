#!/usr/bin/env python3
"""
Model loader that handles compressed model files
Automatically decompresses .gz files when loading models
"""

import os
import gzip
import shutil
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, T5Tokenizer, T5ForConditionalGeneration

def decompress_if_needed(file_path):
    """Decompress a .gz file if it exists"""
    compressed_path = file_path + '.gz'
    if os.path.exists(compressed_path) and not os.path.exists(file_path):
        try:
            with gzip.open(compressed_path, 'rb') as f_in:
                with open(file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"✅ Decompressed {compressed_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to decompress {compressed_path}: {e}")
            return False
    return True

def load_bert_model(model_path, tokenizer_name="distilbert-base-multilingual-cased"):
    """Load BERT model with automatic decompression"""
    # Decompress if needed
    if not decompress_if_needed(model_path):
        return None, None
    
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        
        # Load model
        model = AutoModelForTokenClassification.from_pretrained(tokenizer_name)
        
        # Load trained weights
        if os.path.exists(model_path):
            state_dict = torch.load(model_path, map_location='cpu')
            model.load_state_dict(state_dict, strict=False)
            print(f"✅ Loaded BERT model from {model_path}")
        else:
            print(f"⚠️  Model file not found: {model_path}")
            return None, None
        
        return model, tokenizer
        
    except Exception as e:
        print(f"❌ Error loading BERT model: {e}")
        return None, None

def load_t5_model(model_dir):
    """Load T5 model with automatic decompression"""
    try:
        # Check for compressed files and decompress if needed
        pytorch_model_path = os.path.join(model_dir, "pytorch_model.bin")
        if not decompress_if_needed(pytorch_model_path):
            return None, None
        
        # Load tokenizer and model
        tokenizer = T5Tokenizer.from_pretrained(model_dir)
        model = T5ForConditionalGeneration.from_pretrained(model_dir)
        
        print(f"✅ Loaded T5 model from {model_dir}")
        return model, tokenizer
        
    except Exception as e:
        print(f"❌ Error loading T5 model: {e}")
        return None, None

def get_model_size_mb(file_path):
    """Get file size in MB"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    elif os.path.exists(file_path + '.gz'):
        return os.path.getsize(file_path + '.gz') / (1024 * 1024)
    return 0

def print_model_sizes():
    """Print sizes of all model files"""
    print("\n📊 Model File Sizes:")
    
    model_files = {
        'English': 'models/english/baseline_ft0_fce_3e.pt',
        'Czech': 'models/czech/ft1_cs_geccc_3e.pt',
        'German': 'models/german/ft2_de_falko-merlin_3e.pt',
        'Italian': 'models/italian/ft3_it_merlin_3e.pt',
        'Swedish': 'models/swedish/ft4_sv_swell_3e.pt',
        'T5': 't5_jfleg/saved_model/model/pytorch_model.bin'
    }
    
    total_size = 0
    for name, path in model_files.items():
        size = get_model_size_mb(path)
        total_size += size
        status = "✅" if size > 0 else "❌"
        print(f"  {status} {name}: {size:.1f} MB")
    
    print(f"  📦 Total: {total_size:.1f} MB")
    return total_size

if __name__ == "__main__":
    print_model_sizes() 