import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

def make_request(prompt:str):
  '''
  Sends a request to Chat GPT API with GUPPYs system prompt (ROLE).
  '''

  with open("BRAIN/system.txt", "r") as f:
    system = f.read()


  url = "https://api.openai.com/v1/chat/completions"
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  data = {
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": system},
      {"role": "user", "content": prompt}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }

  response = requests.post(url, headers=headers, json=data)
  response_data = response.json()
  return response_data['choices'][0]['message']['content'],  response.status_code


if __name__ == "__main__":

  response, status = make_request("how are you guppy?")

  print(response)