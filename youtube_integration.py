#!/usr/bin/env python3
"""
YouTube Integration Module
Integrates the production YouTube Authentication System with the existing Flask app
"""

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Optional
import subprocess
import sys

# Configure logging
logger = logging.getLogger(__name__)

class YouTubeIntegration:
    """Integration layer for production YouTube Authentication System"""
    
    def __init__(self):
        self.cookie_file = "cookies.json"
        self.daemon_process = None
        self.last_cookie_check = 0
        self.cookie_status = {'valid': False, 'last_update': None}
        
        # Check if config exists and start daemon
        self._check_configuration()
        self._start_auth_daemon()
    
    def _check_configuration(self):
        """Check if configuration file exists"""
        try:
            from config import YOUTUBE_EMAIL, YOUTUBE_PASSWORD
            if YOUTUBE_EMAIL and YOUTUBE_PASSWORD:
                logger.info("YouTube authentication configuration found")
                return True
        except ImportError:
            logger.warning("No config.py found - YouTube authentication disabled")
        except Exception as e:
            logger.warning(f"Configuration error: {e}")
        return False
    
    def _start_auth_daemon(self):
        """Start the YouTube authentication daemon in background"""
        try:
            # Check if daemon script exists
            daemon_script = Path("run_youtube_auth.py")
            if not daemon_script.exists():
                logger.warning("YouTube auth daemon script not found")
                return
            
            # Start daemon in background
            def run_daemon():
                try:
                    # Run the authentication system
                    subprocess.run([
                        sys.executable, "run_youtube_auth.py"
                    ], cwd=Path.cwd())
                except Exception as e:
                    logger.error(f"Daemon startup error: {e}")
            
            self.daemon_thread = threading.Thread(target=run_daemon, daemon=True)
            self.daemon_thread.start()
            logger.info("YouTube authentication daemon started in background")
            
        except Exception as e:
            logger.warning(f"Could not start auth daemon: {e}")
    
    def get_current_cookie_file(self) -> Optional[str]:
        """Get the current cookie file path"""
        # Check if cookie file exists and is recent
        if Path(self.cookie_file).exists():
            # Check file age
            file_age = time.time() - Path(self.cookie_file).stat().st_mtime
            if file_age < 24 * 60 * 60:  # Less than 24 hours old
                return self.cookie_file
        return None
    
    def update_ytdl_options(self, ytdl_options: dict) -> dict:
        """Update yt-dlp options with current cookies"""
        cookie_file = self.get_current_cookie_file()
        if cookie_file:
            ytdl_options['cookiefile'] = cookie_file
            logger.debug(f"Using cookie file: {cookie_file}")
        else:
            logger.warning("No valid cookie file available")
        
        return ytdl_options
    
    def get_session_status(self) -> dict:
        """Get status of authentication system"""
        try:
            # Check cookie file status
            cookie_exists = Path(self.cookie_file).exists()
            cookie_age = None
            cookie_size = 0
            
            if cookie_exists:
                stat = Path(self.cookie_file).stat()
                cookie_age = time.time() - stat.st_mtime
                cookie_size = stat.st_size
            
            # Try to get daemon status via API
            daemon_status = "unknown"
            try:
                import requests
                response = requests.get("http://127.0.0.1:8888/status", timeout=2)
                if response.status_code == 200:
                    daemon_data = response.json()
                    daemon_status = "running"
                else:
                    daemon_status = "error"
            except:
                daemon_status = "not_running"
            
            return {
                'cookie_file_exists': cookie_exists,
                'cookie_file_path': self.cookie_file,
                'cookie_age_seconds': cookie_age,
                'cookie_size_bytes': cookie_size,
                'daemon_status': daemon_status,
                'authentication_system': 'production_ready'
            }
            
        except Exception as e:
            logger.error(f"Error getting session status: {e}")
            return {'error': str(e)}

# Global instance
youtube_integration = YouTubeIntegration()

def get_youtube_integration() -> YouTubeIntegration:
    """Get the global YouTube integration instance"""
    return youtube_integration

def clean_ytdl_options_with_auth():
    """Get production-ready yt-dlp options with authentication"""
    options = {
        'format': 'best[height<=1080]/best',
        'quiet': True,
        'no_warnings': True,
        'extractaudio': False,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'ignoreerrors': True,
        'no_check_certificate': True,
        'prefer_insecure': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.youtube.com/',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        },
        'http_chunk_size': 10485760,  # 10MB chunks
        'retries': 5,
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
        'keep_fragments': False,
        'buffersize': 32768,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
        # Advanced options for bot detection bypass
        'extractor_retries': 5,
        'socket_timeout': 30,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
    }
    
    # Add authentication cookies from production system
    integration = get_youtube_integration()
    options = integration.update_ytdl_options(options)
    
    return options