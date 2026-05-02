"""
🏆 Customer Churn Intelligence Platform - Streamlit Cloud Entry Point

This is the main entry point for Streamlit Cloud deployment.
Use this file when deploying to Streamlit Cloud.

For local development:
- Use: streamlit run app_premium_saas.py
- Or: streamlit run app_improved.py

For Docker/Self-hosted:
- See Dockerfile and docker-compose.yml
"""

# Import and run the premium SaaS app
from app_premium_saas import main_premium

if __name__ == "__main__":
    main_premium()
