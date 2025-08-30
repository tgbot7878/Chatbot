# Gemini AI Assistant Telegram Bot

A Telegram bot powered by Google's Gemini AI model.

## Setup Instructions

1. Clone this repository
2. Create a new bot using [BotFather](https://t.me/BotFather) on Telegram and get the API token
3. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. Deploy to Render.com

## Environment Variables

Set these environment variables in Render.com:

- `TELEGRAM_TOKEN`: Your Telegram bot token from BotFather
- `GEMINI_API_KEY`: Your Google Gemini API key
- `WEBHOOK_URL`: The URL of your deployed application (e.g., https://your-app-name.onrender.com)

## Deploy to Render.com

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `./start.sh`
5. Add the required environment variables
