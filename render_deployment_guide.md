# MercuryFX V2 - Render.com Deployment Guide

## 📋 Pre-Deployment Preparation

### 1. Create requirements.txt
Create this file in your project root:
```txt
email-validator==2.1.1
flask==3.0.3
gunicorn==23.0.0
numpy==1.26.4
pandas==2.2.2
python-dotenv==1.0.1
python-telegram-bot==21.4
requests==2.32.3
ta==0.11.0
yfinance==0.2.28
```

### 2. Create Procfile (optional but recommended)
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

### 3. Prepare Environment Variables
You'll need these ready:
- `TELEGRAM_TOKEN` - Your bot token from @BotFather
- `CHAT_ID` - Your Telegram chat/channel ID
- `SESSION_SECRET` - Random string for Flask sessions

## 🚀 Render.com Setup Process

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up/login with GitHub (recommended)
3. Connect your GitHub account

### Step 2: Upload Project to GitHub
1. Create new GitHub repository: `mercuryfx-v2`
2. Upload all your project files:
   - `main.py`
   - `trading_bot.py`
   - `technical_analysis.py`
   - `smart_money_concepts.py`
   - `risk_management.py`
   - `telegram_client.py`
   - `requirements.txt`
   - `templates/index.html`
   - `.env.example` (don't include actual .env)

### Step 3: Create Web Service in Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `mercuryfx-v2` repository

### Step 4: Configure Web Service Settings
```
Name: mercuryfx-v2
Region: Choose closest to you
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT main:app
```

### Step 5: Set Environment Variables
In Render dashboard, go to "Environment" tab and add:
```
TELEGRAM_TOKEN = your_telegram_bot_token_here
CHAT_ID = your_telegram_chat_id_here  
SESSION_SECRET = generate_random_string_here
```

### Step 6: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Wait for "Live" status (usually 2-5 minutes)

## 🔧 Important Render.com Configurations

### Python Version
Add `runtime.txt` file (optional):
```
python-3.11.7
```

### Health Check Endpoint
Your bot already has this configured:
- Health check URL: `https://your-app.onrender.com/`
- Status page: `https://your-app.onrender.com/status`

### Auto-Deploy Setup
- Enable "Auto-Deploy" in Render settings
- Every GitHub push will trigger new deployment

## 📊 Post-Deployment Steps

### 1. Verify Bot is Running
- Check Render logs for successful startup
- Visit your app URL to see "MercuryFX V2 Bot is alive!"
- Test Telegram connection by checking bot status

### 2. Configure Monitoring
- Render provides built-in monitoring
- Set up UptimeRobot for external monitoring (optional)
- Monitor logs in Render dashboard

### 3. Test Signal Generation
- Wait for market hours
- Monitor Telegram for signals
- Check logs for any errors

## 💡 Render.com Specific Notes

### Free Tier Limitations
- App sleeps after 30 minutes of inactivity
- 500 build hours/month
- 750 runtime hours/month
- Consider upgrading for 24/7 operation

### Keep-Alive Solutions (Free Tier)
1. **UptimeRobot**: Ping your app every 5 minutes
2. **External Monitor**: Set up simple HTTP requests
3. **Upgrade to Paid**: $7/month for always-on service

### File Storage
- Render uses ephemeral storage
- Log files (`mercuryfx.log`) will reset on redeploy
- Consider external logging service for persistent logs

## 🛠️ Troubleshooting

### Common Issues
1. **Build Failures**: Check requirements.txt syntax
2. **Import Errors**: Ensure all files are uploaded
3. **Environment Variables**: Double-check Telegram tokens
4. **Port Binding**: Use `$PORT` environment variable

### Debug Commands
Add to your logs if needed:
```python
import os
print(f"PORT: {os.environ.get('PORT', '5000')}")
print(f"Environment: {os.environ.get('RENDER', 'local')}")
```

## 📈 Performance Optimization

### For Production Use
1. Upgrade to paid plan ($7/month minimum)
2. Enable persistent disk if needed
3. Configure custom domain
4. Set up SSL (automatic on Render)
5. Monitor performance metrics

### Scaling Options
- Render auto-scales based on traffic
- Horizontal scaling available on higher plans
- Database integration available

## 🔐 Security Best Practices
- Never commit `.env` files to GitHub
- Use Render's environment variables
- Regularly rotate API tokens
- Monitor access logs
- Enable two-factor authentication on Render account

---

**Your MercuryFX V2 will be live at:** `https://your-app-name.onrender.com`

Total setup time: ~10-15 minutes after GitHub upload!