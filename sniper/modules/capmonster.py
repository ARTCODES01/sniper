from colorama import Style
import discord, datetime, time, flask, requests, json, threading, os, random, httpx, tls_client, sys, base64
from flask import request
from pathlib import Path
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
if os.name == 'nt':
    import ctypes

app = flask.Flask(__name__)

class getBalance():
    r"""Returns the balance of the account in dollars.

     Parameters
     ----------
     >>> apikey : str

     Returns
     -------
     >>> balance : float
     >>> errorId : int
     >>> errorCode : str
     """

    def __init__(self, apikey=None):
        if apikey == None:
            raise Exception("No API Key was provided, get one at https://capmonster.cloud/en/")
            
        self.payload = {"clientKey": apikey}
        self.response = requests.post("https://api.capmonster.cloud/getBalance", json=self.payload)

        self.response = self.response.json()

        try:
            self.balance = float(self.response["balance"])
        except:
            self.balance = "No balance returned."

        try:
            self.errorId = int(self.response["errorId"])
        except:
            self.errorId = "No errorId returned."

        try:
            self.errorCode = str(self.response["errorCode"])
        except:
            self.errorCode = "No errorCode returned."

        self.url = "https://api.capmonster.cloud/getBalance"

def solveCaptcha(rqdata: str, site_key: str, websiteURL: str, useragent: str, capmonster_key: str):

    task_payload = {
        'clientKey': capmonster_key,
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
            'clientKey': capmonster_key,
            'taskId': task_id,
        }
        

        while key is None:
            response = client.post("https://api.capmonster.cloud/getTaskResult", json = get_task_payload).json()
            try:
                if response['status'] == "ready":
                    key = response["solution"]["gRecaptchaResponse"]
                else:
                    time.sleep(1)
            except:
                print(response)
            
    return key