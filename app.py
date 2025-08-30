import os
import logging
from flask import Flask, request
import telegram
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import google.generativeai as genai

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Get environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash-lite')

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user_name = update.effective_user.first_name
    welcome_message = f"""
👋 Hello {user_name}! I'm your AI assistant powered by Gemini.

I can help you with:
- Answering questions
- Generating creative content
- Translating languages
- And much more!

Just send me a message and I'll respond!
"""
    update.message.reply_text(welcome_message)

def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    help_text = """
🤖 Gemini AI Assistant Bot Help

Available commands:
/start - Start the bot
/help - Show this help message
/about - Information about this bot

Just send me any message and I'll respond using Gemini AI!
"""
    update.message.reply_text(help_text)

def about(update: Update, context: CallbackContext):
    """Send information about the bot."""
    about_text = """
ℹ️ About This Bot

This is an AI assistant powered by Google's Gemini model (gemini-2.5-flash-lite).

Developed using:
- Python
- python-telegram-bot library
- Google Generative AI API

Deployed on Render.com
"""
    update.message.reply_text(about_text)

def echo(update: Update, context: CallbackContext):
    """Process user message and generate response using Gemini."""
    user_message = update.message.text
    
    # Show typing action
    update.message.chat.send_action(action=telegram.ChatAction.TYPING)
    
    try:
        # Generate response using Gemini
        response = model.generate_content(user_message)
        bot_response = response.text
        
        # Send the response
        update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        update.message.reply_text("Sorry, I encountered an error while processing your request. Please try again later.")

# Set up dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("about", about))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route('/')
def index():
    return 'Gemini AI Assistant Telegram Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    """Set webhook endpoint for Telegram."""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"

def set_webhook():
    """Set webhook for Telegram bot."""
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        result = bot.set_webhook(webhook_url)
        if result:
            logger.info(f"Webhook set to: {webhook_url}")
        else:
            logger.error("Failed to set webhook")
    else:
        logger.warning("WEBHOOK_URL not set, webhook not configured")

# Set webhook when the app starts
set_webhook()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
