import os
from dotenv import load_dotenv
import requests
import openai

url = 'https://habr.com/ru/feed/'

url_response = requests.get(url)

if url_response.status_code == 200:
    print("200 OK")
else:
    print(f"Request failed with status code: {url_response.status_code}")


load_dotenv()

CLOUD_FOLDER = os.getenv("CLOUD_FOLDER")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_MODEL = os.getenv("CLOUD_MODEL")

client = openai.OpenAI(
  api_key=CLOUD_API_KEY,
  base_url="https://ai.api.cloud.yandex.net/v1",
  project=CLOUD_FOLDER
)

response = client.responses.create(
  model=f"gpt://{CLOUD_FOLDER}/{CLOUD_MODEL}",
  temperature=0.3,
  instructions="Отвечай кратко и по-русски. Как ты должен понимать важность информации: пиши о событиях, которые действительно случились. Пиши о законах, которые приняты, а не просто обсуждаются.",
  input=f"Составь дайджест с этой страницы {url_response.text[:1000]}, выдели оттуда важную информацию.",
  max_output_tokens=500
)

print(response.output_text)