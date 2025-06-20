# YouTube API Production Deployment Guide

## Quick Start

### 1. Configure Credentials
Edit `config.py` and set your Gmail credentials:
```python
YOUTUBE_EMAIL = "your-email@gmail.com"
YOUTUBE_PASSWORD = "your-app-password"
```

### 2. Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku config:set YOUTUBE_EMAIL="your-email@gmail.com"
heroku config:set YOUTUBE_PASSWORD="your-app-password"
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### 3. Deploy to VPS/Contabo
```bash
# Upload files to server
scp -r . user@your-server:/path/to/app

# On server
cd /path/to/app
pip install -r requirements.txt
export YOUTUBE_EMAIL="your-email@gmail.com"
export YOUTUBE_PASSWORD="your-app-password"

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 2 main:app

# Or run with supervisor for auto-restart
```

### 4. Deploy with Docker
```bash
# Set environment variables
export YOUTUBE_EMAIL="your-email@gmail.com"
export YOUTUBE_PASSWORD="your-app-password"

# Start with docker-compose
docker-compose up -d
```

### 5. Deploy to Replit
1. Upload all files to Replit
2. Set secrets in Replit:
   - YOUTUBE_EMAIL: your-email@gmail.com
   - YOUTUBE_PASSWORD: your-app-password
3. Run the project

## Environment Variables

Required:
- `YOUTUBE_EMAIL`: Your Gmail address
- `YOUTUBE_PASSWORD`: Your Gmail App Password

Optional:
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Server port (default: 5000)

## Features

✓ Automatic Gmail login and YouTube authentication
✓ 12-hour automatic cookie refresh
✓ yt-dlp compatible cookie format
✓ Production-ready error handling
✓ Comprehensive logging
✓ API key management
✓ Rate limiting
✓ Thumbnail support
✓ Multiple deployment options

## API Usage

```bash
# Get video/audio stream
curl "http://your-domain.com/youtube?query=test&api_key=your-key"

# Get video stream
curl "http://your-domain.com/youtube?query=test&video=true&api_key=your-key"
```

## Monitoring

- Check logs: `tail -f logs/youtube_auth.log`
- API status: `GET /api/admin/auth/status`
- Health check: `GET /health`

## Support

This is a production-ready system that handles:
- Authentication failures
- Cookie expiration
- IP blocks
- Rate limiting
- Error recovery

Set it up once and it runs forever!
