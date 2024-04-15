from colorama import Style
import discord, datetime, time, flask, requests, json, threading, os, random, httpx, tls_client, sys, base64
from flask import request
from pathlib import Path
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

thread_lock = threading.Lock()

if os.name == 'nt':
    import ctypes

class Console:
    """Console utils"""

    @staticmethod
    def _time():
        return time.strftime("%H:%M:%S", time.gmtime())

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def sprint(content: str, status: bool = True) -> None:
        thread_lock.acquire()
        sys.stdout.write(
            f"{Fore.LIGHTBLACK_EX}{Console()._time()} |{Fore.RESET} {Fore.LIGHTGREEN_EX if status else Fore.RED}{content}"
            + "\n"
            + Fore.RESET
        )
        thread_lock.release()

app = flask.Flask(__name__)

def get_captcha_key(rqdata: str, site_key: str, websiteURL: str, useragent: str):

    task_payload = {
        'clientKey': "d64c29b9f2a169745fb25f7adbfff2f1",
        'task': {
            "type"             :"HCaptchaTaskProxyless",
            "isInvisible"      : True,
            "data"             : rqdata,
            "websiteURL"       : websiteURL,
            "websiteKey"       : site_key,
            "userAgent"        : useragent
                        }
    }
    key = None
    with httpx.Client(headers={'content-type': 'application/json', 'accept': 'application/json'},
                    timeout=30) as client:   
        task_id = client.post(f'https://api.capmonster.cloud/createTask', json=task_payload).json()['taskId']
        get_task_payload = {
            'clientKey': "d64c29b9f2a169745fb25f7adbfff2f1",
            'taskId': task_id,
        }
        

        while key is None:
            response = client.post("https://api.capmonster.cloud/getTaskResult", json = get_task_payload).json()
            if response['status'] == "ready":
                key = response["solution"]["gRecaptchaResponse"]
            else:
                time.sleep(1)
            
    return key
    

#join server
def join_server(session, headers, useragent, invite, token, thread):
    join_outcome = False
    guild_id = 0
    try:
        for i in range(10):
            response = session.post(f'https://discord.com/api/v9/invites/{invite}', json={}, headers = headers)
            if response.status_code == 429:
                Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{thread}{Fore.WHITE}] Rate Limited, Retrying: {Fore.RED}{token[:24] + '.' + '*' * (len(token) - 24)}", True)
                time.sleep(5)
                join_server(session, headers, useragent, invite, token)
                
            elif response.status_code in [200, 204]:
                Console().sprint(f"{Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{thread}{Fore.WHITE}] Joined Server: {Fore.GREEN}{token[:24] + '.' + '*' * (len(token) - 24)}", True)
                join_outcome = True
                guild_id = response.json()["guild"]["id"]
                break
                #variables.joins += 1
            elif "captcha_rqdata" in response.text:
                #{'captcha_key': ['You need to update your app to join this server.'], 'captcha_sitekey': 'a9b5fb07-92ff-493f-86fe-352a2803b3df', 'captcha_service': 'hcaptcha', 'captcha_rqdata': '6x2V9nU0sF4schdwvU80ptu4CQnFEJQz1cA0pvoTzBbkXzGPoJLljDVNvlJBWFUm5yqj4p83buOfIcHKSIGqDlARNU0/ik6Xp5dC3+xbEQvsxT1juCKbLB4mAlDR4UJOKwO7UKbW35kXxtP8HLJ2nusPOjZnGtlDKI0R5f85', 'captcha_rqtoken': 'InZ4akJpMzBtS2Y0SVlsSEIzTTE3Q1ArTzA5VlQrM1dSOFVUc3RBUTJkS0JTUC9UUG90TUU2TzBIUGtZQkhLd0lsQnFJZUE9PXA1WnptRnJLME1CMDlQaHgi.Y73eww.S3g5RodcfWcgWI7MLihE0lkgf4A'}
                Console().sprint(f"{Fore.WHITE}({Fore.RED}*{Fore.WHITE}) [{Fore.RED}{thread}{Fore.WHITE}] Captcha Detected: {Fore.YELLOW}{token[:24] + '.' + '*' * (len(token) - 24)}", False)
                r = response.json()
                solution = get_captcha_key(rqdata = r['captcha_rqdata'], site_key = r['captcha_sitekey'], websiteURL = "https://discord.com", useragent = useragent)
                #sprint(f"[{thread}] Solution: {solution[:60]}...", True)
                response = session.post(f'https://discord.com/api/v9/invites/{invite}', json={'captcha_key': solution,'captcha_rqtoken': r['captcha_rqtoken']}, headers = headers)
                if response.status_code in [200, 204]:
                    #sprint(f"[{thread}] Joined with Captcha: {token}", True)
                    join_outcome = True
                    guild_id = response.json()["guild"]["id"]
                    Console().sprint(f"{Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{thread}{Fore.WHITE}] Joined Server With Captcha: {Fore.GREEN}{token[:24] + '.' + '*' * (len(token) - 24)}", True)
                    break
                    #variables.joins += 1
                else:
                    Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{thread}{Fore.WHITE}] Failed to join server: {Fore.RED}{token[:24] + '.' + '*' * (len(token) - 24)} {response.text}", False)
                    break
                    
        return join_outcome, guild_id

            
    except Exception as e:
        Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{thread}{Fore.WHITE}] Retrying with error, {e}: {Fore.RED}{token[:24] + '.' + '*' * (len(token) - 24)}", False)
        join_server(session, headers, useragent, invite, token, thread)
        
def getTokenInfo(token): # Gets the token info
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    try:
        tokenInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me', headers={'Authorization': token}).text)
        return tokenInfo
    except:
        return False
    
def getTokenUsername(token): # Gets the token username
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        tokenInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me', headers={'Authorization': token}).text)
        return tokenInfo['username']
    except:
        return False

def getTokenEmail(token): # Gets the token email
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        tokenInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me', headers={'Authorization': token}).text)
        return tokenInfo['email']
    except:
        return False
    
def formatToken(token): # Formats the token
    if ':' in token:
        token = token.split(':')[-1]
        
    return token
    
def getTokenAvatar(token): # Gets the token avatar
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        tokenInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me', headers={'Authorization': token}).text)
        return tokenInfo['avatar']
    except:
        return False
        
def getTokenID(token): # Gets the token ID
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        tokenInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me', headers={'Authorization': token}).text)
        return tokenInfo['id']
    except:
        return False
    
def getBoostInfo(token): # Gets the boost info
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        boostInfo = json.loads(client.get(f'https://discord.com/api/v10/users/@me/guilds/premium/subscription-slots', headers={'Authorization': token}).text)
        return boostInfo
    except:
        return False
    
def tokenStatusCode(token):
    if validateToken(token) == False:
        return False
    client = requests.session()
    client.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    try:
        tokenStatusCode = client.get(f'https://discord.com/api/v10/users/@me/affinities/guilds', headers={'Authorization': token}).status_code
        return tokenStatusCode
    except:
        return False
    
currentPath = os.path.dirname(os.path.realpath(__file__))
fingerprints = json.load(open(f"{currentPath}/fingerprints.json", "r")) # Loads fingerprints from fingerprints.json

def get_fingerprint():
    try:
        fingerprint = httpx.get(f"https://discord.com/api/v10/experiments")
        return fingerprint.json()['fingerprint']
    except Exception as e:
        get_fingerprint()


def get_cookies(x, useragent):
    try:
        response = httpx.get('https://discord.com/api/v10/experiments', headers = {'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','content-type': 'application/json','origin': 'https://discord.com','referer':'https://discord.com','sec-ch-ua': f'"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': useragent, 'x-debug-options': 'bugReporterEnabled','x-discord-locale': 'en-US','x-super-properties': x})
        cookie = f"locale=en; __dcfduid={response.cookies.get('__dcfduid')}; __sdcfduid={response.cookies.get('__sdcfduid')}; __cfruid={response.cookies.get('__cfruid')}"
        return cookie
    except Exception as e:
        get_cookies(x, useragent)

def get_headers(token):
    x = fingerprints[random.randint(0, (len(fingerprints)-1))]['x-super-properties']
    useragent = fingerprints[random.randint(0, (len(fingerprints)-1))]['useragent']
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer':'https://discord.com',
        'sec-ch-ua': f'"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'cookie': get_cookies(x, useragent,),
        'sec-fetch-site': 'same-origin',
        'user-agent': useragent,
        'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjY3OTg3NTk0NjU5NzA1NjY4MyIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiIxMDM1ODkyMzI4ODg5NTk0MDM2IiwibG9jYXRpb25fY2hhbm5lbF90eXBlIjowfQ==',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-super-properties': x,
        'fingerprint': get_fingerprint()
        }
    return headers, useragent

def validateToken(token): # Checks if the token is valid
    client = requests.session()
    headers = {
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer':'https://discord.com',
        'sec-ch-ua': f'"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    client.headers.update(headers)

    if client.get(f'https://discord.com/api/v10/users/@me').status_code == 200:
        return True
    else:
        return False