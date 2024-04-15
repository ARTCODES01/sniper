import colorama, json, requests, threading, time, sys, os, winsound
from colorama import Fore, Back, Style
from modules import capmonster, invites, tokens, session

thread_lock = threading.Lock()
printNumber = 0

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
        global printNumber
        printNumber += 1

Console().clear()
printNumber += 1
token = input(f"{Fore.LIGHTBLACK_EX}{Console()._time()} |{Fore.RESET} {Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Paste your discord token: ")
Console().clear()
tokenHidden = ""
for i in range(len(token)):
    tokenHidden += "*"
print(f"{Fore.LIGHTBLACK_EX}{Console()._time()} |{Fore.RESET} {Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Paste your discord token: {tokenHidden}")
printNumber += 1
guildid = input(f"{Fore.LIGHTBLACK_EX}{Console()._time()} |{Fore.RESET} {Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Paste the id of the server you want to snipe the vanity on: ")
printNumber += 1
vanities = open("vanities.txt", "r").read().splitlines()
printNumber += 1
delay = input(f"{Fore.LIGHTBLACK_EX}{Console()._time()} |{Fore.RESET} {Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Type in the delay you would like to snipe at (in seconds): ")
printNumber += 1

token = tokens.formatToken(token)

if tokens.validateToken(token) == False:
    Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{printNumber}{Fore.WHITE}] {Fore.CYAN}Invalid token, please restart the program and try again.", False)
    time.sleep(5)
    sys.exit()

try:
    delay = int(delay)
except:
    Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{printNumber}{Fore.WHITE}] {Fore.CYAN}Invalid delay, please restart the program and try again.", False)
    time.sleep(5)
    sys.exit()

headers, _ = tokens.get_headers(token)
client = session.getTlsClient()
client.headers.update(headers)
response = client.get(f'https://discord.com/api/v10/guilds/{guildid}')
if response.status_code != 200:
    Console().sprint(f"{Fore.WHITE}({Fore.RED}+{Fore.WHITE}) [{Fore.RED}{printNumber}{Fore.WHITE}] {Fore.CYAN}Invalid guild id, please restart the program and make sure you are in the guild.", False)
    time.sleep(5)
    sys.exit()

snipedInvite = False

while snipedInvite == False:
    for vanity in vanities:
        req = client.get(f'https://discord.com/api/v10/invites/{vanity}?inputValue={vanity}&with_counts=true&with_expiration=true').text
        if 'type' in req:
            members = json.loads(req)['approximate_member_count']
            boosts = json.loads(req)['guild']['premium_subscription_count']
            if int(boosts) < 14:
                boosts = f"{boosts} (Partnered Server)"
            Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{printNumber}{Fore.WHITE}] {Fore.RED}{vanity} {Fore.CYAN}is taken {Fore.LIGHTBLACK_EX}| {Fore.CYAN}Members: {Fore.LIGHTBLACK_EX}{members} {Fore.CYAN}| Boosts: {Fore.LIGHTBLACK_EX}{boosts}", False)
        else:
            Console().sprint(f"{Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Vanity invite is avaliable, attempting to snipe...", True)
            request = client.patch(f'https://discord.com/api/v9/guilds/{guildid}/vanity-url', json={"code": vanity})
            if request.status_code == 200:
                snipedInvite = True
                Console().sprint(f"{Fore.WHITE}({Fore.GREEN}+{Fore.WHITE}) [{Fore.GREEN}{printNumber}{Fore.WHITE}] {Fore.CYAN}Successfully sniped vanity invite!", True)
                winsound.Beep(500, 1000)
                time.sleep(1)
                winsound.Beep(500, 1000)
                time.sleep(1)
                winsound.Beep(500, 1000)
                time.sleep(1)
                break
            else:
                Console().sprint(f"{Fore.WHITE}({Fore.RED}-{Fore.WHITE}) [{Fore.RED}{printNumber}{Fore.WHITE}] {Fore.CYAN}Failed to snipe vanity, please assure you have the correct permissions and that your server is level 3. A beep sound has been played to alert you of this.", False)
                winsound.Beep(500, 1000)
                time.sleep(1)
                winsound.Beep(500, 1000)
                time.sleep(1)
                winsound.Beep(500, 1000)
                time.sleep(1)

    time.sleep(int(delay))

input("\n\nPress enter to exit...")