#!/usr/bin/env python3
"""
Production Configuration for YouTube Authentication System
Set your credentials here - the system will handle everything else automatically
"""

# YouTube Authentication Credentials
# Use Gmail App Password for maximum security (recommended)
YOUTUBE_EMAIL = "pm5763468@gmail.com"
YOUTUBE_PASSWORD = "Pubjmobilemerehe13nhi"  # Use App Password for production

# Cookie Management Settings
COOKIE_REFRESH_INTERVAL = 12 * 60 * 60  # 12 hours in seconds
COOKIE_FILE_PATH = "cookies.json"  # yt-dlp compatible format
BACKUP_COOKIE_PATH = "cookies_backup.json"

# Anti-Detection Settings
USE_PROXY_ROTATION = False  # Set to True if you have proxies
PROXY_LIST = [
    # Add proxies in format: "ip:port:username:password" or "ip:port"
    # "1.2.3.4:8080:user:pass",
    # "5.6.7.8:3128",
]

# Browser Automation Settings
HEADLESS_MODE = True  # Run browser in background (no visible window)
MAX_LOGIN_RETRIES = 5  # How many times to retry login on failure
RETRY_DELAY = 30  # Seconds to wait between retries

# Daemon/Service Settings
RUN_AS_DAEMON = True  # Keep running forever in background
LOG_FILE = "youtube_auth.log"  # Log file for monitoring
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Safety and Error Recovery
AUTO_RECOVERY = True  # Automatically recover from errors
IP_BAN_DETECTION = True  # Detect and handle IP bans
CAPTCHA_DETECTION = True  # Detect and handle CAPTCHAs
TWO_FA_BACKUP = True  # Handle 2FA automatically

# Performance Settings
CONCURRENT_SESSIONS = 1  # Number of parallel authentication sessions
SESSION_POOL_SIZE = 3  # Keep multiple sessions ready
HEALTH_CHECK_INTERVAL = 300  # Check system health every 5 minutes

# Database/Storage Settings
USE_ENCRYPTED_STORAGE = True  # Encrypt stored cookies
COOKIE_BACKUP_COUNT = 5  # Keep 5 backup copies of cookies
AUTO_CLEANUP_DAYS = 30  # Auto-delete old logs after 30 days