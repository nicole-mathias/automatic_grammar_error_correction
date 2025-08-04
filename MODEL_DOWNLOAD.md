# Model Download Guide

## Overview

This application can work with base models (automatically downloaded), but for optimal performance, you can download the trained models.

## Option 1: Use Base Models (Recommended for Deployment)

The application will automatically download and use base models if trained models are not found. This is perfect for:
- Quick testing
- Deployment to free platforms
- Limited storage environments

## Option 2: Download Trained Models (For Best Performance)

### Download Links

**Trained Models (Google Drive):**
- [Multilingual BERT Models](https://drive.google.com/drive/folders/1crPqOBruLN-WtZ74oDApQVToiv4bqgun?usp=sharing)
- [T5 Grammar Correction Model](https://drive.google.com/drive/folders/1gQZLJ_zvLWI3AyUDfFJ8oSPbin4GJDD4?usp=drive_link)

### Setup Instructions

1. **Download BERT Models:**
   ```bash
   # Create models directory structure
   mkdir -p models/{english,czech,german,italian,swedish}
   
   # Download and place the .pt files:
   # - baseline_ft0_fce_3e.pt → models/english/
   # - ft1_cs_geccc_3e.pt → models/czech/
   # - ft2_de_falko-merlin_3e.pt → models/german/
   # - ft3_it_merlin_3e.pt → models/italian/
   # - ft4_sv_swell_3e.pt → models/swedish/
   ```

2. **Download T5 Model:**
   ```bash
   # Download the t5_model folder contents
   # Place all files in: t5_jfleg/saved_model/model/
   ```

### File Structure

After downloading, your structure should look like:

```
models/
├── english/
│   └── baseline_ft0_fce_3e.pt
├── czech/
│   └── ft1_cs_geccc_3e.pt
├── german/
│   └── ft2_de_falko-merlin_3e.pt
├── italian/
│   └── ft3_it_merlin_3e.pt
└── swedish/
    └── ft4_sv_swell_3e.pt

t5_jfleg/
└── saved_model/
    └── model/
        ├── pytorch_model.bin
        ├── config.json
        ├── tokenizer.json
        └── ... (other T5 files)
```

## Model Sizes

- **BERT Models**: ~514MB each (2.5GB total)
- **T5 Model**: ~850MB
- **Total with trained models**: ~3.3GB

## Performance Comparison

| Model Type | Detection Accuracy | Correction Quality | Memory Usage |
|------------|-------------------|-------------------|--------------|
| Base Models | ~60-70% | Basic | Low |
| Trained Models | ~80-95% | Excellent | High |

## Deployment Considerations

### Free Platforms
- **Render**: Use base models (free tier has memory limits)
- **Railway**: Use base models (limited resources)
- **Fly.io**: Can handle trained models (generous free tier)

### Paid Platforms
- **Heroku**: Can handle trained models
- **AWS/GCP**: Can handle trained models
- **Self-hosted**: Can handle trained models

## Quick Start

1. **For immediate testing:**
   ```bash
   ./deploy.sh
   ```

2. **For best performance:**
   - Download trained models
   - Place them in correct directories
   - Run `./deploy.sh`

## Troubleshooting

### Model Loading Errors
- Ensure model files are in correct directories
- Check file permissions
- Verify file integrity

### Memory Issues
- Use base models for deployment
- Consider model quantization
- Use CPU-only mode

### Download Issues
- Check internet connection
- Verify Google Drive access
- Try alternative download methods 