## IMPORTS ##
import os
import json
import random
import logging
import time
import configparser

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

"""-------------------------------------------------------
# CONFIGURATION
# Process configuration and set the values defined
# in the config.ini file
-------------------------------------------------------"""
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
# Set configuration values obtained from config.ini file
TELEGRAM_TOKEN = config['API_KEYS']['Telegram_token']
SLEEP_TIME = config['DEFAULT']['Sleep_time']
STORIES_PATH = config['DEFAULT']['Stories_path']

"""-------------------------------------------------------
# STORIES FILE
# Select a random file by generating a random number based
# on the total number of stories files in the folder
-------------------------------------------------------"""
directory = os.listdir(STORIES_PATH)
number_of_files = len(directory)
#random_number = str(random.randint(1,number_of_files))
random_number = '3'
story_file = str(STORIES_PATH + 'data_' + random_number + '.json')
# Read the stories file to get all of the content
with open(story_file, 'r') as fullStory:
    scene_story = fullStory.read()
scenes = json.loads(scene_story)

"""-------------------------------------------------------
# LOGGING
# Enable Logging
-------------------------------------------------------"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

"""-------------------------------------------------------
# GAME FUNCTIONS
-------------------------------------------------------"""
async def __game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ 
    # Start of the Game
    # Read the content from the first record in the file
    """
    __scene_number = str('2')

    # Execute if string
    if isinstance(scenes[__scene_number]['intro'], str) == True:
        await update.message.reply_text(
            scenes[__scene_number]['intro'],
            parse_mode=telegram.constants.ParseMode.HTML
        )
    # Execute if list
    elif isinstance(scenes[__scene_number]['intro'], list) == True:
        for paragraph in scenes[__scene_number]['intro']:
            print(scenes[__scene_number]['intro'][paragraph])


def __read_file(scene: str='3', scene_section: str='intro') -> None:
    __story = None
    file = open('stories/data_3.json')
    __story = json.load(file)
    return __story

def main() -> None:
    """
    # Run the bot
    """
    # Create the application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    __read_file()

    print("FUCK!")

    application.add_handler(CommandHandler("start", __game_start))

# Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
