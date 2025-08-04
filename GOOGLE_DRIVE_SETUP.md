# Google Drive Setup for Railway Deployment

## Step 1: Get Google Drive File IDs

To make your models accessible to Railway, you need to:

1. **Upload your models to Google Drive** (if not already done)
2. **Make them publicly accessible**
3. **Get the file IDs**

### How to get Google Drive File IDs:

1. **Upload your model files to Google Drive**
2. **Right-click on each file** → **Get link**
3. **Click "Copy link"**
4. **The link will look like**: `https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing`
5. **Extract the FILE_ID_HERE part** (the long string between `/d/` and `/view`)

### Example:
- Link: `https://drive.google.com/file/d/1ABC123DEF456GHI789/view?usp=sharing`
- File ID: `1ABC123DEF456GHI789`

## Step 2: Update the download_models.py file

Replace the placeholder IDs in `download_models.py` with your actual file IDs:

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

## Step 3: Make Files Public

For Railway to download the files, they must be publicly accessible:

1. **Right-click on each file** in Google Drive
2. **Click "Share"**
3. **Click "Change to anyone with the link"**
4. **Set permission to "Viewer"**
5. **Click "Done"**

## Step 4: Test the Download

Before deploying, test the download script locally:

```bash
python download_models.py
```

## Step 5: Deploy to Railway

Once you've updated the file IDs, commit and push:

```bash
git add .
git commit -m "Add model download script for Railway deployment"
git push origin main
```

Then deploy to Railway - it will automatically download the models during deployment.

## Alternative: Direct Download Links

If you prefer, you can also:
1. Upload to a file hosting service (like Dropbox, OneDrive)
2. Get direct download links
3. Replace the Google Drive URLs with direct download URLs

## File Structure Expected

The script expects these files:
- `models/english/baseline_ft0_fce_3e.pt`
- `models/czech/ft1_cs_geccc_3e.pt`
- `models/german/ft2_de_falko-merlin_3e.pt`
- `models/italian/ft3_it_merlin_3e.pt`
- `models/swedish/ft4_sv_swell_3e.pt`
- `t5_jfleg/saved_model/model/` (T5 model files)

## Troubleshooting

If Railway fails to download models:
1. Check that file IDs are correct
2. Verify files are publicly accessible
3. Check Railway logs for download errors
4. Consider using a different hosting service 