import os
import logging
import torch
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForTokenClassification, T5Tokenizer, T5ForConditionalGeneration, DistilBertForTokenClassification
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model variables
bert_models = {}
bert_tokenizers = {}
t5_model = None
t5_tokenizer = None

# Language configuration
LANGUAGES = {
    'english': {
        'name': 'English',
        'model_path': 'models/english/baseline_ft0_fce_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'FCE',
        'accuracy': None,
        'supports_correction': True,
        'description': 'Grammar Error Detection and Correction'
    },
    'czech': {
        'name': 'Czech',
        'model_path': 'models/czech/ft1_cs_geccc_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'GECCC',
        'accuracy': None,
        'supports_correction': False,
        'description': 'Grammar Error Detection'
    },
    'german': {
        'name': 'German',
        'model_path': 'models/german/ft2_de_falko-merlin_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'FALKO-MERLIN',
        'accuracy': None,
        'supports_correction': False,
        'description': 'Grammar Error Detection'
    },
    'italian': {
        'name': 'Italian',
        'model_path': 'models/italian/ft3_it_merlin_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'MERLIN',
        'accuracy': None,
        'supports_correction': False,
        'description': 'Grammar Error Detection'
    },
    'swedish': {
        'name': 'Swedish',
        'model_path': 'models/swedish/ft4_sv_swell_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'SWELL',
        'accuracy': None,
        'supports_correction': False,
        'description': 'Grammar Error Detection'
    }
}

# Test sentences for accuracy calculation
TEST_SENTENCES = {
    'english': [
        ("I goes to the store yesterday.", [0, 1, 0, 0, 0, 0, 0, 0]),
        ("She have three cats.", [0, 0, 1, 0, 0, 0]),
        ("They was at the party.", [0, 0, 1, 0, 0, 0, 0]),
        ("He don't like coffee.", [0, 0, 1, 0, 0, 0]),
        ("We is going home.", [0, 0, 1, 0, 0, 0]),
        ("The cat sleep on the bed.", [0, 0, 0, 1, 0, 0, 0, 0]),
        ("I buyed a new car.", [0, 0, 1, 0, 0, 0, 0]),
        ("She teached me English.", [0, 0, 1, 0, 0, 0]),
        ("They bringed gifts.", [0, 0, 1, 0, 0]),
        ("He catched the ball.", [0, 0, 1, 0, 0, 0])
    ],
    'german': [
        ("Ich geht zur Schule.", [0, 1, 0, 0, 0]),
        ("Du haben ein Auto.", [0, 0, 1, 0, 0, 0]),
        ("Er ist ein Student.", [0, 0, 0, 0, 0, 0]),
        ("Wir sind hier.", [0, 0, 0, 0, 0]),
        ("Sie haben Zeit.", [0, 0, 0, 0, 0]),
        ("Das ist gut.", [0, 0, 0, 0, 0]),
        ("Ich bin müde.", [0, 0, 0, 0, 0]),
        ("Du bist schön.", [0, 0, 0, 0, 0]),
        ("Er hat Hunger.", [0, 0, 0, 0, 0]),
        ("Wir sind fertig.", [0, 0, 0, 0, 0])
    ],
    'italian': [
        ("Io vado al negozio.", [0, 0, 0, 0, 0, 0]),
        ("Tu hai una macchina.", [0, 0, 0, 0, 0, 0]),
        ("Lui è un studente.", [0, 0, 0, 0, 0, 0]),
        ("Noi siamo qui.", [0, 0, 0, 0, 0]),
        ("Voi avete tempo.", [0, 0, 0, 0, 0]),
        ("Questo è buono.", [0, 0, 0, 0, 0]),
        ("Io sono stanco.", [0, 0, 0, 0, 0]),
        ("Tu sei bella.", [0, 0, 0, 0, 0]),
        ("Lui ha fame.", [0, 0, 0, 0, 0]),
        ("Noi siamo pronti.", [0, 0, 0, 0, 0])
    ],
    'czech': [
        ("Já jdu do obchodu.", [0, 0, 0, 0, 0, 0]),
        ("Ty máš auto.", [0, 0, 0, 0, 0]),
        ("On je student.", [0, 0, 0, 0, 0]),
        ("My jsme tady.", [0, 0, 0, 0, 0]),
        ("Vy máte čas.", [0, 0, 0, 0, 0]),
        ("Toto je dobré.", [0, 0, 0, 0, 0]),
        ("Já jsem unavený.", [0, 0, 0, 0, 0, 0]),
        ("Ty jsi krásná.", [0, 0, 0, 0, 0]),
        ("On má hlad.", [0, 0, 0, 0, 0]),
        ("My jsme připraveni.", [0, 0, 0, 0, 0])
    ],
    'swedish': [
        ("Jag går till affären.", [0, 0, 0, 0, 0, 0]),
        ("Du har en bil.", [0, 0, 0, 0, 0, 0]),
        ("Han är en student.", [0, 0, 0, 0, 0, 0]),
        ("Vi är här.", [0, 0, 0, 0, 0]),
        ("Ni har tid.", [0, 0, 0, 0, 0]),
        ("Detta är bra.", [0, 0, 0, 0, 0]),
        ("Jag är trött.", [0, 0, 0, 0, 0]),
        ("Du är vacker.", [0, 0, 0, 0, 0]),
        ("Han har hunger.", [0, 0, 0, 0, 0]),
        ("Vi är redo.", [0, 0, 0, 0, 0])
    ]
}

def calculate_model_accuracy(language):
    """Calculate real accuracy for a language model using test sentences"""
    if language not in bert_models or language not in TEST_SENTENCES:
        return None
    
    model = bert_models[language]
    tokenizer = bert_tokenizers[language]
    test_sentences = TEST_SENTENCES[language]
    
    total_correct = 0
    total_tokens = 0
    
    try:
        for sentence, expected_labels in test_sentences:
            inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=2)
            
            predicted_labels = []
            for i, pred in enumerate(predictions[0]):
                if i == 0:  # Skip [CLS] token
                    continue
                if i >= len(predictions[0]) - 1:  # Skip [SEP] token
                    break
                predicted_labels.append(1 if pred.item() == 1 else 0)
            
            for pred, expected in zip(predicted_labels, expected_labels):
                if pred == expected:
                    total_correct += 1
                total_tokens += 1
        
        if total_tokens > 0:
            accuracy = total_correct / total_tokens
            logger.info(f"Calculated accuracy for {language}: {accuracy:.3f} ({total_correct}/{total_tokens})")
            return accuracy
        else:
            return None
            
    except Exception as e:
        logger.error(f"Error calculating accuracy for {language}: {e}")
        return None

def load_t5_model():
    """Load the T5 model for grammar correction (English only)"""
    global t5_model, t5_tokenizer
    try:
        model_path = "t5_jfleg/saved_model/model/"
        if os.path.exists(model_path) and os.listdir(model_path):
            logger.info(f"Loading trained T5 model from {model_path}")
            t5_tokenizer = T5Tokenizer.from_pretrained("t5-base")
            t5_model = T5ForConditionalGeneration.from_pretrained(model_path)
            logger.info("Trained T5 model loaded successfully")
            return True
        else:
            logger.info("Trained T5 model not found, loading base model")
            t5_tokenizer = T5Tokenizer.from_pretrained("t5-base")
            t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
            logger.info("T5 base model loaded successfully")
            return False
    except Exception as e:
        logger.error(f"Error loading T5 model: {e}")
        return False

def load_bert_model(language):
    """Load BERT model for a specific language"""
    global bert_models, bert_tokenizers
    
    if language in bert_models:
        return True
    
    try:
        lang_config = LANGUAGES[language]
        model_path = lang_config['model_path']
        
        if os.path.exists(model_path):
            logger.info(f"Loading {language} BERT model from {model_path}")
            bert_models[language] = torch.load(model_path, map_location='cpu')
            bert_tokenizers[language] = AutoTokenizer.from_pretrained(lang_config['tokenizer_name'])
            logger.info(f"{language.capitalize()} BERT model loaded successfully")
            return True
        else:
            logger.warning(f"Model file not found for {language}: {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading {language} BERT model: {e}")
        return False

def load_all_models():
    """Load all language models"""
    logger.info("Loading all language models...")
    
    t5_loaded = load_t5_model()
    
    loaded_count = 0
    for language in LANGUAGES.keys():
        if load_bert_model(language):
            loaded_count += 1
    
    logger.info(f"Models loaded: {loaded_count}/{len(LANGUAGES)} languages")
    
    logger.info("Calculating model accuracies...")
    for language in LANGUAGES.keys():
        if language in bert_models:
            accuracy = calculate_model_accuracy(language)
            if accuracy is not None:
                LANGUAGES[language]['accuracy'] = accuracy
    
    if t5_loaded:
        logger.info("T5 model loaded successfully")
    else:
        logger.warning("T5 model loaded with limited capability")
    
    for language in LANGUAGES.keys():
        if language in bert_models:
            logger.info(f"{language.capitalize()} model loaded successfully")
        else:
            logger.warning(f"{language.capitalize()} model not loaded")
    
    logger.info("Service ready! Starting Flask server")

def correct_grammar(text, language='english'):
    """Correct grammar errors in text using T5 model (English only)"""
    if language != 'english':
        return {"error": "Grammar correction is only available for English"}
    
    if t5_model is None or t5_tokenizer is None:
        return {"error": "T5 model not loaded"}
    
    try:
        input_text = f"grammar: {text}"
        inputs = t5_tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        with torch.no_grad():
            outputs = t5_model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
        
        corrected_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "corrected_text": corrected_text,
            "model_type": "trained" if "t5_jfleg" in str(t5_model) else "base"
        }
        
    except Exception as e:
        logger.error(f"Error in grammar correction: {e}")
        return {"error": f"Error in grammar correction: {e}"}

def detect_errors(text, language):
    """Detect grammar errors in text using the specified language model"""
    try:
        if language not in bert_models or bert_models[language] is None:
            return {"error": f"Model for {language} not loaded"}
        
        bert_model = bert_models[language]
        bert_tokenizer = bert_tokenizers[language]
        
        inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = bert_model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=2)
            probabilities = torch.softmax(outputs.logits, dim=2)
            confidence_scores = torch.max(probabilities, dim=2)[0]
        
        tokens = bert_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        tags = []
        
        if len(predictions.shape) > 1:
            pred_sequence = predictions[0]
            conf_sequence = confidence_scores[0]
        else:
            pred_sequence = predictions
            conf_sequence = confidence_scores
        
        for i, (pred, conf) in enumerate(zip(pred_sequence, conf_sequence)):
            if i < len(tokens):
                try:
                    if pred.numel() == 1:
                        pred_value = pred.item()
                        conf_value = conf.item()
                    else:
                        pred_value = pred[0].item() if len(pred.shape) > 0 else pred.item()
                        conf_value = conf[0].item() if len(conf.shape) > 0 else conf.item()
                    
                    tag = "i" if pred_value == 1 else "c"
                    tags.append({
                        "token": tokens[i], 
                        "tag": tag, 
                        "confidence": round(conf_value, 3)
                    })
                except Exception as e:
                    logger.warning(f"Error processing prediction {i}: {e}")
                    tags.append({
                        "token": tokens[i], 
                        "tag": "c", 
                        "confidence": 0.5
                    })
        
        avg_confidence = sum(tag["confidence"] for tag in tags) / len(tags) if tags else 0
        
        return {
            "tokens": tags,
            "accuracy": LANGUAGES[language]['accuracy'],
            "dataset": LANGUAGES[language]['dataset'],
            "avg_confidence": round(avg_confidence, 3),
            "low_confidence_warning": avg_confidence < 0.7
        }
        
    except Exception as e:
        logger.error(f"Error in error detection: {e}")
        return {"error": f"Error in error detection: {e}"}

@app.route('/')
def index():
    return render_template('multilingual.html')

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get available languages and their status"""
    current_models = {lang: lang in bert_models for lang in LANGUAGES.keys()}
    return jsonify({
        "languages": {lang: {"config": config, "loaded": current_models[lang]} 
                     for lang, config in LANGUAGES.items()},
        "status": "healthy",
        "t5_model_loaded": t5_model is not None,
        "total_models_loaded": sum(current_models.values()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/correct', methods=['POST'])
def api_correct():
    """API endpoint for grammar correction"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'english')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = correct_grammar(text, language)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in correction API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect', methods=['POST'])
def api_detect():
    """API endpoint for error detection"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'english')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = detect_errors(text, language)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in detection API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for combined analysis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'english')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        detection_result = detect_errors(text, language)
        correction_result = correct_grammar(text, language) if language == 'english' else {"error": "Correction not available"}
        
        return jsonify({
            "detection": detection_result,
            "correction": correction_result
        })
        
    except Exception as e:
        logger.error(f"Error in analysis API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len(bert_models),
        "t5_loaded": t5_model is not None
    })

if __name__ == '__main__':
    logger.info("🚀 Starting Multi-Language Grammar Error Detection & Correction Service")
    load_all_models()
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🎉 Service ready! Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False) 