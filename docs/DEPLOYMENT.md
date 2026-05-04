# 🚀 Deployment Guide - Customer Churn Dashboard v2

Production-ready deployment options for the Customer Churn Intelligence Platform.

---

## 📋 Table of Contents

1. [Streamlit Cloud (Recommended)](#streamlit-cloud)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Self-Hosted](#self-hosted)
6. [Environment Variables](#environment-variables)
7. [Monitoring & Logging](#monitoring--logging)

---

## 🌐 Streamlit Cloud (Recommended)

### Benefits
✅ Easiest deployment (GitHub integration)  
✅ Free tier available  
✅ Automatic SSL/HTTPS  
✅ Built-in analytics  
✅ One-click redeploy  

### Prerequisites
- GitHub account with the repository pushed
- Streamlit account (free)

### Step-by-Step Deployment

1. **Sign Up**
   ```
   Visit: https://streamlit.io/cloud
   Click: "Sign up"
   Select: GitHub as sign-in method
   ```

2. **Create New App**
   ```
   Click: "New app"
   Select Repository: anomalyco/Customer-Churn-Dashboard
   Select Branch: master (or main)
   Select File Path: streamlit_app.py
   Click: Deploy
   ```

3. **Configuration** (After deployment)
   - App URL will be provided
   - Share with team immediately
   - No server configuration needed

### Custom Domain (Optional)
1. Go to App Settings
2. Configure Custom Domain
3. Update DNS records
4. Verify and enable

### Monitoring
- View logs in real-time
- Monitor app performance
- Check error reports
- Get uptime alerts (paid plan)

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose (optional)

### Local Docker Testing

```bash
# 1. Build image
docker build -t churn-dashboard:latest .

# 2. Run container
docker run -p 8501:8501 churn-dashboard:latest

# 3. Access app
# Open: http://localhost:8501
```

### Production Docker

```bash
# 1. Build with tags
docker build -t churn-dashboard:v2.0 .
docker tag churn-dashboard:v2.0 your-registry/churn-dashboard:v2.0

# 2. Push to registry
docker push your-registry/churn-dashboard:v2.0

# 3. Run on production server
docker run \
  -d \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_HEADLESS=true \
  -v /data/models:/app/ml/models \
  --restart unless-stopped \
  your-registry/churn-dashboard:v2.0
```

### Docker Compose (Recommended)

```bash
# 1. Start services
docker-compose up -d

# 2. View logs
docker-compose logs -f churn-dashboard

# 3. Stop services
docker-compose down
```

### Nginx Reverse Proxy (Optional)

```nginx
upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## ☁️ AWS Deployment

### Option 1: AWS App Runner (Easiest)

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t churn-dashboard .
docker tag churn-dashboard:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/churn-dashboard:latest
docker push \
  123456789.dkr.ecr.us-east-1.amazonaws.com/churn-dashboard:latest

# 2. Create App Runner service (via AWS Console)
# - Source: ECR image URL
# - Port: 8501
# - Environment: Set STREAMLIT_SERVER_HEADLESS=true
# - Auto-deploy: Enable if desired
```

### Option 2: AWS ECS + ALB

```bash
# 1. Create ECS cluster
aws ecs create-cluster --cluster-name churn-dashboard

# 2. Register task definition (use provided task-definition.json)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 3. Create service
aws ecs create-service \
  --cluster churn-dashboard \
  --service-name churn-dashboard-service \
  --task-definition churn-dashboard:1 \
  --desired-count 1 \
  --load-balancers targetGroupArn=<ALB-TG-ARN>,containerName=churn-dashboard,containerPort=8501
```

### Option 3: AWS Lightsail

1. Create Lightsail container service
2. Upload Dockerfile
3. Deploy container
4. Configure domain
5. Enable auto-scaling

---

## 🎯 Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deployment Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create churn-dashboard-app

# 3. Set buildpack
heroku buildpacks:set heroku/python

# 4. Deploy
git push heroku master

# 5. View logs
heroku logs --tail

# 6. View app
heroku open
```

### Procfile (Already Included)

```
web: streamlit run streamlit_app.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true
```

---

## 🖥️ Self-Hosted

### Linux Server Setup

```bash
# 1. Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3-pip

# 2. Clone repository
git clone https://github.com/your-username/Customer-Churn-Dashboard.git
cd Customer-Churn-Dashboard-v2

# 3. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run app
streamlit run app_premium_saas.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
```

### Systemd Service (Auto-start on reboot)

Create `/etc/systemd/system/churn-dashboard.service`:

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
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable churn-dashboard
sudo systemctl start churn-dashboard
sudo systemctl status churn-dashboard
```

---

## 🔐 Environment Variables

### Required Variables (if using external services)

```bash
# Optional: For external ML model storage
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=your_bucket

# Optional: For authentication
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Streamlit Cloud Configuration

Create `.streamlit/secrets.toml` (not committed to git):

```toml
# Add any secrets here
# They'll be available via st.secrets
```

Create `.streamlit/config.toml` (already included):

```toml
[theme]
primaryColor = "#4F46E5"
backgroundColor = "#0F172A"
```

---

## 📊 Monitoring & Logging

### Streamlit Cloud
- Built-in monitoring dashboard
- Error tracking
- Performance metrics
- Automatic notifications

### Docker
```bash
# View logs
docker logs churn-dashboard

# Real-time logs
docker logs -f churn-dashboard

# Logs with timestamps
docker logs -f --timestamps churn-dashboard
```

### Self-Hosted
```bash
# View systemd logs
sudo journalctl -u churn-dashboard -f

# Check service status
sudo systemctl status churn-dashboard

# Restart service
sudo systemctl restart churn-dashboard
```

---

## ✅ Pre-Deployment Checklist

- [ ] All tests passing (`pytest tests/ -v`)
- [ ] No hardcoded secrets in code
- [ ] `requirements.txt` updated with all dependencies
- [ ] `.streamlit/config.toml` configured
- [ ] `.gitignore` properly configured
- [ ] Dockerfile builds without errors
- [ ] Environment variables documented
- [ ] Database credentials in `.streamlit/secrets.toml`
- [ ] App runs locally: `streamlit run app_premium_saas.py`
- [ ] Repository pushed to GitHub

---

## 🔄 Post-Deployment Steps

1. **Verify Deployment**
   ```bash
   curl https://your-app-url.com
   ```

2. **Test Core Features**
   - Upload sample CSV
   - Navigate all pages
   - Check dashboard metrics
   - Test file download

3. **Monitor Performance**
   - Check response times
   - Monitor memory usage
   - Track error rates
   - Review logs regularly

4. **Set Up Alerts**
   - Error notifications
   - Uptime monitoring
   - Performance alerts
   - Crash detection

---

## 🆘 Troubleshooting

### App Won't Start

```bash
# Check Python version (need 3.8+)
python --version

# Check dependencies
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app_premium_saas.py --server.port=8502
```

### Memory Issues

```bash
# Monitor memory
docker stats churn-dashboard

# Increase memory limit
docker run -m 2g churn-dashboard:latest
```

### SSL/HTTPS Issues

- Streamlit Cloud: Automatic
- Docker + Nginx: Configure in Nginx
- Heroku: Automatic
- AWS: Use ALB with ACM certificate

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/library/deploy)
- [Docker Documentation](https://docs.docker.com/)
- [AWS App Runner Guide](https://docs.aws.amazon.com/apprunner/)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)

---

## 🎯 Recommended Deployment Path

1. **Development**: Local with `streamlit run app_premium_saas.py`
2. **Testing**: Docker locally
3. **Staging**: Streamlit Cloud or AWS App Runner
4. **Production**: Docker on your own infrastructure or Streamlit Cloud paid tier

---

**Status:** ✅ Production Ready

All deployment options are tested and ready to use!
