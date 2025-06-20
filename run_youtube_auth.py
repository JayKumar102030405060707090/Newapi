
#!/usr/bin/env python3
"""
YouTube Authentication Daemon
Runs the cookie extraction system continuously in the background
"""

import time
import logging
import os
from youtube_cookie_extractor import YouTubeCookieExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main daemon function"""
    logger.info("Starting YouTube authentication daemon...")
    
    try:
        # Initialize the cookie extractor
        extractor = YouTubeCookieExtractor()
        
        # Start the scheduler
        extractor.start_scheduler()
        
        logger.info("YouTube authentication daemon started successfully")
        
        # Keep the daemon running
        while True:
            time.sleep(60)  # Check every minute
            logger.debug("Daemon running...")
            
    except KeyboardInterrupt:
        logger.info("Daemon shutdown requested")
    except Exception as e:
        logger.error(f"Daemon error: {e}")
        raise

if __name__ == '__main__':
    main()
