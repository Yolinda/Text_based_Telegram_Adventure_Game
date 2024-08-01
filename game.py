# Import local files
from helpers import __read_config, __select_story_file

# Import other files
import json
import telegram
from telegram import (
    Chat, 
    ChatMember, 
    ChatMemberUpdated, 
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Game, 
    GameHighScore, 
    _games
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

# Read data from stories file
with open(__select_story_file(), 'r') as read_story:
    story = read_story.read()
scenes = json.loads(story)

async def __game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Start the Game!
        Display an Game Introduction
    """
    global scene_number
    global game_type

    scene_number = str(1)
    player_name = update.effective_user.first_name
    game_type = False

    # Create the Game Introduction
    intro = f"Welcome to <b>MY GAME</b>, {player_name}."
    intro+= "[### INSERT INTRODUCTION ###]"

    await update.effective_chat.send_message(
        intro,
        parse_mode=telegram.constants.ParseMode.HTML
    )

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="__gameType_story"),
            InlineKeyboardButton("No", callback_data="__gameType_quizzes"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def __game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    global game_type_selected
    global scene_number

    # If not the start of Game, set the Scene Number to the option the Player selected
    if query.data != '__gameType_story':
        scene_number = int(query.data)
        scene_number = str(scene_number)

    # If start of game, set the Game Selection Type which will be used to determine the type of Game the
    # Player wants to Play
    if query.data == '__gameType_story':
        game_type_selected = '__gameType_story'

    if game_type_selected == '__gameType_story':
        await query.message.reply_text("something")
        game_type_selected = '__gameType_story'

        """ Execute Story Game """
        # Print Scene Introduction
        if isinstance(scenes[scene_number]['intro'], str) == True:
            await query.message.reply_text(
                scenes[scene_number]['intro'],
                parse_mode=telegram.constants.ParseMode.HTML
            )

        elif isinstance(scenes[scene_number]['intro'], list) == True:
            for paragraph in scenes[scene_number]['intro']:
                await query.message.reply_text(
                    paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
        elif isinstance(scenes[scene_number]['intro'], dict) == True:
            for paragraph in scenes[scene_number]['intro']:
                await query.message.reply_text(
                    scenes[scene_number]['intro'][paragraph],
                    parse_mode=telegram.constants.ParseMode.HTML
                )
        
        # Print Scene Story
        if isinstance(scenes[scene_number]['story'], str) == True:
            await query.message.reply_text(
                scenes[scene_number]['story'],
                parse_mode=telegram.constants.ParseMode.HTML
            )

        elif isinstance(scenes[scene_number]['story'], list) == True:
            for paragraph in scenes[scene_number]['story']:
                await query.message.reply_text(
                    paragraph,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
        elif isinstance(scenes[scene_number]['story'], dict) == True:
            for paragraph in scenes[scene_number]['story']:
                await query.message.reply_text(
                    scenes[scene_number]['intro'][paragraph],
                    parse_mode=telegram.constants.ParseMode.HTML
                )

        # Display Keyboard Options
        keyboard = [
            [
                InlineKeyboardButton(
                    scenes[scene_number]['options']['1']['text'], 
                    callback_data=scenes[scene_number]['options']['1']['link']
                ),
                InlineKeyboardButton(
                    scenes[scene_number]['options']['2']['text'], 
                    callback_data=scenes[scene_number]['options']['2']['link']
                ),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("Please choose:", reply_markup=reply_markup)
    
    elif query.data == '__gameType_quizzes':
        """ Execute Quiz Game """


def main() -> None:
    """
    # Run the bot
    """
    # Create the application and pass it your bot's token
    application = Application.builder().token(__read_config('API_KEYS','Telegram_token')).build()

    application.add_handler(CommandHandler("start", __game_start))
    application.add_handler(CallbackQueryHandler(__game))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()