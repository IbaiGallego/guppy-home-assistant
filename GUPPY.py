from dotenv import load_dotenv
import os
import telebot
import schedule
import time
import requests
from io import BytesIO
from threading import Thread
from PIL import Image

import BRAIN.logos as logos
import FUNCTIONS.cpu as cpu
import FUNCTIONS.weather as weather
import FUNCTIONS.nasa as nasa


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

#### COMMAND FUNCTIONS ####

@guppy.message_handler(func=lambda message: message.text.startswith(r'/message'))
def guppy_message_handler(message):
   if guppy_auth(message): 
    message_text = message.text.replace(r'/message', '').strip()
    if message_text:
      response, status = logos.make_request(message.text)
      if status == 200:
        send_telegram_message(response)
      else:
        send_telegram_message(f"Sorry Captain, connection was lost Status code: {status}")
    else:
      send_telegram_message("No message to send")

@guppy.message_handler(commands=['help'])
def help(message):
  if guppy_auth(message):  
    response_message = r'''
{/cpu}
returns cpu temperature

_______________

{/weather}
if command by itself, returns weather of Madrid
if followed by city with with a single capital letter returns weather at that city

_______________

{/message}
sends request to gpt-3.5-turbo with the message

_______________

{/rain}
will manually check for rain in madrid
'''
  send_telegram_message(response_message)

@guppy.message_handler(commands=['cpu'])
def cpu_status(message):
  if guppy_auth(message):  
    response_message = cpu.main()
    send_telegram_message(response_message)

@guppy.message_handler(func=lambda message: message.text.startswith(r'/weather'))
def get_weather_api(message):
  if guppy_auth(message):  
    city = message.text.replace(r'/weather', '').strip()
    if not city:
      response_message = weather.get_weather('Madrid')
    else:
      response_message = weather.get_weather(city)
    send_telegram_message(response_message)

@guppy.message_handler(commands=['rain'])
def manual_check_for_rain(message):
  if guppy_auth(message):
    check_for_rain()

@guppy.message_handler(commands=['nasapic'])
def manual_get_pic_of_day(message):
  if guppy_auth(message):
    get_nasa_pic_of_day()

#### SCHEDULER FUNCTIONS ####
    
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Sleep for 1 hour


import requests
from io import BytesIO
from PIL import Image

def resize_image(image_data, max_total_pixels=10000, max_ratio=20):
    """
    Resizes an image to ensure the width and height do not exceed 10000 pixels combined,
    and that the width-to-height ratio does not exceed 20.
    
    :param image_data: BytesIO object containing the original image data.
    :param max_total_pixels: Maximum allowed total pixels (width + height).
    :param max_ratio: Maximum allowed width-to-height ratio.
    :return: BytesIO object containing the resized image data.
    """
    # Open the image from the BytesIO object
    image = Image.open(image_data)

    # Check the total pixels and aspect ratio
    width, height = image.size
    total_pixels = width + height
    aspect_ratio = width / height if height != 0 else max_ratio + 1  # Prevent division by zero

    # Resize if necessary
    if total_pixels > max_total_pixels or aspect_ratio > max_ratio:
        # Calculate the new size to fit within the constraints
        scale_factor = min(max_total_pixels / total_pixels, max_ratio / aspect_ratio)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height), Image.LANCZOS)

    # Save the resized image to a new BytesIO object
    resized_image_io = BytesIO()
    image.save(resized_image_io, format='JPEG')  # Save as JPEG for compatibility
    resized_image_io.name = 'resized_image.jpg'
    resized_image_io.seek(0)  # Reset the stream position to the beginning
    
    return resized_image_io

def get_nasa_pic_of_day():
    # Fetch the image URL and explanation from NASA
    image_url, explanation = nasa.get_nasa_picture_of_day()

    # Fetch the image from the URL
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Use BytesIO to keep the image in memory as a file-like object
        original_image_io = BytesIO(response.content)
        original_image_io.name = 'nasa_image.jpg'  # Giving a name to the file

        # Resize the image using the resize_image function
        resized_image_io = resize_image(original_image_io)
        
        # Send the resized image
        guppy.send_photo(CAP_ID, photo=resized_image_io)
        
        # Close the BytesIO objects
        original_image_io.close()
        resized_image_io.close()
        
        # Send the explanation
        send_telegram_message("This is the NASA explanation")
        send_telegram_message(explanation)
    else:
        guppy.send_message(CAP_ID, "Failed to retrieve the image.")


def check_for_rain():
  response_message = ""
  if weather.will_it_rain():
    response_message = "Good Day Cap. It will rain today, no need to water your plants. Dont forget your umbrella."
    send_telegram_message()
  else:
    response_message = "No Rain Today Captain. Did you remember to water the plants?"

def did_you_wash_clothes():
  response_message = "Good day Cap. Did you wash your clothes this week? I have a feeling you are getting somewhat stinky."

schedule.every().day.at("09:00").do(check_for_rain)
schedule.every().day.at("22:00").do(get_nasa_pic_of_day)
schedule.every().sunday.at("11:00").do(did_you_wash_clothes)
# Start the scheduler in a separate thread
scheduler_thread = Thread(target=run_scheduler)
scheduler_thread.start()

#### INITIALIZES GUPPY ####

guppy.polling()