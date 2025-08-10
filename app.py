from flask import Flask, request, jsonify, render_template
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, BertTokenizer, BertForTokenClassification
import numpy as np
import logging
import os
import time
import signal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for models
t5_model = None
t5_tokenizer = None
bert_model = None
bert_tokenizer = None

# Model configurations - using HF Hub models
MODEL_CONFIG = {
    't5_model_name': 't5-base',  # Base T5 model for grammar correction
    'bert_model_name': 'bert-base-multilingual-cased',  # Base BERT model for error detection
    'max_length': 512
}

def load_models():
    """Load models from Hugging Face Hub"""
    global t5_model, t5_tokenizer, bert_model, bert_tokenizer
    
    # Set timeout for model loading (10 minutes for HF Spaces)
    timeout_seconds = 600
    
    # Load T5 model with retry mechanism and better error handling
    max_retries = 5
    for attempt in range(max_retries):
        try:
            logger.info(f"Loading T5 model from Hugging Face Hub... (attempt {attempt + 1}/{max_retries})")
            
            # Set timeout for the model loading
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Model loading timed out")
            
            # Set timeout for this attempt
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(300)  # 5 minutes per attempt
            
            try:
                t5_tokenizer = T5Tokenizer.from_pretrained(MODEL_CONFIG['t5_model_name'])
                t5_model = T5ForConditionalGeneration.from_pretrained(MODEL_CONFIG['t5_model_name'])
                signal.alarm(0)  # Cancel timeout
                logger.info("✅ T5 model loaded successfully")
                break
            except TimeoutError:
                signal.alarm(0)  # Cancel timeout
                raise TimeoutError("T5 model loading timed out")
                
        except Exception as e:
            signal.alarm(0)  # Cancel timeout
            logger.error(f"Error loading T5 model (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                t5_model = None
                t5_tokenizer = None
                logger.error("Failed to load T5 model after all attempts")
            else:
                logger.info(f"Retrying T5 model loading in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)  # Wait longer before retry
    
    # Load BERT model with similar retry mechanism
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Loading BERT model from Hugging Face Hub... (attempt {attempt + 1}/{max_retries})")
            bert_tokenizer = BertTokenizer.from_pretrained(MODEL_CONFIG['bert_model_name'])
            bert_model = BertForTokenClassification.from_pretrained(MODEL_CONFIG['bert_model_name'])
            logger.info("✅ BERT model loaded successfully")
            break
        except Exception as e:
            logger.error(f"Error loading BERT model (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                bert_model = None
                bert_tokenizer = None
                logger.error("Failed to load BERT model after all attempts")
            else:
                logger.info(f"Retrying BERT model loading in 3 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(3)

def correct_grammar(text):
    """Correct grammar using T5 model"""
    if t5_model is None or t5_tokenizer is None:
        return {"error": "T5 model not available"}
    
    try:
        # Prepare input for T5
        input_text = f"grammar: {text}"
        inputs = t5_tokenizer(input_text, return_tensors="pt", max_length=MODEL_CONFIG['max_length'], truncation=True)
        
        # Generate correction
        outputs = t5_model.generate(
            inputs.input_ids,
            max_length=MODEL_CONFIG['max_length'],
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2
        )
        
        corrected_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Return format expected by frontend
        return {
            "success": True,
            "original_text": text,
            "corrected_text": corrected_text
        }
    except Exception as e:
        logger.error(f"Error in grammar correction: {e}")
        return {"error": f"Grammar correction failed: {str(e)}"}

def detect_errors(text):
    """Detect grammar errors using BERT model"""
    if bert_model is None or bert_tokenizer is None:
        return {"error": "BERT model not available"}
    
    try:
        # Tokenize text
        inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=MODEL_CONFIG['max_length'])
        
        # Get predictions
        with torch.no_grad():
            outputs = bert_model(**inputs)
            logits = outputs.logits[0]  # Remove batch dimension
            probabilities = torch.softmax(logits, dim=1)
        
        # Get the most likely class for each token
        predictions = torch.argmax(logits, dim=1)
        
        # Convert tokens back to text for analysis
        tokens = bert_tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        
        # Analyze the predictions to identify potential errors
        error_positions = []
        confidence_scores = []
        
        # Look for tokens with high uncertainty (low confidence in prediction)
        for i, (token, prob_dist) in enumerate(zip(tokens, probabilities)):
            if token in ['[CLS]', '[SEP]', '[PAD]']:
                continue
                
            # Calculate confidence (entropy-based)
            entropy = -torch.sum(prob_dist * torch.log(prob_dist + 1e-10))
            confidence = 1.0 - (entropy / torch.log(torch.tensor(bert_model.config.num_labels)))
            
            # Flag as potential error if confidence is low
            if confidence < 0.7:  # Threshold for error detection
                error_positions.append(i)
                confidence_scores.append(float(confidence))
        
        # Calculate overall quality score
        if len(confidence_scores) > 0:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            quality_score = max(0, min(100, (1 - avg_confidence) * 100))
        else:
            quality_score = 0
        
        # Return format expected by frontend
        return {
            "text": text,
            "quality_score": quality_score,
            "error_count": len(error_positions),
            "errors_detected": len(error_positions) > 0,
            "confidence_scores": confidence_scores,
            "total_tokens": len(tokens),
            "potential_errors": len(error_positions),
            "fallback": False  # Indicates we're using the trained model
        }
        
    except Exception as e:
        logger.error(f"Error in error detection: {e}")
        return {"error": f"Error detection failed: {str(e)}"}

def analyze_text(text):
    """Analyze text for grammar and style"""
    correction_result = correct_grammar(text)
    detection_result = detect_errors(text)
    
    # Convert correction result to expected format
    if "error" not in correction_result:
        correction_result = {
            "original": correction_result.get("original_text", text),
            "corrected": correction_result.get("corrected_text", text)
        }
    
    return {
        "text": text,
        "correction": correction_result,
        "detection": detection_result
    }

@app.route('/')
def index():
    return render_template('multilingual.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "t5_model_loaded": t5_model is not None,
        "bert_model_loaded": bert_model is not None
    })

@app.route('/api/correct', methods=['POST'])
def correct():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = correct_grammar(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = detect_errors(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = analyze_text(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def languages():
    return jsonify({
        "languages": [
            {"code": "en", "name": "English", "supports_correction": True},
            {"code": "cs", "name": "Czech", "supports_correction": False},
            {"code": "de", "name": "German", "supports_correction": False},
            {"code": "it", "name": "Italian", "supports_correction": False},
            {"code": "sv", "name": "Swedish", "supports_correction": False}
        ]
    })

if __name__ == '__main__':
    logger.info("Starting Grammar Error Detection & Correction Service")
    logger.info("Loading models...")
    
    # Load models with timeout
    def timeout_handler(signum, frame):
        raise TimeoutError("Model loading timed out")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(300)  # 5 minutes timeout
    
    try:
        load_models()
        signal.alarm(0)  # Cancel timeout
        
        if t5_model is not None or bert_model is not None:
            logger.info("🎉 Service ready! At least one model loaded successfully")
        else:
            logger.error("❌ No models loaded successfully")
            exit(1)
            
    except TimeoutError:
        logger.error("❌ Model loading timed out")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Error loading models: {e}")
        exit(1)
    
    # Start Flask server
    logger.info("Starting Flask server on http://0.0.0.0:7860")
    app.run(host='0.0.0.0', port=7860, debug=False) 