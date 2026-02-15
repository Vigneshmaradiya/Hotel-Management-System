# Backend Deployment Guide

## Overview
Your backend needs to be deployed to a cloud service so Streamlit Cloud can access it via a public URL.

---

## ✅ Recommended: Railway (Easiest & Free)

### Why Railway?
- ✅ Free tier (500 hours/month, $5 credit)
- ✅ Auto-deploys from GitHub
- ✅ Built-in PostgreSQL support
- ✅ Simple configuration
- ✅ Automatic HTTPS

### Steps:

1. **Sign up at [Railway.app](https://railway.app)** using your GitHub account

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Vigneshmaradiya/Hotel-Management-System`
   - Click "Deploy Now"

3. **Configure Backend Service**:
   - Railway auto-detects the Dockerfile
   - Set Root Directory: `backend`
   - Go to Variables tab and add:
     ```
     DATABASE_URL=postgresql://postgres.bvzqxyswqpjdwetjqobx:hms_krishna_maradiya@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
     ```
   - Click "Generate Domain" to get your public URL

4. **Copy the Railway URL** (e.g., `https://your-app.up.railway.app`)

5. **Update Streamlit Cloud**:
   - Go to your Streamlit app settings
   - Add Secret:
     ```toml
     API_BASE_URL = "https://your-app.up.railway.app"
     ```
   - Restart the app

**Done!** Your backend is now permanently accessible.

---

## Alternative 1: Render (Also Free & Easy)

### Steps:

1. Go to [Render.com](https://render.com) and sign up with GitHub

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Name: `hms-backend`
     - Root Directory: `backend`
     - Runtime: `Docker`
     - Instance Type: `Free`

3. **Add Environment Variable**:
   ```
   DATABASE_URL=postgresql://postgres.bvzqxyswqpjdwetjqobx:hms_krishna_maradiya@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
   ```

4. Click "Create Web Service"

5. Copy the URL (e.g., `https://hms-backend.onrender.com`)

6. Update Streamlit secrets with this URL

**Note:** Render free tier spins down after 15 min of inactivity. First request may be slow.

---

## Alternative 2: Fly.io (Free with More Resources)

### Steps:

1. Install Fly CLI:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. Login and deploy:
   ```bash
   fly auth login
   cd backend
   fly launch --name hms-backend
   ```

3. Set secrets:
   ```bash
   fly secrets set DATABASE_URL="postgresql://postgres.bvzqxyswqpjdwetjqobx:hms_krishna_maradiya@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
   ```

4. Deploy:
   ```bash
   fly deploy
   ```

5. Get your URL:
   ```bash
   fly info
   ```

---

## Local Docker Testing

Before deploying, test locally:

```bash
# Build and run with docker-compose
docker-compose up --build

# Test the API
curl http://localhost:8000/rooms
```

Or build manually:
```bash
cd backend
docker build -t hms-backend .
docker run -p 8000:8000 --env-file ../.env hms-backend
```

---

## Update Streamlit Cloud Configuration

Once your backend is deployed:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your HMS app
3. Click ⋮ → "Settings"
4. Go to "Secrets"
5. Add:
   ```toml
   API_BASE_URL = "https://your-backend-url.com"
   ```
6. Save and reboot app

---

## Comparison Table

| Service | Free Tier | Auto-sleep | Deploy Time | Difficulty |
|---------|-----------|------------|-------------|------------|
| **Railway** | 500 hrs/mo | No | ~2 min | ⭐ Easiest |
| **Render** | Unlimited* | Yes (15min) | ~5 min | ⭐⭐ Easy |
| **Fly.io** | 3 VMs | No | ~3 min | ⭐⭐⭐ Medium |

*Render: 750 hours/month, but sleeps after inactivity

---

## Troubleshooting

### Backend won't connect to Supabase
- Verify DATABASE_URL is correct in environment variables
- Check Supabase allows connections from your cloud provider's IPs
- Try using Session mode pooler instead of Transaction mode

### Streamlit can't reach backend
- Verify the backend URL is accessible: `curl https://your-backend-url.com`
- Check API_BASE_URL in Streamlit secrets matches exactly
- Ensure no trailing slash in the URL

### Railway/Render deployment fails
- Check build logs for errors
- Verify Dockerfile is correct
- Ensure requirements.txt has all dependencies

---

## Cost Estimates

All options have generous free tiers:
- **Development/Testing**: Completely FREE
- **Production**: 
  - Railway: $5/month after free tier
  - Render: $7/month for always-on
  - Fly.io: $0-$5/month depending on usage

**Recommendation**: Start with Railway's free tier. It's the easiest and most reliable for your use case.
