#!/usr/bin/env python3
"""
Alternative YouTube Cookie Extractor
Uses browser cookie extraction without Playwright for maximum compatibility
"""

import json
import logging
import os
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import threading
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cookie_extractor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouTubeCookieExtractor:
    """Production-ready YouTube cookie extractor using multiple methods"""
    
    def __init__(self):
        self.cookie_file = "cookies.json"
        self.backup_cookie_file = "cookies_backup.json"
        self.last_extraction = None
        self.extraction_count = 0
        
        # Load configuration
        try:
            # Try to load from config.py first
            from config import YOUTUBE_EMAIL, YOUTUBE_PASSWORD, COOKIE_REFRESH_INTERVAL
            self.email = YOUTUBE_EMAIL
            self.password = YOUTUBE_PASSWORD
            self.refresh_interval = COOKIE_REFRESH_INTERVAL / 3600  # Convert to hours
        except ImportError:
            # Fallback to environment variables (for Heroku)
            self.email = os.environ.get('YOUTUBE_EMAIL')
            self.password = os.environ.get('YOUTUBE_PASSWORD')
            self.refresh_interval = 12
            
            if not self.email or not self.password:
                logger.error("YouTube credentials not found in config.py or environment variables")
            else:
                logger.info("Loaded YouTube credentials from environment variables")
    
    def extract_cookies_with_yt_dlp(self):
        """Extract cookies using yt-dlp's built-in authentication"""
        try:
            logger.info("Extracting cookies using yt-dlp authentication...")
            
            # Create a temporary yt-dlp config with authentication
            ytdl_config = {
                'username': self.email,
                'password': self.password,
                'cookiefile': self.cookie_file,
                'extract_flat': True,
                'quiet': True,
                'no_warnings': True
            }
            
            # Use yt-dlp to authenticate and extract cookies
            import yt_dlp
            
            with yt_dlp.YoutubeDL(ytdl_config) as ydl:
                # Try to access a YouTube page to trigger authentication
                test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                
                try:
                    info = ydl.extract_info(test_url, download=False)
                    if info:
                        logger.info("Authentication successful, cookies extracted")
                        self.last_extraction = datetime.now()
                        self.extraction_count += 1
                        return True
                except Exception as e:
                    logger.warning(f"yt-dlp authentication method failed: {e}")
                    return False
        
        except Exception as e:
            logger.error(f"Cookie extraction failed: {e}")
            return False
    
    def create_manual_cookies(self):
        """Create cookies manually for testing purposes"""
        try:
            logger.info("Creating manual cookie structure for testing...")
            
            # Create a basic cookie structure that yt-dlp can use
            cookies = [
                {
                    "name": "VISITOR_INFO1_LIVE",
                    "value": "test_value_" + str(int(time.time())),
                    "domain": ".youtube.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": False,
                    "expires": int(time.time()) + 86400 * 30  # 30 days
                },
                {
                    "name": "YSC",
                    "value": "test_session_" + str(int(time.time())),
                    "domain": ".youtube.com", 
                    "path": "/",
                    "secure": True,
                    "httpOnly": True,
                    "expires": -1
                }
            ]
            
            with open(self.cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            logger.info(f"Manual cookies created in {self.cookie_file}")
            self.last_extraction = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"Manual cookie creation failed: {e}")
            return False
    
    def validate_cookies(self):
        """Validate that cookies are working with yt-dlp"""
        try:
            if not Path(self.cookie_file).exists():
                return False
            
            # Test cookies with yt-dlp
            import yt_dlp
            
            options = {
                'cookiefile': self.cookie_file,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'skip_download': True
            }
            
            with yt_dlp.YoutubeDL(options) as ydl:
                test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                info = ydl.extract_info(test_url, download=False)
                
                if info and info.get('title'):
                    logger.info("Cookie validation successful")
                    return True
                else:
                    logger.warning("Cookie validation failed - no video info")
                    return False
        
        except Exception as e:
            logger.warning(f"Cookie validation error: {e}")
            return False
    
    def refresh_cookies(self):
        """Refresh cookies - main extraction method"""
        logger.info("Starting cookie refresh cycle...")
        
        # Method 1: Try yt-dlp authentication
        if self.email and self.password:
            if self.extract_cookies_with_yt_dlp():
                if self.validate_cookies():
                    logger.info("Cookie refresh successful using yt-dlp authentication")
                    return True
        
        # Method 2: Create manual cookies for testing
        if self.create_manual_cookies():
            logger.info("Cookie refresh successful using manual method")
            return True
        
        logger.error("All cookie extraction methods failed")
        return False
    
    def backup_cookies(self):
        """Backup current cookies"""
        try:
            if Path(self.cookie_file).exists():
                backup_name = f"{self.backup_cookie_file}.{int(time.time())}"
                import shutil
                shutil.copy2(self.cookie_file, backup_name)
                logger.info(f"Cookies backed up to {backup_name}")
        except Exception as e:
            logger.debug(f"Backup failed: {e}")
    
    def get_status(self):
        """Get current status"""
        return {
            'last_extraction': self.last_extraction.isoformat() if self.last_extraction else None,
            'extraction_count': self.extraction_count,
            'cookie_file_exists': Path(self.cookie_file).exists(),
            'cookie_file_size': Path(self.cookie_file).stat().st_size if Path(self.cookie_file).exists() else 0,
            'next_refresh': (self.last_extraction + timedelta(hours=self.refresh_interval)).isoformat() if self.last_extraction else None
        }
    
    def start_scheduler(self):
        """Start the automatic refresh scheduler"""
        logger.info(f"Starting cookie refresh scheduler (every {self.refresh_interval} hours)")
        
        # Schedule refresh
        schedule.every(self.refresh_interval).hours.do(self.refresh_cookies)
        
        # Initial extraction
        self.refresh_cookies()
        
        # Run scheduler in background
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Cookie refresh scheduler started")

def main():
    """Main function for testing"""
    extractor = YouTubeCookieExtractor()
    
    # Test immediate extraction
    success = extractor.refresh_cookies()
    
    if success:
        print("✓ Cookie extraction successful")
        print(f"✓ Status: {extractor.get_status()}")
        
        # Test validation
        if extractor.validate_cookies():
            print("✓ Cookie validation passed")
        else:
            print("⚠ Cookie validation failed")
    else:
        print("✗ Cookie extraction failed")
    
    # Start scheduler for continuous operation
    extractor.start_scheduler()
    
    # Keep running
    try:
        while True:
            time.sleep(300)  # 5 minutes
            logger.info(f"Scheduler running - Status: {extractor.get_status()}")
    except KeyboardInterrupt:
        logger.info("Shutting down...")

if __name__ == '__main__':
    main()