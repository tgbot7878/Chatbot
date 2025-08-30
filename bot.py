import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini model API endpoint (assuming you're using a local or remote API)
GEMINI_API_URL = "http://your-gemini-api-endpoint.com/infer"  # Replace with actual URL
GEMINI_API_KEY = "your_gemini_api_key"  # Replace with your API key if necessary

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello! I am your AI assistant. How can I help you today?")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle messages sent by the user."""
    user_message = update.message.text

    # Make a request to the Gemini model
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {"input": user_message}

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        ai_response = response.json().get("response", "Sorry, I couldn't process that.")
        update.message.reply_text(ai_response)
    else:
        update.message.reply_text("Sorry, something went wrong. Please try again later.")

def main():
    """Start the bot."""
    # Set up the Updater with your Telegram token
    TELEGRAM_TOKEN = "your_telegram_bot_token"  # Replace with your Telegram bot token
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    # Handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
  
