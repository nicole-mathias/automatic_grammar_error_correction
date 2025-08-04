#!/usr/bin/env python3
"""
Lightweight Grammar Error Detection & Correction Service
Uses base models initially to avoid 4GB deployment limit
"""

import os
import logging
import torch
from flask import Flask, request, jsonify, render_template
from transformers import (
    AutoTokenizer, AutoModelForTokenClassification,
    T5Tokenizer, T5ForConditionalGeneration,
    DistilBertForTokenClassification
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model variables
t5_tokenizer = None
t5_model = None
bert_tokenizer = None
bert_model = None

def load_base_models():
    """Load base models (smaller, no trained weights)"""
    global t5_tokenizer, t5_model, bert_tokenizer, bert_model
    
    try:
        logger.info("Loading base T5 model...")
        t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
        t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')
        logger.info("✅ Base T5 model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load T5 model: {e}")
        t5_model = None
    
    try:
        logger.info("Loading base DistilBERT model...")
        bert_tokenizer = AutoTokenizer.from_pretrained('distilbert-base-multilingual-cased')
        bert_model = DistilBertForTokenClassification.from_pretrained('distilbert-base-multilingual-cased')
        logger.info("✅ Base DistilBERT model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load BERT model: {e}")
        bert_model = None

def detect_errors(text, language='english'):
    """Detect grammar errors in text using base model"""
    if not bert_model or not bert_tokenizer:
        return {
            "error": "Model not loaded",
            "tags": [],
            "note": "Base model loaded - limited error detection capability"
        }
    
    try:
        # Tokenize input
        inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Get predictions
        with torch.no_grad():
            outputs = bert_model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=2)
        
        # Convert predictions to tags
        tags = []
        tokens = bert_tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        
        for i, (token, pred) in enumerate(zip(tokens, predictions[0])):
            if token.startswith('##'):
                continue
            tag = 'i' if pred.item() == 1 else 'c'
            tags.append({
                "token": token.replace('##', ''),
                "tag": tag,
                "confidence": 0.5  # Base model has limited confidence
            })
        
        return {
            "tags": tags,
            "note": "Using base DistilBERT model - limited error detection capability"
        }
    
    except Exception as e:
        logger.error(f"Error in error detection: {e}")
        return {"error": str(e)}

def correct_grammar(text, language='english'):
    """Correct grammar using base T5 model"""
    if not t5_model or not t5_tokenizer:
        return {
            "error": "Model not loaded",
            "corrected_text": text,
            "note": "Base model loaded - limited correction capability"
        }
    
    try:
        # Prepare input
        input_text = f"grammar: {text}"
        inputs = t5_tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate correction
        with torch.no_grad():
            outputs = t5_model.generate(
                inputs['input_ids'],
                max_length=512,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
        
        corrected_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "corrected_text": corrected_text,
            "note": "Using base T5 model - limited correction capability"
        }
    
    except Exception as e:
        logger.error(f"Error in grammar correction: {e}")
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('multilingual.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": {
            "t5": t5_model is not None,
            "bert": bert_model is not None
        }
    })

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    
    result = detect_errors(text, language)
    return jsonify(result)

@app.route('/api/correct', methods=['POST'])
def correct():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    
    if language != 'english':
        return jsonify({"error": "Grammar correction only available for English"})
    
    result = correct_grammar(text, language)
    return jsonify(result)

@app.route('/api/languages', methods=['GET'])
def languages():
    return jsonify({
        "languages": {
            "english": {
                "name": "English",
                "description": "Grammar Detection and Correction",
                "accuracy": None,
                "supports_correction": True
            },
            "czech": {
                "name": "Czech",
                "description": "Grammar Detection",
                "accuracy": None,
                "supports_correction": False
            },
            "german": {
                "name": "German", 
                "description": "Grammar Detection",
                "accuracy": None,
                "supports_correction": False
            },
            "italian": {
                "name": "Italian",
                "description": "Grammar Detection", 
                "accuracy": None,
                "supports_correction": False
            },
            "swedish": {
                "name": "Swedish",
                "description": "Grammar Detection",
                "accuracy": None,
                "supports_correction": False
            }
        }
    })

if __name__ == '__main__':
    logger.info("Starting Lightweight Grammar Error Detection & Correction Service")
    load_base_models()
    logger.info("🎉 Service ready! Starting Flask server on http://0.0.0.0:5002")
    app.run(host='0.0.0.0', port=5002, debug=False) 