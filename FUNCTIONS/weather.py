import requests
import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("WEATHER_API")

def get_weather(city):
    # Define the URL for the API call
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # Send the request to the API
    response = requests.get(url)
    
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant information
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        message = f"""Weather in {city}:
Temperature: {temperature}°C
Description: {weather_description}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
"""

    else:
        message = f"Failed to get weather response Status Code: {response.status_code}"

    return message

def will_it_rain(lat = 40.4297, lon = -3.6452):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        rain = False

        for i in range(8):
            if data["list"][i]["weather"][0]["main"] == "Rain":
                rain = True
                return rain
            
        return rain

if __name__=='__main__':
    print(will_it_rain())