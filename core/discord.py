import requests
import os

DISCORD_WEBHOOK = os.getenv("WEBHOOK")

def send_discord(message):
    if not DISCORD_WEBHOOK:
        return
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=data)
