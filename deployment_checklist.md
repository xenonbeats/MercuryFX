# 🚀 Render.com Deployment Checklist for MercuryFX V2

## ✅ Pre-Upload Checklist
- [ ] Create `requirements.txt` with exact versions
- [ ] Verify all Python files are ready
- [ ] Have Telegram bot token ready
- [ ] Have Telegram chat ID ready
- [ ] Create GitHub repository

## ✅ File Upload Checklist
Upload these files to GitHub:
- [ ] `main.py` - Flask server entry point
- [ ] `trading_bot.py` - Core trading logic  
- [ ] `technical_analysis.py` - Technical indicators
- [ ] `smart_money_concepts.py` - SMC analysis
- [ ] `risk_management.py` - Risk management system
- [ ] `telegram_client.py` - Telegram integration
- [ ] `requirements.txt` - Dependencies list
- [ ] `templates/index.html` - Web interface
- [ ] `README.md` (optional) - Project description

## ✅ Render.com Setup Steps
1. [ ] Create Render account
2. [ ] Connect GitHub repository
3. [ ] Create new Web Service
4. [ ] Configure build settings:
   - [ ] Runtime: Python 3
   - [ ] Build Command: `pip install -r requirements.txt`
   - [ ] Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`
5. [ ] Set environment variables:
   - [ ] `TELEGRAM_TOKEN`
   - [ ] `CHAT_ID`
   - [ ] `SESSION_SECRET`
6. [ ] Deploy and wait for "Live" status

## ✅ Post-Deployment Verification
- [ ] Visit app URL - should show "MercuryFX V2 Bot is alive!"
- [ ] Check `/status` page works
- [ ] Verify bot starts in Render logs
- [ ] Test Telegram connection
- [ ] Monitor for first trading signal
- [ ] Set up external monitoring (UptimeRobot)

## 🔧 Quick Setup Commands

### Create requirements.txt:
```txt
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

### Render Build Settings:
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT main:app
```

### Environment Variables:
```
TELEGRAM_TOKEN=your_bot_token_from_botfather
CHAT_ID=your_telegram_chat_id
SESSION_SECRET=random_string_for_flask_sessions
```

## 💡 Important Notes

- **Free Tier**: App sleeps after 30 minutes of inactivity
- **Always-On**: Upgrade to $7/month for 24/7 operation
- **Logs**: Check Render dashboard for startup logs
- **Updates**: Auto-deploy on GitHub pushes (if enabled)

## 🚨 Common Issues & Solutions

**Build Fails**: Check requirements.txt syntax
**Bot Won't Start**: Verify environment variables are set
**No Signals**: Wait for market hours and check logs
**App Sleeps**: Use UptimeRobot pings every 5 minutes

---

**Expected Result**: Your MercuryFX V2 bot running 24/7 at `https://your-app.onrender.com`