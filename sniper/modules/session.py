from colorama import Style
import discord, datetime, time, flask, requests, json, threading, os, random, httpx, tls_client, sys, base64
from flask import request
from pathlib import Path
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
if os.name == 'nt':
    import ctypes

currentPath = os.path.dirname(os.path.realpath(__file__))
fingerprints = json.load(open(f"{currentPath}/fingerprints.json", "r")) # Loads fingerprints from fingerprints.json
client_identifiers = ['safari_ios_16_0', 'safari_ios_15_6', 'safari_ios_15_5', 'safari_16_0', 'safari_15_6_1', 'safari_15_3', 'opera_90', 'opera_89', 'firefox_104', 'firefox_102']

app = flask.Flask(__name__)

def getClient(): # Gets a requests session
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    client.get('https://discord.com/')

    return client
    
def getTlsClient(): # Gets a tls_client session
    session = tls_client.Session(ja3_string = fingerprints[random.randint(0, (len(fingerprints)-1))]['ja3'], client_identifier = random.choice(client_identifiers))
    
    return session
    