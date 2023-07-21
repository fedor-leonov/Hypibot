import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
hypixelKey = os.getenv('HYPIXELKEY')

async def convertToUUID(username):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://api.mojang.com/users/profiles/minecraft/{username}') as playerInfo:
            data = await playerInfo.json()
            return data['id']
            

async def getPlayerData(username, aspect):
    uuid = await convertToUUID(username)
    params = {'key': hypixelKey, 'uuid': uuid}
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://api.hypixel.net/{aspect}', params=params) as playerData:
            data = await playerData.json()
            if data['success']:
                return data
            else:
                raise Exception("API error")