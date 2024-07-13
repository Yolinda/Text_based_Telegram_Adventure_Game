import json
import random
import logging
import time
import configparser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

## Configuration processing
## Read parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

TELEGRAM_TOKEN = config['API_KEYS']['Telegram_token']

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="section_a"),
            InlineKeyboardButton("Option 2", callback_data="section_b"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    
    # Get the option selected by the player
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    # Create the various scenes
    """ Section A: Explore the Cell """
    if query.data == "section_a":
        # Create options
        keyboard = [
            [
                InlineKeyboardButton("Escape Through the Window", callback_data="section_a"),
                InlineKeyboardButton("Hide Under the Bed", callback_data="section_b"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            text="What do you do next?", 
            reply_markup=reply_markup
        )

    elif query.data == "section_b":
        """ Section B: Call for Help """

        # Create options
        keyboard = [
            [
                InlineKeyboardButton("Approach the Door", callback_data="section_a"),
                InlineKeyboardButton("Stay Back", callback_data="section_b"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Define Display Text

        await query.message.reply_text(
            text="what do you do next?", 
            reply_markup=reply_markup
        )
    


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(game))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()