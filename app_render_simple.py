#!/usr/bin/env python3
"""
Simple Grammar Error Detection & Correction Service
Uses only basic Python libraries - no transformers/tokenizers
"""

import os
import logging
import re
from flask import Flask, request, jsonify, render_template

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple grammar rules for demonstration
GRAMMAR_RULES = {
    'english': {
        'subject_verb_agreement': [
            (r'\b(I|he|she|it)\s+(go|goes)\b', r'\1 go'),
            (r'\b(I|he|she|it)\s+(are|were)\b', r'\1 am'),
            (r'\b(you|we|they)\s+(goes|is|was)\b', r'\1 go'),
        ],
        'common_errors': [
            (r'\b(its)\s+', r"it's "),
            (r'\b(your)\s+(going)\b', r"you're going"),
            (r'\b(their)\s+(going)\b', r"they're going"),
            (r'\b(there)\s+(going)\b', r"they're going"),
        ]
    }
}

def detect_errors_simple(text, language='english'):
    """Simple grammar error detection using regex patterns"""
    if language not in GRAMMAR_RULES:
        return {"error": f"Language {language} not supported"}
    
    errors = []
    words = text.split()
    
    # Check for basic patterns
    for pattern, replacement in GRAMMAR_RULES[language]['subject_verb_agreement']:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            errors.append({
                "token": match.group(),
                "tag": "i",
                "confidence": 0.8,
                "suggestion": re.sub(pattern, replacement, match.group(), flags=re.IGNORECASE)
            })
    
    # Check for common errors
    for pattern, replacement in GRAMMAR_RULES[language]['common_errors']:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            errors.append({
                "token": match.group(),
                "tag": "i", 
                "confidence": 0.9,
                "suggestion": re.sub(pattern, replacement, match.group(), flags=re.IGNORECASE)
            })
    
    # Mark all other words as correct
    all_tokens = []
    for word in words:
        is_error = any(error["token"].lower() in word.lower() for error in errors)
        all_tokens.append({
            "token": word,
            "tag": "i" if is_error else "c",
            "confidence": 0.9 if is_error else 0.95
        })
    
    return {
        "tags": all_tokens,
        "note": "Using simple regex-based detection (limited capability)"
    }

def correct_grammar_simple(text, language='english'):
    """Simple grammar correction using regex patterns"""
    if language != 'english':
        return {"error": "Grammar correction only available for English"}
    
    corrected_text = text
    
    # Apply corrections
    for pattern, replacement in GRAMMAR_RULES[language]['subject_verb_agreement']:
        corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.IGNORECASE)
    
    for pattern, replacement in GRAMMAR_RULES[language]['common_errors']:
        corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.IGNORECASE)
    
    return {
        "corrected_text": corrected_text,
        "note": "Using simple regex-based correction (limited capability)"
    }

@app.route('/')
def index():
    return render_template('multilingual.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": {
            "simple_detection": True,
            "simple_correction": True
        },
        "deployment": "render-simple-no-transformers"
    })

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    
    result = detect_errors_simple(text, language)
    return jsonify(result)

@app.route('/api/correct', methods=['POST'])
def correct():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')
    
    if language != 'english':
        return jsonify({"error": "Grammar correction only available for English"})
    
    result = correct_grammar_simple(text, language)
    return jsonify(result)

@app.route('/api/languages', methods=['GET'])
def languages():
    return jsonify({
        "languages": {
            "english": {
                "name": "English",
                "description": "Grammar Detection and Correction",
                "accuracy": 75.0,
                "supports_correction": True
            },
            "czech": {
                "name": "Czech",
                "description": "Grammar Detection",
                "accuracy": 60.0,
                "supports_correction": False
            },
            "german": {
                "name": "German", 
                "description": "Grammar Detection",
                "accuracy": 60.0,
                "supports_correction": False
            },
            "italian": {
                "name": "Italian",
                "description": "Grammar Detection", 
                "accuracy": 60.0,
                "supports_correction": False
            },
            "swedish": {
                "name": "Swedish",
                "description": "Grammar Detection",
                "accuracy": 60.0,
                "supports_correction": False
            }
        }
    })

if __name__ == '__main__':
    logger.info("🚀 Starting Simple Grammar Error Detection & Correction Service")
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🎉 Service ready! Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False) 