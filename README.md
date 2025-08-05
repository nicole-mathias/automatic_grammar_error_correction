# Multilingual Grammar Error Detection & Correction

A powerful web application for detecting and correcting grammar errors in multiple languages using state-of-the-art AI models.

## 🌍 Supported Languages

- **English** - Error detection + Grammar correction
- **Czech** - Error detection only
- **German** - Error detection only  
- **Italian** - Error detection only
- **Swedish** - Error detection only

## ✨ Features

- **🔍 Grammar Error Detection**: Identifies grammar errors with confidence scores
- **✏️ Grammar Correction**: Corrects errors (English only)
- **🌐 Multilingual Support**: 5 languages with specialized models
- **🎨 Modern UI**: Clean, responsive web interface
- **🔧 REST API**: Full API for integration
- **📊 Detailed Analysis**: Error statistics and confidence scores

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd automatic_grammar_error_correction

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open http://localhost:7860
```

### Hugging Face Spaces Deployment

See [README_HF_SPACES.md](README_HF_SPACES.md) for detailed deployment instructions.

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/health` | GET | Health check |
| `/api/languages` | GET | Available languages |
| `/api/detect` | POST | Error detection |
| `/api/correct` | POST | Grammar correction |
| `/api/analyze` | POST | Combined analysis |

### Example API Usage

```bash
# Error Detection
curl -X POST http://localhost:7860/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "I goes to the store", "language_code": "en"}'

# Grammar Correction
curl -X POST http://localhost:7860/api/correct \
  -H "Content-Type: application/json" \
  -d '{"text": "I goes to the store", "language_code": "en"}'
```

## 📊 Model Information

- **T5 Model**: Grammar correction (English only)
- **BERT Models**: Error detection for each language
  - English: FCE dataset
  - Czech: GECCC dataset  
  - German: Falko-Merlin dataset
  - Italian: Merlin dataset
  - Swedish: SWELL dataset

## 🎯 Language Capabilities

| Language | Error Detection | Grammar Correction | Model |
|----------|----------------|-------------------|-------|
| English  | ✅ Yes         | ✅ Yes            | FCE   |
| Czech    | ✅ Yes         | ❌ No             | GECCC |
| German   | ✅ Yes         | ❌ No             | Falko-Merlin |
| Italian  | ✅ Yes         | ❌ No             | Merlin |
| Swedish  | ✅ Yes         | ❌ No             | SWELL |

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Models**: Transformers (BERT, T5)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Hugging Face Spaces
- **Dependencies**: PyTorch, Transformers, NumPy

## 📁 Project Structure

```
automatic_grammar_error_correction/
├── app.py                 # Main Flask application
├── templates/
│   └── multilingual.html  # Web interface
├── models/                # BERT models for each language
├── t5_jfleg/             # T5 model for correction
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README_HF_SPACES.md   # Deployment guide
```

## 🔍 Usage Examples

### Web Interface
1. Select your language from the dropdown
2. Enter text to analyze
3. Choose an action:
   - **Detect Errors**: Find grammar errors
   - **Correct Grammar**: Fix errors (English only)
   - **Full Analysis**: Both detection and correction

### API Response Examples

**Error Detection:**
```json
{
  "accuracy": 0.806,
  "avg_confidence": 0.921,
  "dataset": "FCE",
  "tokens": [
    {"token": "I", "tag": "c", "confidence": 0.95},
    {"token": "goes", "tag": "i", "confidence": 0.86}
  ]
}
```

**Grammar Correction:**
```json
{
  "success": true,
  "corrected_text": "I go to the store",
  "original_text": "I goes to the store"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Loading**: First run may take time to download models
2. **Memory**: Models require significant RAM (~2GB)
3. **Port Conflicts**: App uses port 7860 by default

### Health Check

```bash
curl http://localhost:7860/api/health
```

## 📈 Performance

- **Error Detection**: ~80-85% accuracy across languages
- **Grammar Correction**: ~90% accuracy for English
- **Response Time**: 1-3 seconds per request
- **Model Size**: ~2GB total

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Hugging Face for the Transformers library
- The research teams behind the fine-tuned models
- The open-source community for various tools and libraries

---

**Ready for deployment!** 🚀

For deployment instructions, see [README_HF_SPACES.md](README_HF_SPACES.md).








