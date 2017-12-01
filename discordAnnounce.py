import asyncio
import os
import random
import datetime
import discord
import json
import sys
from collections import OrderedDict

token = "MzU3NjA2NDQ0ODMwMjk0MDE3.DKHIMg.AWDhiu2xyLSHuRg-l0SSuiYJD5s"

discordClient = discord.Client()

def readJson():
	json_data=open("vars.json").read()
	data = json.loads(json_data, object_pairs_hook=OrderedDict)
	return data #an OrderedDict

async def announce():
    await discordClient.wait_until_ready()
    settings = readJson()

    messagePayload = "```" + str(sys.argv[1]) + " successfully synced" + "```"

    if(sys.argv[2] == "0"):
        messageRecipient = await discordClient.get_user_info(settings['Users']['Smoothtalk']['discord_ID'])
        await discordClient.send_message(messageRecipient, messagePayload)
    elif(sys.argv[2] == "1"):
        messageRecipient = await discordClient.get_user_info(settings['Users']['shinigamibob']['discord_ID'])
        await discordClient.send_message(messageRecipient, messagePayload)
    else:
        pass

    await discordClient.logout()

@discordClient.event
async def on_ready():
    print('Logged in as')
    print(discordClient.user.name)
    print(discordClient.user.id)
    await announce()
    print('-------')

discordClient.run(token)
