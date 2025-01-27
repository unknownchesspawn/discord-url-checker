import random
import string
import time
from datetime import datetime, timezone
import os
import webbrowser
import requests

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    BLUE = '[94m'
    GREEN = '[92m'
    YELLOW = '[93m'
    RED = '[91m'
    ENDC = '[0m'
    BOLD = '[1m'
    PURPLE = '[95m'
    CYAN = '[96m'

def open_discord_server():
    discord_link = 'discord.gg/W4FdvqFqnB'
    webbrowser.open(discord_link)
    print(f'{Colors.CYAN}[!] Opening support server...{Colors.ENDC}')
    time.sleep(1)

class VanityChecker:
    def __init__(self, webhook_url, length_choice):
        self.webhook_url = webhook_url
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.check_delay = 0.1
        self.length_choice = length_choice

    def generate_short_code(self):
        return ''.join((random.choice(string.ascii_lowercase) for _ in range(self.length_choice)))

    def double_check_vanity(self, code):
        try:
            url = f'https://discord.com/api/v9/invites/{code}'
            response = self.session.get(url)
            if response.status_code != 404:
                return {'available': False, 'code': code, 'reason': 'already_used'}
            else:
                return {'available': True, 'code': code}
        except Exception as e:
            return {'available': False, 'code': code, 'reason': str(e)}

    def send_webhook(self, vanity_data):
        if vanity_data['available']:
            webhook_data = {
                "content": f"New available vanity: discord.gg/{vanity_data['code']}",
                "username": "Vanity URL Checker",
                "embeds": [
                    {
                        "title": "New Available Vanity",
                        "description": f"Click here: [discord.gg/{vanity_data['code']}]",
                        "color": 5814783
                    }
                ]
            }
            response = self.session.post(self.webhook_url, json=webhook_data)
            if response.status_code == 204:
                print(f"{Colors.GREEN}[✓] Webhook sent successfully!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}[✖] Failed to send webhook.{Colors.ENDC}")
        else:
            print(f"{Colors.RED}[✖] Vanity not available, skipping webhook.{Colors.ENDC}")
        return

def print_banner():
    banner = f'\n{Colors.PURPLE}╔═══════════════════════════════════════════════╗\n║{Colors.CYAN}              AK URL CHECKER                 {Colors.PURPLE}║\n║{Colors.CYAN}         Created by: AK       {Colors.PURPLE}║\n║{Colors.GREEN}      Discord: discord.gg/W4FdvqFqnB    {Colors.PURPLE}║\n╚═══════════════════════════════════════════════╝{Colors.ENDC}\n    '
    print(banner)

def get_length_choice():
    print(f'{Colors.YELLOW}Choose URL length:')
    print(f'{Colors.CYAN}[1] {Colors.GREEN}Two characters')
    print(f'{Colors.CYAN}[2] {Colors.GREEN}Three characters')
    print(f'{Colors.CYAN}[3] {Colors.GREEN}Four characters{Colors.ENDC}')
    choice = input(f'{Colors.YELLOW}[>] {Colors.CYAN}Your choice: {Colors.ENDC}').strip()
    if choice in ['1', '2', '3']:
        return {'1': 2, '2': 3, '3': 4}[choice]

def main():
    clear()
    print_banner()
    open_discord_server()
    length_choice = get_length_choice()
    length_names = {2: 'two', 3: 'three', 4: 'four'}
    webhook_url = input(f'{Colors.YELLOW}[>] {Colors.CYAN}Enter Webhook URL: {Colors.ENDC}').strip()
    checker = VanityChecker(webhook_url, length_choice)
    checked = 0
    available = 0
    banned = 0
    print(f'\n{Colors.GREEN}[!] Starting search for {length_names[length_choice]}-character vanities')
    print(f'{Colors.BLUE}[!] Checking one vanity every 5 seconds')
    print(f'{Colors.PURPLE}════════════════════════════════════════════════{Colors.ENDC}\n')

    try:
        while True:
            vanity_code = checker.generate_short_code()
            result = checker.double_check_vanity(vanity_code)
            checked += 1

            if result and 'available' in result:
                if result['available']:
                    available += 1
                    checker.send_webhook(result)
                    print(f"\n{Colors.GREEN}[✓] AK: {Colors.BOLD}{result['code']}{Colors.ENDC}")
                    print(f"{Colors.CYAN}    URL: discord.gg/{result['code']}{Colors.ENDC}")
                else:
                    banned += 1

                print(f'{Colors.YELLOW}[~] Stats: Checked: {checked} | Available: {available} | Banned: {banned}{Colors.ENDC}')

            time.sleep(checker.check_delay)
            print('\r                                                  \r', end='')

    except KeyboardInterrupt:
        print(f'\n\n{Colors.PURPLE}════════════════════════════════════════════════')
        print(f'{Colors.GREEN}[!] Search stopped')
        print(f'{Colors.CYAN}[+] Total checked: {checked}')
        print(f'{Colors.CYAN}[+] Total available: {available}')
        print(f'{Colors.RED}[+] Total banned: {banned}')
        print(f'{Colors.BLUE}[!] AK © 2025{Colors.ENDC}')

if __name__ == '__main__':
    main()