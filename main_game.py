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

from helpers import __read_config, __select_story_file

""" ------------------ GAME ------------------ """
# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Read content from the selected JSON file
with open(__select_story_file(), 'r') as full_story:
    scene_story = full_story.read()
scenes = json.loads(scene_story)

# Define scene number
__scene_number = str('3')

async def __game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
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
    
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def __play_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    
    if isinstance(scenes[__scene_number]['intro'], str) == True:
        await query.message.reply_text(
            scenes[__scene_number]['intro'],
            parse_mode=telegram.constants.ParseMode.HTML
        )

    elif isinstance(scenes[__scene_number]['intro'], list) == True:
        for paragraph in scenes[__scene_number]['intro']:
            await query.message.reply_text(
                paragraph,
                parse_mode=telegram.constants.ParseMode.HTML
            )
    elif isinstance(scenes[__scene_number]['intro'], dict) == True:
        for paragraph in scenes[__scene_number]['intro']:
            await query.message.reply_text(
                scenes[__scene_number]['intro'][paragraph],
                parse_mode=telegram.constants.ParseMode.HTML
            )
    
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("Please choose:", reply_markup=reply_markup)

async def __help_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")

def main() -> None:
    """
    # Run the bot
    """
    # Create the application and pass it your bot's token
    application = Application.builder().token(__read_config('API_KEYS','Telegram_token')).build()

    application.add_handler(CommandHandler("start", __game_start))
    application.add_handler(CallbackQueryHandler(__play_game))
    application.add_handler(CommandHandler("help", __help_me))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
