# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Install Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Or using Homebrew (macOS)
brew install railway
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize Project
```bash
# Navigate to your project directory
cd automatic_grammar_error_correction

# Initialize Railway project
railway init
```

### Step 4: Deploy
```bash
# Deploy to Railway
railway up
```

### Step 5: Get Your URL
```bash
# Get your deployment URL
railway status
```

## Alternative: Deploy via GitHub

### Step 1: Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Railway deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect it's a Python app

### Step 3: Configure Environment
Railway will automatically:
- Install dependencies from `requirements.txt`
- Use Python 3.9 (from `runtime.txt`)
- Start the app using the `Procfile`

## Environment Variables (Optional)

You can set these in Railway dashboard:

```bash
PORT=5002
PYTHON_VERSION=3.9.16
```

## Monitoring Your App

### View Logs
```bash
railway logs
```

### Check Status
```bash
railway status
```

### Open in Browser
```bash
railway open
```

## Railway Free Tier Limits

- **$5 credit/month** (about 500 hours of runtime)
- **512MB RAM** per service
- **1GB storage**
- **Custom domains** supported
- **Automatic deployments** from GitHub

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` is correct
   - Ensure Python version in `runtime.txt`

2. **App Won't Start**
   - Check logs: `railway logs`
   - Verify port configuration in app

3. **Memory Issues**
   - Railway free tier has 512MB RAM
   - Consider using base models instead of trained models

### Performance Tips

1. **Use Base Models**: For Railway's free tier, the app will automatically use base models
2. **Optimize Dependencies**: Only essential packages in `requirements.txt`
3. **Health Checks**: The app includes `/api/health` endpoint for monitoring

## Cost Optimization

- **Free tier**: $5 credit/month (~500 hours)
- **Base models**: Lower memory usage
- **Auto-sleep**: Railway will sleep inactive services
- **Scale down**: Use minimal resources

## Next Steps

After deployment:
1. Test your app at the provided URL
2. Set up a custom domain (optional)
3. Monitor usage in Railway dashboard
4. Consider upgrading if you need more resources

## Support

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Community: [discord.gg/railway](https://discord.gg/railway)
- GitHub Issues: [github.com/railwayapp/cli](https://github.com/railwayapp/cli) 