import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("TOKEN")
secret_key = os.getenv("SECRET_KEY")

url = "https://jogja.wablas.com/api/v2/schedule"

def create_schedule(data_list):
    headers = {
        "Authorization": f"{token}.{secret_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        data=json.dumps(data_list),
        headers=headers,
        verify=False
    )

    return response.json()
