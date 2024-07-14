# Import packages
import os
import json
import random
import logging
import time
import configparser

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

""" Configuration Processing """
# Read parameters from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# Set configurations to use in the file
TELEGRAM_TOKEN = config['API_KEYS']['Telegram_token']
SLEEP_TIME = int(config['DEFAULT']['Sleep_Time'])

""" Import story from JSON file """
# count number of files in stories folder
lst = os.listdir('stories/') # your directory path
number_of_stories = len(lst)

# Select a random story
number = str(random.randint(1,number_of_stories))
story_file = str('stories/data_' + number + '.json')

# read file
with open(story_file, 'r') as myfile:
   scene_story = myfile.read()

# parse file
scenes = json.loads(scene_story)

#print(type(scenes['1']['intro']))
#print(type(scenes['1']['option_2']))

#data = "<class 'dict'>"
#print(isinstance(data, dict) or isinstance(data, str))

player_chat_id = ''

""" Enable logging """
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    # Set the player chat id, which is needed to send images back to the player
    global player_chat_id
    player_chat_id = update.effective_chat.id

    for scene_story in scenes:
        if scene_story == '1':

            keyboard = [
                [
                    InlineKeyboardButton(scenes[scene_story]['option_1']['text'], callback_data=scenes[scene_story]['option_1']['link']),
                    InlineKeyboardButton(scenes[scene_story]['option_2']['text'], callback_data=scenes[scene_story]['option_2']['link']),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            intro = scenes[scene_story]['intro'].split("|")

            for intro_paragraph in intro:
                # Display image to uer
                #await update.message.reply_photo(
                #    photo=open('user_photo.jpg', 'rb')
                #)

                # Display video to user
                #await update.message.reply_video(
                #    video=open('video.mp4', 'rb')
                #)

                await update.message.reply_text(
                    intro_paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
                time.sleep(SLEEP_TIME)

            story = scenes[scene_story]['story'].split("|")

            for story_paragraph in story:

                await update.message.reply_text(
                    story_paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )

                time.sleep(SLEEP_TIME)

            if scenes[scene_story]['option_1']['link'] != "" and scenes[scene_story]['option_2']['link'] != "":
                await update.message.reply_text(
                    "What next?", 
                    reply_markup=reply_markup,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
            
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    
    # Get the option selected by the player
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    # Create the various scenes
    #if query.data == "scene_1":
    display_scene = query.data

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
                query.data
            )
            
            intro = scenes[scene_story]['intro'].split("|")

            for intro_paragraph in intro:
                
                await query.message.reply_text(
                    intro_paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
                time.sleep(SLEEP_TIME)

            story = scenes[scene_story]['story'].split("|")

            for story_paragraph in story:
                await query.message.reply_text(
                    story_paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
                time.sleep(SLEEP_TIME)
            
            if scenes[scene_story]['option_1']['link'] != "" and scenes[scene_story]['option_2']['link'] != "":
                await query.message.reply_text(
                    "Whats next?", 
                    reply_markup=reply_markup,
                    parse_mode=telegram.constants.ParseMode.HTML
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