# Multilingual Grammar Error Detection & Correction

A sophisticated web application that leverages advanced AI models to detect and correct grammar errors across multiple languages. Built with Flask, PyTorch, and Transformers, this system provides real-time grammar analysis with confidence scoring and performance metrics.

## Features

### Core Capabilities
- **Multilingual Support**: Grammar error detection for English, German, Italian, Czech, and Swedish
- **Grammar Correction**: Advanced T5-based correction for English text
- **Real-time Analysis**: Instant processing with confidence scoring
- **Performance Metrics**: Dynamic accuracy calculation and model performance visualization
- **User-friendly Interface**: Clean, responsive web interface with language selection

### Technical Features
- **AI-Powered Detection**: DistilBERT models trained on language-specific datasets
- **Advanced Correction**: T5 transformer model for English grammar correction
- **Confidence Scoring**: Token-level confidence indicators for analysis reliability
- **Model Performance**: Real-time accuracy calculation and visualization
- **RESTful API**: Comprehensive API endpoints for integration

## Supported Languages

| Language | Detection | Correction | Dataset | Model |
|----------|-----------|------------|---------|-------|
| English  | ✅ | ✅ | FCE | DistilBERT + T5 |
| German   | ✅ | ❌ | FALKO-MERLIN | DistilBERT |
| Italian  | ✅ | ❌ | MERLIN | DistilBERT |
| Czech    | ✅ | ❌ | GECCC | DistilBERT |
| Swedish  | ✅ | ❌ | SWELL | DistilBERT |

## Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd automatic_grammar_error_correction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download models** (if not already present)
   - Place trained model files in the `models/` directory
   - Ensure T5 model is in `t5_jfleg/saved_model/model/`

5. **Run the application**
   ```bash
   python app_multilingual.py
   ```

6. **Access the application**
   - Open browser and navigate to `http://localhost:5002`
   - The application will be ready for use

## Usage

### Web Interface
1. **Select Language**: Choose from the available languages
2. **Enter Text**: Input text for analysis in the text area
3. **Analyze**: Click "Detect Grammar Errors" for error detection
4. **Correct**: For English, use "Correct Grammar" for automated corrections
5. **View Results**: See highlighted errors and confidence scores

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Get Available Languages
```bash
GET /api/languages
```

#### Detect Grammar Errors
```bash
POST /api/detect
Content-Type: application/json

{
    "text": "I goes to the store yesterday.",
    "language": "english"
}
```

#### Correct Grammar (English only)
```bash
POST /api/correct
Content-Type: application/json

{
    "text": "I goes to the store yesterday.",
    "language": "english"
}
```

#### Combined Analysis
```bash
POST /api/analyze
Content-Type: application/json

{
    "text": "I goes to the store yesterday.",
    "language": "english"
}
```

## Model Architecture

### Error Detection
- **Model**: DistilBERT for Token Classification
- **Task**: Binary classification (correct/incorrect) for each token
- **Training**: Fine-tuned on language-specific grammar error datasets
- **Output**: Token-level predictions with confidence scores

### Grammar Correction
- **Model**: T5 Transformer
- **Task**: Sequence-to-sequence text correction
- **Training**: Fine-tuned on English grammar correction datasets
- **Output**: Corrected text with improved grammar

## Performance Metrics

The application calculates real-time accuracy based on test sentences:

- **English**: 81.7% accuracy (FCE dataset)
- **German**: 94.7% accuracy (FALKO-MERLIN dataset)
- **Italian**: 96.6% accuracy (MERLIN dataset)
- **Czech**: 85.2% accuracy (GECCC dataset)
- **Swedish**: 86.0% accuracy (SWELL dataset)

## Deployment

### Local Development
```bash
python app_multilingual.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5002 app_multilingual:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5002

CMD ["python", "app_multilingual.py"]
```

### Free Deployment Platforms

#### 1. Render
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `python app_multilingual.py`
- Environment: Python 3.9

#### 2. Railway
- Connect your GitHub repository
- Automatic deployment from main branch
- Environment variables handled automatically

#### 3. Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and deploy
fly auth login
fly launch
fly deploy
```

#### 4. Heroku (Free tier discontinued, but paid options available)
```bash
# Create Procfile
echo "web: python app_multilingual.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## Configuration

### Environment Variables
- `PORT`: Application port (default: 5002)
- `HOST`: Application host (default: 0.0.0.0)
- `DEBUG`: Debug mode (default: False)

### Model Configuration
Models are configured in `app_multilingual.py`:
```python
LANGUAGES = {
    'english': {
        'name': 'English',
        'model_path': 'models/english/baseline_ft0_fce_3e.pt',
        'tokenizer_name': 'distilbert-base-multilingual-cased',
        'dataset': 'FCE',
        'supports_correction': True,
        'description': 'Grammar Detection and Correction'
    }
    # ... other languages
}
```

## API Response Format

### Error Detection Response
```json
{
    "tokens": [
        {
            "token": "I",
            "tag": "c",
            "confidence": 0.95
        },
        {
            "token": "goes",
            "tag": "i",
            "confidence": 0.87
        }
    ],
    "accuracy": 0.817,
    "dataset": "FCE",
    "avg_confidence": 0.91,
    "low_confidence_warning": false
}
```

### Grammar Correction Response
```json
{
    "corrected_text": "I went to the store yesterday.",
    "model_type": "trained"
}
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -ti:5002 | xargs kill -9
   ```

2. **Model loading errors**
   - Ensure model files are in correct directories
   - Check file permissions
   - Verify model file integrity

3. **Memory issues**
   - Reduce batch size in model configuration
   - Use CPU-only mode for deployment
   - Consider model quantization

### Performance Optimization

1. **Model Loading**
   - Models are loaded once at startup
   - Consider lazy loading for large models
   - Implement model caching

2. **Response Time**
   - Optimize tokenization
   - Use batch processing for multiple requests
   - Implement request queuing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face Transformers library
- PyTorch for deep learning capabilities
- Flask for web framework
- Chart.js for data visualization

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Note**: This application requires trained models to function properly. Ensure all model files are present in the correct directories before deployment.








