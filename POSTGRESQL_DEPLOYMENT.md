# PostgreSQL Cloud Deployment Guide

## Free PostgreSQL Hosting Options

Your HMS app now uses PostgreSQL, which has better free hosting options than MySQL:

### Option 1: **Neon** (Recommended - Free Forever)
- **Free Tier**: 10 GB storage, 3 GB RAM
- **URL**: [neon.tech](https://neon.tech)
- **Pros**: Generous free tier, serverless, auto-scaling
- **Setup**:
  1. Sign up at neon.tech
  2. Create a new project
  3. Copy the **Connection String** (DATABASE_URL)
  4. Use it in your environment variables

### Option 2: **Supabase** (PostgreSQL + More Features)
- **Free Tier**: 500 MB database, 2 GB bandwidth/month
- **URL**: [supabase.com](https://supabase.com)
- **Pros**: Includes auth, storage, realtime features
- **Setup**:
  1. Sign up at supabase.com
  2. Create a new project
  3. Go to Settings → Database
  4. Copy the **Connection String**

### Option 3: **ElephantSQL**
- **Free Tier**: 20 MB storage (tiny but works forsmall projects)
- **URL**: [elephantsql.com](https://elephantsql.com)
- **Pros**: Simple, easy setup

### Option 4: **Railway** (All-in-one)
- **Free Tier**: $5 free credit/month (usually enough for hobby projects)
- **URL**: [railway.app](https://railway.app)
- **Pros**: Deploy both database AND backend together

---

## Complete Deployment Steps

### Step 1: Setup PostgreSQL Database

#### Using Neon (Recommended):
1. Go to [neon.tech](https://neon.tech) and sign up
2. Click **"Create a project"**
3. Name your project: `HMS Database`
4. Copy the connection string that looks like:
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb
   ```

#### Initialize Database Schema:
Once you have your database:
1. Connect using a PostgreSQL client or their web interface
2. Run the SQL script from `database/init.sql`

**OR use psql command line:**
```bash
psql YOUR_DATABASE_URL < database/init.sql
```

---

### Step 2: Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)** and sign in with GitHub

2. **Deploy from GitHub**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your HMS repository
   - Railway will detect it's a Python app

3. **Configure Environment Variables**:
   Click on your deployment → Variables → Add these:
   ```
   DATABASE_URL=<your-neon-connection-string>
   PORT=8000
   ```

4. **Configure Build Settings** (if needed):
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Get your backend URL**: Railway provides a URL like:
   ```
   https://hms-backend-production.up.railway.app
   ```

---

### Step 3: Deploy Frontend to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with GitHub**

3. **New app**:
   - Repository: Select your HMS repo
   - Branch: main
   - Main file path: `frontend/app.py`
   - App URL: Choose your custom URL (e.g., `hms-vignesh`)

4. **Add Secrets** (Advanced Settings → Secrets):
   ```toml
   API_BASE_URL = "https://your-backend-url.up.railway.app"
   ```
   ⚠️ **Important**: Replace with your actual Railway backend URL!

5. **Deploy!**

Your app will be live at: `https://hms-vignesh.streamlit.app`

---

## Alternative: Deploy Everything to Render

[Render](https://render.com) can host both PostgreSQL and your backend:

1. **Create PostgreSQL Database**:
   - New → PostgreSQL
   - Free tier available
   - Get the **Internal Database URL**

2. **Create Web Service for Backend**:
   - New → Web Service
   - Connect your GitHub repo
   - Settings:
     - Root Directory: `backend`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `DATABASE_URL`: (from step 1)
     - `PYTHON_VERSION`: `3.11`

3. **Deploy Frontend to Streamlit** (same as Step 3 above)

---

## Environment Variables Reference

### Backend (.env or Railway/Render):
```bash
# Option 1: Single URL (recommended for cloud)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Option 2: Separate values (for local dev)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=hotel_management
```

### Frontend (Streamlit Secrets):
```toml
API_BASE_URL = "https://your-backend-url.com"
```

---

## Testing Your Deployment

1. **Test Backend**:
   ```bash
   curl https://your-backend-url.com/
   # Should return: {"message": "Hotel Management System API"}
   
   curl https://your-backend-url.com/rooms
   # Should return list of rooms
   ```

2. **Test Frontend**:
   - Visit your Streamlit URL
   - Check Dashboard loads
   - Try adding a guest or viewing rooms
   - If you see connection errors, check your `API_BASE_URL` secret

---

## Local Development with PostgreSQL

### Install PostgreSQL:
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/)
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt install postgresql`

### Setup Local Database:
```bash
# Start PostgreSQL
# Windows: PostgreSQL service should start automatically
# Mac/Linux: brew services start postgresql  OR  sudo service postgresql start

# Create database and run schema
psql -U postgres
CREATE DATABASE hotel_management;
\q

# Run init script
psql -U postgres -d hotel_management -f database/init.sql
```

### Run Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# Backend will run on http://localhost:8000
```

### Run Frontend:
```bash
cd frontend
streamlit run app.py
# Frontend will run on http://localhost:8501
```

---

## Troubleshooting

### "Connection refused" errors:
- Backend is not running or URL is wrong
- Check API_BASE_URL in Streamlit secrets
- Verify backend is deployed and accessible

### "Database connection failed":
- Check DATABASE_URL is correct
- Verify database is running
- Check firewall/network settings

### "relation does not exist" errors:
- Database schema not initialized
- Run init.sql on your database

### Backend deployment fails:
- Check requirements.txt exists in backend/
- Verify Python version compatibility
- Check build logs for errors

---

## Cost Summary

**100% Free Setup**:
- ✅ Neon: Free PostgreSQL (10 GB)
- ✅ Streamlit Cloud: Free frontend hosting
- ✅ Railway: Free with $5/month credit (usually enough)

**Total Cost**: $0/month for hobby projects! 🎉

---

## Security Notes

1. **Never commit `.env` file** (already in .gitignore)
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (automatic on Streamlit/Railway)
4. **Rotate database passwords** periodically
5. **Limit database access** to specific IPs if possible

---

## Next Steps

1. Push your updated code to GitHub
2. Follow Step 1-3 above to deploy
3. Share your Streamlit URL with anyone!
4. Your app will have a permanent URL that works from anywhere

Need help? Check the error logs in Railway/Streamlit dashboard.
