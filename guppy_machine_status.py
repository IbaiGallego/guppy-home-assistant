import psutil
import telebot
import time
import os
from dotenv import load_dotenv

#### LOAD ENVIRONMENT VARIABLES ####

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CAP_ID = int(os.getenv('MY_ID'))

#### INITIALIZE TELEGRAM BOT ####

guppy = telebot.TeleBot(TOKEN)

#### FUNCTIONS ####

def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp_str = file.read().strip()
            temp_celsius = int(temp_str) / 1000.0
            return temp_celsius
    except FileNotFoundError:
        return None

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def send_telegram_message(message):
    guppy.send_message(CAP_ID, message)

def main():
    while True:
        # Get CPU temperature and usage
        cpu_temp = get_cpu_temperature()
        cpu_usage = get_cpu_usage()

        if cpu_temp is not None:
            message = (f"CPU Temperature: {cpu_temp:.2f}°C\n"
                       f"CPU Usage: {cpu_usage:.2f}%")
        else:
            message = "Could not read CPU temperature.\n"
            message += f"CPU Usage: {cpu_usage:.2f}%"

        # Send the message via Telegram
        send_telegram_message(message)

        # Wait for 10 seconds before the next check
        time.sleep(10)

if __name__ == "__main__":
    main()

