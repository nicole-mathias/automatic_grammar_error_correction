# Hugging Face Spaces Deployment Guide

This repository is optimized for deployment on Hugging Face Spaces with a multilingual grammar error detection and correction service.

## 🚀 Quick Deployment Steps

1. **Fork this repository** to your GitHub account
2. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
3. **Click "Create new Space"**
4. **Configure your Space:**
   - **Owner**: Your Hugging Face username
   - **Space name**: `grammar-error-correction` (or your preferred name)
   - **License**: MIT
   - **SDK**: **Docker**
   - **Space hardware**: CPU (free tier) or GPU if needed
5. **Click "Create Space"**
6. **Connect your GitHub repository:**
   - Go to Settings → Repository
   - Select your forked repository
   - Set branch to `main`
7. **Deploy automatically** - no additional configuration needed!

## ✅ What's Included

- **Dockerfile** - Optimized for HF Spaces with port 7860
- **requirements.txt** - All necessary dependencies
- **app.py** - Main Flask application with multilingual support
- **templates/multilingual.html** - Modern web interface
- **models/** - Pre-trained BERT models for 5 languages
- **t5_jfleg/** - T5 model for grammar correction

## 🌍 Features

- **Multilingual Support**: English, Czech, German, Italian, Swedish
- **Grammar Error Detection**: Using fine-tuned BERT models for each language
- **Grammar Correction**: Using T5 model (English only)
- **Modern Web Interface**: Clean, responsive UI with real-time feedback
- **REST API**: Full API endpoints for integration
- **Error Handling**: Robust error handling and user feedback

## 🔧 API Endpoints

- `GET /` - Web interface
- `GET /api/health` - Health check
- `GET /api/languages` - Available languages and model status
- `POST /api/detect` - Error detection
- `POST /api/correct` - Grammar correction
- `POST /api/analyze` - Combined analysis

## 📊 Model Information

- **T5 Model**: Grammar correction (English only)
- **BERT Models**: Error detection for 5 languages
  - English: FCE dataset
  - Czech: GECCC dataset
  - German: Falko-Merlin dataset
  - Italian: Merlin dataset
  - Swedish: SWELL dataset
- **Model Size**: ~2GB total (automatically cached by HF)

## 🎯 Language Capabilities

| Language | Error Detection | Grammar Correction |
|----------|----------------|-------------------|
| English  | ✅ Yes         | ✅ Yes            |
| Czech    | ✅ Yes         | ❌ No             |
| German   | ✅ Yes         | ❌ No             |
| Italian  | ✅ Yes         | ❌ No             |
| Swedish  | ✅ Yes         | ❌ No             |

## 🚨 Troubleshooting

### If deployment fails:

1. **Check model files**: Ensure all model files are present in the repository
2. **Verify Dockerfile**: Make sure it's in the root directory
3. **Check requirements.txt**: Ensure all dependencies are listed
4. **Review HF Spaces logs**: Check for specific error messages
5. **Model loading issues**: Models are large, first deployment may take time

### Common Issues:

- **Port conflicts**: App uses port 7860 (HF Spaces default)
- **Memory issues**: Models require significant RAM
- **Timeout**: First model download may take several minutes

## 🧪 Local Testing

Test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access at http://localhost:7860
```

## 📝 Usage Examples

### Web Interface
1. Open the deployed Space URL
2. Select your language
3. Enter text to analyze
4. Choose: Detect Errors, Correct Grammar, or Full Analysis

### API Usage
```bash
# Error Detection
curl -X POST https://your-space.hf.space/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "I goes to the store", "language_code": "en"}'

# Grammar Correction
curl -X POST https://your-space.hf.space/api/correct \
  -H "Content-Type: application/json" \
  -d '{"text": "I goes to the store", "language_code": "en"}'
```

## 🔄 Updates

To update your deployed Space:
1. Push changes to your GitHub repository
2. HF Spaces will automatically rebuild and redeploy
3. Check the deployment logs for any issues

## 📞 Support

If you encounter issues:
1. Check the HF Spaces logs
2. Verify all files are present in your repository
3. Test locally first
4. Check the model loading status via `/api/health`

---

**Ready to deploy!** 🚀 