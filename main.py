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

# Import story from JSON file
# read file
with open('data.json', 'r') as myfile:
   scene_story = myfile.read()

# parse file
scenes = json.loads(scene_story)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

COUNT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    for scene_story in scenes:
        if scene_story == '1':

            keyboard = [
                [
                    InlineKeyboardButton(scenes[scene_story]['option_1']['text'], callback_data=scenes[scene_story]['option_1']['link']),
                    InlineKeyboardButton(scenes[scene_story]['option_2']['text'], callback_data=scenes[scene_story]['option_2']['link']),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                scenes[scene_story]['intro']
            )

            await update.message.reply_text(
                scenes[scene_story]['story'], 
                reply_markup=reply_markup
            )
            
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    # Build scene to display
    global COUNT
    COUNT = COUNT + 1
    display_scene = str(COUNT)

    # Get the option selected by the player
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    # Create the various scenes
    """ Section A: Explore the Cell """
    #if query.data == "scene_1":

    for scene_story in scenes:
        if scene_story == display_scene:
            # Create options
            keyboard = [
                [
                    InlineKeyboardButton(scenes[scene_story]['option_1']['text'], callback_data=scenes[scene_story]['option_1']['link']),
                    InlineKeyboardButton(scenes[scene_story]['option_2']['text'], callback_data=scenes[scene_story]['option_2']['link']),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(
                scenes[scene_story]['intro']
            )

            await query.message.reply_text(
                scenes[scene_story]['story'], 
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