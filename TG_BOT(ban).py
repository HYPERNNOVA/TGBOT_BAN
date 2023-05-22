from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with the token obtained from the BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Define a dictionary to store ban reasons
ban_reasons = {}

# Define the function to handle the /b command
def ban_user(update, context):
    message = update.message
    chat_id = message.chat_id
    user_id = message.reply_to_message.from_user.id
    ban_reason = context.args

    # Check if the user who triggered the command is an admin
    chat_member = context.bot.get_chat_member(chat_id, message.from_user.id)
    if not chat_member.is_chat_admin():
        message.reply_text("Only admins are authorized to ban users.")
        return

    # Ban the user
    context.bot.kick_chat_member(chat_id, user_id)

    # Save the ban reason
    ban_reason = ' '.join(ban_reason)
    ban_reasons[user_id] = ban_reason

    message.reply_text(f'Banned user {user_id} for reason: {ban_reason}')

# Define the function to handle the /banreason command
def ban_reason(update, context):
    message = update.message
    user_id = context.args[0]

    # Check if a ban reason is available for the user
    if user_id in ban_reasons:
        reason = ban_reasons[user_id]
        message.reply_text(f'Ban reason for user {user_id}: {reason}')
    else:
        message.reply_text(f'No ban reason available for user {user_id}')

# Define the function to handle all other messages
def handle_message(update, context):
    message = update.message

    # Check if the message starts with '/b'
    if message.text.startswith('/b'):
        ban_user(update, context)

# Set up the bot and register the command and message handlers
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('b', ban_user))
dispatcher.add_handler(CommandHandler('banreason', ban_reason))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
