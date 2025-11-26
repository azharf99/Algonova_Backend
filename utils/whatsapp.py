import requests
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("TOKEN")
secret_key = os.getenv("SECRET_KEY")

url = "https://jogja.wablas.com/api/schedule"

def create_schedule(data):
    headers = {
        "Authorization": f"{token}.{secret_key}"
    }

    response = requests.post(
        url,
        data=data,
        headers=headers,
        verify=False
    )

    return response.json()
