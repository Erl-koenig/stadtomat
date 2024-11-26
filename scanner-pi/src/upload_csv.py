import supabase
from config import SUPABASE_KEY, SUPABASE_URL
from pathlib import Path
import requests


def check_internet_connection():
    """
    Check if the device is connected to the internet
    """
    url = "http://www.google.com"
    timeout = 10
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def upload_file(file: Path):
    """
    Upload a file to a remote server
    """
    if check_internet_connection() is False:
        print("no internet connection")
        return False
    client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)
    try:
        with open(file, "rb") as f:
            response = client.storage.from_("piece_image").upload(
                file=f,
                path=f"csv/{file.name}",
                file_options={"cache-control": "3600", "upsert": "false"},
            )
            if not response:
                print(f"Error uploading file {file}")
                return False
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error uploading file {file}")
        return False
    return True
