from colorama import Style
import discord, datetime, time, flask, requests, json, threading, os, random, httpx, tls_client, sys, base64
from flask import request
from pathlib import Path
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
if os.name == 'nt':
    import ctypes

app = flask.Flask(__name__)

def validateInvite(invite:str): # Checks if the invite is valid
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    if 'type' in client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text:
        return True
    else:
        return False 
    
def getInviteInfo(invite:str): # Gets the invite info
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False    
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo
    except:
        return False
    
def getInviteChannel(invite:str): # Gets the invite channel
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['channel']['name']
    except:
        return False
    
def getInviteGuild(invite:str): # Gets the invite guild
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['name']
    except:
        return False
    
def getInviteGuildID(invite:str): # Gets the invite guild ID
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False    
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['id']
    except:
        return False
    
def getInviteGuildIcon(invite:str): # Gets the invite guild icon
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False    
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['icon']
    except:
        return False
    
def getInviteGuildSplash(invite:str): # Gets the invite guild splash
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['splash']
    except:
        return False
    
def getInviteGuildBanner(invite:str): # Gets the invite guild banner
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['banner']
    except:
        return False
    
def getInviteGuildDescription(invite:str): # Gets the invite guild description
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['description']
    except:
        return False

def getInviteGuildFeatures(invite:str): # Gets the invite guild features
    invite = invite.replace('https://discord.gg/', '')
    if validateInvite(invite) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        inviteInfo = json.loads(client.get(f'https://discord.com/api/v10/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true').text)
        return inviteInfo['guild']['features']
    except:
        return False