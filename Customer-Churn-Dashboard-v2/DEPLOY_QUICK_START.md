# 🚀 Quick Deploy Guide - 5 Minutes to Production

Choose your deployment platform and follow the steps.

---

## 🌐 Option 1: Streamlit Cloud (Easiest - 3 minutes)

### Prerequisites
- GitHub account (repository already pushed)
- Free Streamlit account

### Steps

1. **Visit Streamlit Cloud**
   ```
   https://streamlit.io/cloud
   ```

2. **Sign In with GitHub**
   - Click "Sign up"
   - Authorize with GitHub
   - Complete signup

3. **Deploy App**
   - Click "New app"
   - Select your repository: `Customer-Churn-Dashboard-v2`
   - Branch: `master`
   - File path: `streamlit_app.py`
   - Click "Deploy"

4. **Wait** (2-3 minutes)
   - App builds and deploys
   - You'll get a public URL

5. **Share**
   - Share URL with team
   - App is live! 🎉

### Custom Domain (Optional)
- Go to App Settings
- Configure custom domain
- Update DNS

---

## 🐳 Option 2: Docker (Local Testing - 5 minutes)

### Prerequisites
- Docker installed

### Steps

```bash
# 1. Build
docker build -t churn-dashboard:latest .

# 2. Run
docker run -p 8501:8501 churn-dashboard:latest

# 3. Open
# http://localhost:8501

# 4. Stop
# Press Ctrl+C
```

### Production Docker

```bash
# 1. Build
docker build -t churn-dashboard:v2.0 .

# 2. Run with persistence
docker run -d \
  -p 8501:8501 \
  -v models:/app/ml/models \
  -e STREAMLIT_SERVER_HEADLESS=true \
  --restart unless-stopped \
  --name churn-dashboard \
  churn-dashboard:v2.0

# 3. Check status
docker ps

# 4. View logs
docker logs -f churn-dashboard
```

---

## ☁️ Option 3: AWS (5 minutes)

### Prerequisites
- AWS account
- Docker installed locally

### Steps

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name churn-dashboard
   ```

2. **Build and Push**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     123456789.dkr.ecr.us-east-1.amazonaws.com
   
   # Build
   docker build -t churn-dashboard .
   
   # Tag
   docker tag churn-dashboard:latest \
     123456789.dkr.ecr.us-east-1.amazonaws.com/churn-dashboard:latest
   
   # Push
   docker push \
     123456789.dkr.ecr.us-east-1.amazonaws.com/churn-dashboard:latest
   ```

3. **Deploy with App Runner**
   - Open AWS Console
   - Go to App Runner
   - Create Service
   - Select ECR image URL
   - Port: 8501
   - Deploy

4. **Done**
   - App Runner gives you a URL
   - Live in production! 🎉

---

## 🎯 Option 4: Heroku (5 minutes)

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

```bash
# 1. Login
heroku login

# 2. Create app
heroku create churn-dashboard-app

# 3. Set buildpack
heroku buildpacks:set heroku/python

# 4. Deploy
git push heroku master

# 5. Open
heroku open

# 6. View logs
heroku logs --tail
```

---

## 💻 Option 5: Self-Hosted Linux (5 minutes)

### Prerequisites
- Linux server (Ubuntu/Debian)
- SSH access

### Steps

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Install Python
sudo apt update
sudo apt install python3.11 python3-pip

# 3. Clone repo
git clone https://github.com/your-username/Customer-Churn-Dashboard.git
cd Customer-Churn-Dashboard-v2

# 4. Setup
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run
streamlit run app_premium_saas.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
```

### Optional: Auto-start on reboot

```bash
# Create service
sudo nano /etc/systemd/system/churn-dashboard.service
```

Paste:
```ini
[Unit]
Description=Customer Churn Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Customer-Churn-Dashboard-v2
ExecStart=/home/ubuntu/Customer-Churn-Dashboard-v2/venv/bin/streamlit run app_premium_saas.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable churn-dashboard
sudo systemctl start churn-dashboard
```

---

## 📊 Quick Comparison

| Platform | Difficulty | Cost | Setup Time | Best For |
|----------|-----------|------|-----------|----------|
| **Streamlit Cloud** | ⭐ Very Easy | Free | 3 min | Quick demos, small teams |
| **Docker** | ⭐⭐ Easy | Varies | 5 min | Full control, any server |
| **AWS App Runner** | ⭐⭐ Easy | ~$5-10/mo | 5 min | Enterprise, scaling |
| **Heroku** | ⭐⭐ Easy | ~$7+/mo | 5 min | Simple hosting |
| **Self-Hosted** | ⭐⭐⭐ Medium | Variable | 10 min | Maximum control |

---

## ✅ What's Included for Deployment

✅ `.streamlit/config.toml` - Streamlit configuration  
✅ `Dockerfile` - Docker container image  
✅ `docker-compose.yml` - Docker Compose setup  
✅ `Procfile` - Heroku configuration  
✅ `streamlit_app.py` - Streamlit Cloud entry point  
✅ `.gitignore` - Proper git ignore rules  
✅ `DEPLOYMENT.md` - Full deployment guide  

All files are production-ready!

---

## 🆘 Common Issues

### "Port already in use"
```bash
# On different port
streamlit run app_premium_saas.py --server.port=8502
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "App crashes on startup"
```bash
# Check logs
streamlit run app_premium_saas.py --logger.level=debug
```

### "Out of memory"
```bash
# Docker: Increase memory
docker run -m 2g churn-dashboard:latest

# Or reduce model size in config
```

---

## 🎯 Recommended Path

1. **Start**: Streamlit Cloud (fastest)
2. **Test**: Docker locally
3. **Scale**: AWS App Runner or self-hosted

---

## 📞 Need Help?

1. Read `DEPLOYMENT.md` for detailed options
2. Check app logs for errors
3. Verify `.streamlit/config.toml` settings
4. Ensure `requirements.txt` is up to date

---

## 🎉 You're Ready!

Pick your platform and deploy in 5 minutes or less! 🚀

**Start with:** [Streamlit Cloud](#-option-1-streamlit-cloud-easiest---3-minutes)

**Questions?** See `DEPLOYMENT.md` for complete guide.
