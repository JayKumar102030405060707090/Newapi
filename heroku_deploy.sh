
#!/bin/bash
# Heroku deployment script

echo "Deploying YouTube API to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Error: Heroku CLI not installed. Please install it first."
    exit 1
fi

# Set environment variables (replace with your actual credentials)
echo "Setting environment variables..."
heroku config:set YOUTUBE_EMAIL="pm5763468@gmail.com"
heroku config:set YOUTUBE_PASSWORD="Pubjmobilemerehe13nhi"
heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
heroku config:set FLASK_ENV="production"

# Scale the worker process
echo "Scaling worker process..."
heroku ps:scale worker=1

# Deploy the application
echo "Deploying to Heroku..."
git add .
git commit -m "Deploy YouTube API with authentication fixes"
git push heroku main

# Check deployment status
echo "Checking deployment status..."
heroku ps

echo "Deployment complete! Your app should be available at:"
heroku info -s | grep web_url | cut -d= -f2
