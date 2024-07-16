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

# Define scene number
__scene_number = str('3')

if isinstance(scenes[__scene_number]['intro'], list) == True:
    for paragraph in scenes[__scene_number]['intro']:
        print(paragraph)

"""-------------------------------------------------------
# GAME FUNCTIONS
-------------------------------------------------------"""
async def __game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ 
    # Start of the Game
    # Read the content from the first record in the file
    """
    keyboard = [
                [
                    InlineKeyboardButton("Option 1", callback_data="1"),
                    InlineKeyboardButton("Option 2", callback_data="2")
                ]
            ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(scenes[__scene_number]['intro'], str) == True:
        await update.message.reply_text(
            scenes[__scene_number]['intro'],
            parse_mode=telegram.constants.ParseMode.HTML
        )

    elif isinstance(scenes[__scene_number]['intro'], list) == True:
        for paragraph in scenes[__scene_number]['intro']:
            await update.message.reply_text(
                paragraph,
                parse_mode=telegram.constants.ParseMode.HTML
            )
    elif isinstance(scenes[__scene_number]['intro'], dict) == True:
        for paragraph in scenes[__scene_number]['intro']:
            await update.message.reply_text(
                scenes[__scene_number]['intro'][paragraph],
                parse_mode=telegram.constants.ParseMode.HTML
            )
    
    await update.message.reply_text(
        "What's Next?",
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup,
    )

async def __play_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the option selected by the player
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    # Create the various scenes
    #if query.data == "scene_1":
    __scene_number = query.data

    if isinstance(scenes[__scene_number]['story'], str) == True:
        await update.message.reply_text(
            scenes[__scene_number]['story'],
            parse_mode=telegram.constants.ParseMode.HTML
        )

    elif isinstance(scenes[__scene_number]['story'], list) == True:
        for paragraph in scenes[__scene_number]['story']:
            await update.message.reply_text(
                paragraph,
                parse_mode=telegram.constants.ParseMode.HTML
            )
    elif isinstance(scenes[__scene_number]['story'], dict) == True:
        for paragraph in scenes[__scene_number]['story']:
            await update.message.reply_text(
                scenes[__scene_number]['intro'][paragraph],
                parse_mode=telegram.constants.ParseMode.HTML
            )

def main() -> None:
    """
    # Run the bot
    """
    # Create the application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", __game_start))
    application.add_handler(CallbackQueryHandler(__play_game))

# Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()