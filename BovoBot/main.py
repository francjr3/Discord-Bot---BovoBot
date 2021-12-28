# disc_bot.py
# 
# Author: Francisco Rodriguez Santana
# 
# Date: 12/14/2021
#
# Description:
# Discord bot that manages and moderates discord messages and interactions
# between users. Additional features available to help server owners and 
# server members alike.
#
# Additional Notes:
# Progam is run on replit.com using replit storage,
# discord library, and requests library. All commands start with '%'
#
import discord
import os
import requests
import json
import random
from replit import db
from keep_running import keep_run
import data_format
#from discord.ext.commands import has_permissions, CheckFailure, BadArgument

client = discord.Client()

ad_sad = ["sad", "depressed", "kms"]
banned_terms = []

if "message_scan" not in db.keys():
    db["message_scan"] = True
if "banned_terms" not in db.keys():
    db["banned_terms"] = []


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + "  -" + json_data[0]["a"]
    return quote


def update_bannedTerms(term):
    db["banned_terms"].append(term)
    return f"Banned terms list updated with \'{term}\'."

def delete_bannedTerm(term):
    if term in db["banned_terms"]:
        db["banned_terms"].remove(term)
        return f"\'{term}\', removed."
    else:
        return f"\'{term}\', not in banned terms list."



# called when bot is ready to use
@client.event
async def on_ready():
    print(f"Logged on as {client.user} - bot ready to use")


@client.event
async def on_message(message):
    # Ignores messages made by bot
    if message.author == client.user:
        return
    msg = message.content

    # Hello/welcome message
    if msg.startswith("%hello"):
        await message.channel.send(f"Hello {message.author}!")

    # API inspirational message
    elif msg.startswith("%inspiration"):
        quote = get_quote()
        await message.channel.send(quote)

    # Adds ban term.
    elif msg.startswith("%new_ban"):
        ban_term = msg.split("%new_ban ", 1)[1]
        await message.channel.send(update_bannedTerms(ban_term))
    # Removes ban term.
    elif msg.startswith("%del_ban"):
        ban_term = msg.split("%del_ban ", 1)[1]
        await message.channel.send(delete_bannedTerm(ban_term))

    # Lists banned terms.
    elif msg.startswith("%ban_list"):
        enc_list = db["banned_terms"]
        await message.channel.send(data_format.formatList("~Banned Term(s) list: ", enc_list.value))

    # Toggle message scanner.
    elif msg.startswith("%message_scan"):
        val = msg.split("%message_scan ", 1)[1]

        db["message_scan"] = False if val.lower() != "true" else True
        resp_msg = "Message Scan on" if db["message_scan"] else "Message Scan off"
        await message.channel.send(resp_msg)

    # Creates text thread with provided name if user has admin permissions
    elif msg.startswith("%create_channel"):
        channel_name = msg.split("%create_channel ", 1)[1]
        await message.guild.create_text_channel(channel_name)

    # Scans message for banned_terms.        
    elif db["message_scan"]:
        if any(word in msg for word in db["banned_terms"]):
            ban_used = [word for word in db["banned_terms"] if word in msg]
            await message.channel.send(f"\t~ WARNING ~\n~ Banned term(s) used: {ban_used} ~\n~ Continued use may result in admin intervention! ~") # Fix


keep_run()
client.run(os.environ['TOKEN'])

