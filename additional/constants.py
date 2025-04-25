from colorama import Fore
from additional.config import (
    THREADS,
    PROXY_ERR_LOG,
    DETAILED_EXCEPTION,
)

VIEWS_LIMIT = int(input(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET} Views amount: "))
POST_URL = str(input(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET} Post link (e.g https://t.me/telegram/3): "))

PROXIES = open('./inp/proxies.txt', 'r').read().splitlines()
CURRENT_VERSION = 1.01