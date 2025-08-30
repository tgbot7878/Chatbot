import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Railway Environment variables se
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
MODEL_NAME = os.environ.get('MODEL', 'gemini-pro')

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# Store conversation history
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Namaste {user.first_name}! 🙏\n\n"
        "Main ek AI assistant hoon Gemini AI se powered. "
        "Aap mujhse kuch bhi pooch sakte hain!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
Available Commands:
/start - Bot shuru karein
/help - Yeh help message dikhayein
/about - Bot ke baare mein jaanein
/clear - Conversation history clear karein

Bas message likhkar bhejein aur main aapki help karunga!
    """
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot."""
    about_text = """
🤖 Gemini AI Telegram Bot

Powered by Google's Gemini AI technology.
Developed with Python and python-telegram-bot library.

Hosted on Railway.app - 24/7 Always On!
    """
    await update.message.reply_text(about_text)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation history."""
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text("Conversation history cleared! ✅")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and generate response using Gemini AI."""
    try:
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Show typing action
        await update.message.chat.send_action(action="typing")
        
        # Initialize conversation history if not exists
        if user_id not in conversations:
            conversations[user_id] = []
        
        # Add user message to history
        conversations[user_id].append({"role": "user", "parts": [user_message]})
        
        # Generate response using Gemini AI with history
        response = model.generate_content(conversations[user_id])
        
        # Add model response to history
        conversations[user_id].append({"role": "model", "parts": [response.text]})
        
        # Keep only last 10 messages to avoid context overflow
        if len(conversations[user_id]) > 10:
            conversations[user_id] = conversations[user_id][-10:]
        
        # Send the response back to user
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Error in handling message: {e}")
        await update.message.reply_text("Mujhe kuch technical problem ho rahi hai. Thodi der baad try karein.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Check if tokens are set
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set in environment variables")
        return
        
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set in environment variables")
        return
    
    # Create Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the Bot
    print("🤖 Bot is running on Railway...")
    print(f"🔧 Using model: {MODEL_NAME}")
    application.run_polling()

if __name__ == '__main__':
    main()
