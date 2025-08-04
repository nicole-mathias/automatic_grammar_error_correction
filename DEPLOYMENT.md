# Deployment Guide

This guide provides step-by-step instructions for deploying the Multilingual Grammar Error Detection & Correction application to free platforms.

## Prerequisites

Before deploying, ensure you have:
- A GitHub repository with your code
- All model files in the correct directories
- A working local version of the application

## Free Deployment Platforms

### 1. Render (Recommended)

Render is one of the best free platforms for Python applications.

#### Setup Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: grammar-error-detection
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app_multilingual.py
   ```

4. **Environment Variables** (Optional)
   ```
   PORT=5002
   HOST=0.0.0.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete
   - Your app will be available at `https://your-app-name.onrender.com`

#### Advantages:
- Free tier available
- Automatic deployments from GitHub
- Custom domains supported
- Good performance

### 2. Railway

Railway offers simple deployment with automatic scaling.

#### Setup Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure**
   - Railway will auto-detect Python
   - Add environment variables if needed
   - Deploy automatically

4. **Access**
   - Railway provides a URL automatically
   - Can add custom domain

#### Advantages:
- Very simple setup
- Automatic deployments
- Good free tier
- Built-in monitoring

### 3. Fly.io

Fly.io offers global deployment with edge computing.

#### Setup Steps:

1. **Install flyctl**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly**
   ```bash
   fly auth login
   ```

3. **Create fly.toml**
   ```bash
   fly launch
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

#### Advantages:
- Global edge deployment
- Generous free tier
- Custom domains
- Good performance

### 4. Vercel (Alternative)

While primarily for frontend, Vercel can handle Python apps.

#### Setup Steps:

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Repository**
   - Click "New Project"
   - Import your GitHub repository

3. **Configure**
   - Add `vercel.json` to your project:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app_multilingual.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app_multilingual.py"
       }
     ]
   }
   ```

4. **Deploy**
   - Vercel will auto-deploy
   - Get your URL automatically

## Model File Management

### For Free Platforms

Since free platforms have limitations, consider these options:

1. **Use Base Models Only**
   - Modify the app to use base models when trained models aren't available
   - Add fallback logic in `app_multilingual.py`

2. **Host Models Separately**
   - Upload models to Google Drive or AWS S3
   - Download models at runtime (not recommended for production)

3. **Use Smaller Models**
   - Consider using smaller, quantized models
   - Optimize model loading for memory constraints

### Model Optimization

```python
# Add to app_multilingual.py for production
import os

# Check if models exist, fallback to base models
def load_models_safely():
    if os.path.exists('models/english/baseline_ft0_fce_3e.pt'):
        # Load trained models
        pass
    else:
        # Load base models
        pass
```

## Environment Configuration

### Create a Production Config

Create `config.py`:

```python
import os

class Config:
    DEBUG = False
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5002))
    
    # Model paths
    MODEL_PATH = os.getenv('MODEL_PATH', './models')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
```

### Update app_multilingual.py

```python
from config import Config

if __name__ == '__main__':
    load_all_models()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
```

## Performance Optimization

### For Free Platforms

1. **Reduce Memory Usage**
   ```python
   # Use CPU only
   import torch
   torch.set_num_threads(1)
   
   # Load models with map_location
   model = torch.load('model.pt', map_location='cpu')
   ```

2. **Optimize Model Loading**
   ```python
   # Lazy loading
   models = {}
   
   def get_model(language):
       if language not in models:
           models[language] = load_model(language)
       return models[language]
   ```

3. **Add Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_detection(text, language):
       return detect_errors(text, language)
   ```

## Monitoring and Logging

### Add Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### Health Check Endpoint

```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'models_loaded': len(bert_models),
        't5_loaded': t5_model is not None,
        'timestamp': datetime.now().isoformat()
    }
```

## Troubleshooting Deployment

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for all dependencies
   - Ensure Python version compatibility
   - Verify file paths

2. **Runtime Errors**
   - Check logs for model loading errors
   - Verify environment variables
   - Test locally first

3. **Memory Issues**
   - Use smaller models
   - Implement lazy loading
   - Add memory monitoring

### Debug Commands

```bash
# Check application logs
fly logs
railway logs
render logs

# SSH into deployment (if available)
fly ssh console
railway shell
```

## Cost Optimization

### Free Tier Limits

- **Render**: 750 hours/month free
- **Railway**: $5 credit/month
- **Fly.io**: 3 shared-cpu-1x 256mb VMs
- **Vercel**: 100GB-hours/month

### Optimization Tips

1. **Use Free Hours Wisely**
   - Deploy only when needed
   - Use sleep mode when possible

2. **Optimize Resource Usage**
   - Use smaller models
   - Implement caching
   - Reduce memory footprint

3. **Monitor Usage**
   - Track API calls
   - Monitor memory usage
   - Set up alerts

## Security Considerations

### For Production

1. **Environment Variables**
   ```bash
   SECRET_KEY=your-secure-secret-key
   DEBUG=False
   ```

2. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app)
   
   @app.route('/api/detect')
   @limiter.limit("10 per minute")
   def api_detect():
       # Your code here
   ```

3. **Input Validation**
   ```python
   from flask import abort
   
   def validate_input(text):
       if len(text) > 1000:
           abort(400, description="Text too long")
       return text
   ```

## Next Steps

After successful deployment:

1. **Test All Features**
   - Test all language models
   - Verify API endpoints
   - Check performance

2. **Set Up Monitoring**
   - Add error tracking
   - Monitor response times
   - Set up alerts

3. **Optimize Performance**
   - Implement caching
   - Optimize model loading
   - Add CDN if needed

4. **Documentation**
   - Update README with deployment URL
   - Document API usage
   - Add troubleshooting guide

---

**Note**: Free platforms have limitations. For production use, consider paid options or self-hosting for better performance and reliability. 