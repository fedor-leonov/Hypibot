import requests
import os
from dotenv import load_dotenv

load_dotenv()
hypixelKey = os.getenv('HYPIXELKEY')

def convertToUUID(username):
    return requests.get(url = f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]

def getPlayerData(username, aspect):
    uuid = convertToUUID(username)
    data = requests.get(
        url = f"https://api.hypixel.net/{aspect}",
        params = {
            "key": f"{hypixelKey}",
            "uuid": f"{uuid}"
        }
    ).json()
    if data["success"]:
        return data
    else:
        raise Exception("API error")