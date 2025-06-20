
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 main:app
worker: python youtube_cookie_extractor.py
