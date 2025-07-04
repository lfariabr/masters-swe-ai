import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_discord_message(message):
    url = DISCORD_WEBHOOK_URL
    data = {"content": message}
    response = requests.post(url, json=data)
    return response.status_code