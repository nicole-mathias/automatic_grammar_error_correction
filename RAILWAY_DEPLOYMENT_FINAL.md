# Railway Deployment Guide - Final

## Option 1: Environment Variables (Recommended)

This approach uses Railway's environment variables to store Google Drive file IDs.

### Step 1: Get Google Drive File IDs

1. **Upload your model files to Google Drive**
2. **Right-click on each file** → **Get link**
3. **Click "Copy link"**
4. **Extract the file ID** from the URL:
   - URL: `https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing`
   - File ID: `FILE_ID_HERE`

### Step 2: Make Files Public

1. **Right-click on each file** in Google Drive
2. **Click "Share"**
3. **Click "Change to anyone with the link"**
4. **Set permission to "Viewer"**
5. **Click "Done"**

### Step 3: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**: `nicole-mathias/automatic_grammar_error_correction`

### Step 4: Set Environment Variables

In your Railway project dashboard:

1. **Go to your project**
2. **Click "Variables" tab**
3. **Add these environment variables**:

```
ENGLISH_MODEL_ID=your_english_file_id_here
CZECH_MODEL_ID=your_czech_file_id_here
GERMAN_MODEL_ID=your_german_file_id_here
ITALIAN_MODEL_ID=your_italian_file_id_here
SWEDISH_MODEL_ID=your_swedish_file_id_here
T5_MODEL_ID=your_t5_file_id_here
```

### Step 5: Deploy

Railway will automatically:
1. Install dependencies from `requirements.txt`
2. Run `download_models_env.py` to download models
3. Start `app_multilingual.py`
4. Make your app available at the provided URL

## Option 2: Direct File IDs in Code

If you prefer to hardcode the file IDs:

### Step 1: Update download_models.py

Replace the placeholder IDs in `download_models.py`:

```python
MODEL_FILES = {
    'english': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_ACTUAL_ENGLISH_FILE_ID',
        'filename': 'baseline_ft0_fce_3e.pt'
    },
    'czech': {
        'url': 'https://drive.google.com/uc?export=download&id=YOUR_ACTUAL_CZECH_FILE_ID',
        'filename': 'ft1_cs_geccc_3e.pt'
    },
    # ... etc for all models
}
```

### Step 2: Update railway.json

Change the start command back to:

```json
{
  "deploy": {
    "startCommand": "python download_models.py && python app_multilingual.py"
  }
}
```

### Step 3: Deploy

Follow the same deployment steps as Option 1, but skip the environment variables step.

## File Structure

The deployment expects these files to be downloaded:

```
models/
├── english/baseline_ft0_fce_3e.pt
├── czech/ft1_cs_geccc_3e.pt
├── german/ft2_de_falko-merlin_3e.pt
├── italian/ft3_it_merlin_3e.pt
└── swedish/ft4_sv_swell_3e.pt

t5_jfleg/saved_model/model/
├── pytorch_model.bin
├── config.json
└── tokenizer.json
```

## Testing Locally

Before deploying, test the download script:

```bash
# For environment variables approach
export ENGLISH_MODEL_ID=your_id_here
export CZECH_MODEL_ID=your_id_here
# ... etc
python download_models_env.py

# For direct approach
python download_models.py
```

## Troubleshooting

### Common Issues:

1. **Models not downloading**:
   - Check file IDs are correct
   - Verify files are publicly accessible
   - Check Railway logs for errors

2. **App not starting**:
   - Check Railway logs for Python errors
   - Verify all dependencies are in `requirements.txt`

3. **Health check failing**:
   - Increase `healthcheckTimeout` in `railway.json`
   - Check if models are downloading correctly

### Railway Logs

To check Railway logs:
1. Go to your Railway project
2. Click on your service
3. Click "Logs" tab
4. Look for download progress and any errors

## Alternative Hosting

If Google Drive doesn't work, try:
- **Dropbox**: Upload files and get direct download links
- **OneDrive**: Similar to Dropbox
- **GitHub Releases**: Upload as release assets
- **AWS S3**: Upload to S3 bucket with public access

## Cost Optimization

Railway's free tier includes:
- 500 hours/month
- 512MB RAM
- 1GB storage

For larger models, consider:
- Using compressed model files
- Implementing model caching
- Using a paid Railway plan

## Security Notes

- Environment variables are encrypted in Railway
- Don't commit file IDs to public repositories
- Use environment variables for sensitive data
- Regularly rotate access tokens if using API keys 