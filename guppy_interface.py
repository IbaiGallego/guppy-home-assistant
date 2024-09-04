from dotenv import load_dotenv
import os
import telebot
import BRAIN.logos as logos
import FUNCTIONS.cpu as cpu
import FUNCTIONS.weather as weather

#### LOAD ENVIRONMENT VARIABLES ####

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CAP_ID = int(os.getenv('MY_ID'))

guppy = telebot.TeleBot(TOKEN)

#### AUTHENTICATION v.1.0 ####

def guppy_auth(message) -> bool:
  '''
  Checks if user is the captain
  '''
  chat_id = message.chat.id
  if chat_id == CAP_ID:
    return True
  else:
    return False

#### BASE SEND MESSAGE FUNCTION ####

def send_telegram_message(message):
    '''
    specific function to send message to captain.
    '''
    guppy.send_message(CAP_ID, message)

#### MESSAGE HANDLER ####

@guppy.message_handler(func=lambda message: message.text.startswith(r'\message'))
def guppy_message_handler(message):
   if guppy_auth(message): 
    response, status = logos.make_request(message.text)
    if status == 200:
      send_telegram_message(response)
    else:
      send_telegram_message(f"Sorry Captain, connection was lost Status code: {status}")

@guppy.message_handler(commands=['help'])
def help(message):
  if guppy_auth(message):  
    message = '''Current Commands:
  \cpu  ->  returns cpu temperature
  \weather
    ->  if command by itself, returns weather of Madrid
    ->  id followed by city with with a single capital letter returns weather at that city
  \message  ->  sends request to gpt-3.5-turbo with the message
'''

@guppy.message_handler(commands=['cpu'])
def cpu_status(message):
  if guppy_auth(message):  
    message = cpu.main()
    send_telegram_message(message)

@guppy.message_handler(func=lambda message: message.text.startswith(r'\weather'))
def get_weather_api(message):
  if guppy_auth(message):  
    city = message.text.replace(r'\weather', '').strip()
    if not city:
      message = weather.get_weather('Madrid')
    else:
      message = weather.get_weather(city)
    send_telegram_message(message)

#### INITIALIZES GUPPY ####

guppy.polling()