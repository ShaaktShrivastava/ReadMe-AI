# 🚀 Deployment Guide - ReadMeAI on Streamlit Cloud

## Quick Deploy (5 minutes)

### Step 1: Go to Streamlit Cloud
Visit: https://share.streamlit.io/

### Step 2: Sign In
- Click "Sign in with GitHub"
- Authorize Streamlit to access your repositories

### Step 3: Deploy New App
1. Click "New app" button
2. Fill in the form:
   - **Repository**: `ShaaktShrivastava/ReadMe-AI`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom name like `readme-ai-yourname`

### Step 4: Add Secrets (IMPORTANT!)
1. Click "Advanced settings" before deploying
2. In the "Secrets" section, add:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```
3. Replace with your actual Mistral API key

### Step 5: Deploy!
- Click "Deploy!"
- Wait 2-3 minutes for the app to build and start
- Your app will be live at: `https://your-app-name.streamlit.app`

---

## Alternative: Deploy After Creation

If you already deployed without secrets:

1. Go to your app dashboard
2. Click the menu (⋮) → "Settings"
3. Go to "Secrets" tab
4. Add your secrets:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```
5. Click "Save"
6. App will automatically restart with secrets

---

## Files Included for Deployment

✅ `requirements.txt` - Python dependencies
✅ `.streamlit/config.toml` - Streamlit configuration
✅ `.streamlit/secrets.toml` - Local secrets template (not pushed to GitHub)
✅ `packages.txt` - System dependencies
✅ `.gitignore` - Prevents secrets from being committed

---

## Troubleshooting

### App won't start?
- Check that all dependencies are in `requirements.txt`
- Verify your MISTRAL_API_KEY is correct in Streamlit Cloud secrets
- Check the app logs in Streamlit Cloud dashboard

### Chroma DB issues?
- ChromaDB will create its database in the cloud environment
- First upload might take longer as it creates the vector database

### API rate limits?
- Free Mistral API has rate limits
- Consider upgrading your Mistral API plan for production use

---

## Your Live App Will Be At:
🌐 `https://readme-ai-shaaktshrivastava.streamlit.app`
(or whatever name you choose)

---

## Need Help?
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- Mistral API: https://docs.mistral.ai/

Happy Deploying! 🎉
