import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("TOKEN")
secret_key = os.getenv("SECRET_KEY")

def create_schedule(data_list):
    if data_list:
        url = "https://jogja.wablas.com/api/v2/schedule"
        headers = {
            "Authorization": f"{token}.{secret_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            data=json.dumps(data_list),
            headers=headers,
            verify=False,
        )

        return response.json()
    return None


def update_schedule(data_list, schedule_id):
    if data_list:
        url = f"https://jogja.wablas.com/api/v2/schedule/{schedule_id}"
        headers = {
            "Authorization": f"{token}.{secret_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            data=json.dumps(data_list),
            headers=headers,
            verify=False,
        )

        return response.json()
    return None


def upload_files_to_wablas(group_name, student_name, course_name, feedback_number):

    # file type: image, audio, video, document
    upload_type = "document"
    # Local path to file
    file_path = f"C:/Users/HYPE AMD/Documents/Algonova_Backend/mediafiles/{group_name}/Rapor {student_name} Bulan ke-{feedback_number} {course_name}.pdf"
    # Prepare multipart form data
    files = {
        "file": (
            file_path.split("/")[-1],          # filename
            open(file_path, "rb"),             # file object
            "application/octet-stream"         # MIME type (optional)
        )
    }

    headers = {
        "Authorization": f"{token}.{secret_key}",
    }

    url = f"https://jogja.wablas.com/api/upload/{upload_type}"

    response = requests.post(
        url,
        headers=headers,
        files=files,   # multipart/form-data
        verify=False,   # matches PHP: disable SSL verification
    )

    return response.json()
