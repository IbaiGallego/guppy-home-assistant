import os
import dotenv
import requests

dotenv.load_dotenv()
api_key = os.getenv("NASA_API")


def get_nasa_picture_of_day():
    # Define the URL for the API call
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    # Send the request to the API
    response = requests.get(url)

    return response.json()["hdurl"], response.json()["explanation"]


if __name__=="__main__":
    print(get_nasa_picture_of_day())