from dotenv import load_dotenv
import os
import telebot

#### LOAD ENVIRONMENT VARIABLES ####

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CAP_ID = int(os.getenv('MY_ID'))



#### INITIALIZE TELEGRAM BOT ####

guppy = telebot.TeleBot(TOKEN)



#### AUTHENTICATION v.1.0 ####

def guppy_auth(chat_id: int) -> bool:
  '''
  Checks if user is the captain
  '''
  if chat_id == CAP_ID:
    return True
  else:
    return False



#### COMMANDS ####

@guppy.message_handler(commands=['Guppy'])
def greet(message):

  chat_id = int(message.chat.id)

  message_for_captain = 'Aye Captain'

  message_unauth_user = 'UNAUTHORIZED USER DETECTED'

  if chat_id == CAP_ID:
    guppy.send_message(chat_id, message_for_captain)

  else:
    guppy.send_message(chat_id, message_unauth_user)



#### INITIALIZES GUPPY ####

guppy.polling()