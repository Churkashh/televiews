# github.com/Churkashh

import tls_client
import threading
import ctypes
import random
import time
import os

from urllib.parse import urlparse
from loguru import logger
from colorama import Fore

from additional.constants import (
    DETAILED_EXCEPTION,
    CURRENT_VERSION,
    PROXY_PER_VIEW,
    REMOVE_PROXIES,
    PROXY_ERR_LOG,
    VIEWS_LIMIT,
    POST_URL,
    PROXIES,
    THREADS
)


threads_working = True
main_threads = []
threads_num = 0

if os.name == "nt":
    CMD = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.SetWindowLongW(CMD, -16, ctypes.windll.user32.GetWindowLongW(CMD, -16) | 0x80000)
    ctypes.windll.user32.SetLayeredWindowAttributes(CMD, 0, 235, 0x2)
    os.system("cls")
    print("# github.com/Churkashh")
    time.sleep(0.5)
    os.system("cls")

def fetch_session() -> tls_client.Session:
    """Fetch tls-client session"""
    session = tls_client.Session(client_identifier='firefox_120', random_tls_extension_order=True)
    session.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
    }
    
    return session

def parse_post_url(url: str) -> tuple:
    """Parse telegram channel post url"""
    parts = urlparse(url).path.strip('/').split('/')
    channel_name = parts[0]
    post_id = parts[1]
    return channel_name, post_id


class Statistics:
    """Views statistics"""
    views = 0
    fails = 0
    
class Utils:
    @staticmethod
    def title_worker():
        """Set title name"""
        if os.name == 'nt':
            while threads_working:
                title = f"v{CURRENT_VERSION} TeleViews (github.com/Churkashh) | Views sent: {Statistics.views} ~ Fails: {Statistics.fails} | github.com/Churkashh"
                ctypes.windll.kernel32.SetConsoleTitleW(title)
                time.sleep(3)
    
    @staticmethod
    def file_worker():
        if REMOVE_PROXIES:
            while threads_working:
                time.sleep(5)
                with open("./inp/proxies.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(PROXIES))
                    
    @staticmethod
    def get_proxy():
        if not PROXIES:
            return None
        
        if PROXY_PER_VIEW:
            return PROXIES.pop(random.randrange(len(PROXIES)))
        
        else:
            return random.choice(PROXIES)

class TeleViews():
    def __init__(self, thread_id: int) -> None:
        self.__session = fetch_session()
        self.__thread_id = f"Thread-{thread_id}"

    def sendView(self, channel_name: str, post_id: str) -> None:
        """Send a view to the post in the channel"""
        proxy = Utils.get_proxy()
        if not proxy:
            logger.error(f"[{self.__thread_id}] No proxies left")
            return
        
        self.__session.proxies = f"http://{proxy}"
        
        url = f"https://t.me/{channel_name}/{post_id}"
        self.__session.headers["referer"] = url
        
        while True:
            try:
                params = {
                    'embed': '1',
                    'mode': 'tme',
                }
                
                resp = self.__session.get(
                    url,
                    params=params,
                )
                
                data_view = str(resp.text).split('data-view="')[1].split('"')[0] if 'data-view="' in resp.text else None
                if resp.status_code != 200 or not data_view:
                    Statistics.fails += 1
                    logger.error(f"[{self.__thread_id}] Failed to fetch post data ({resp.status_code}) -> {resp.text}")
                    return
                
                break
            except Exception as e:
                proxy_change = self.__handle_exception(str(e))
                if proxy_change:
                    proxy = Utils.get_proxy()
                    if not proxy:
                        logger.error(f"[{self.__thread_id}] No proxies left")
                        return
                    
                    self.__session.proxies = f"http://{proxy}"
                
        self.__session.headers["referer"] = f"https://t.me/{channel_name}/{post_id}?embed=1&mode=tme"
        url = "https://t.me/v/"
        
        while True:
            try:
                params = {
                    'views': data_view,
                }

                resp = self.__session.get(
                    url,
                    params=params,
                    headers={
                        "X-Requested-With": "XMLHttpRequest"
                    }
                )
                
                if resp.status_code != 200:
                    Statistics.fails += 1
                    logger.error(f"[{self.__thread_id}] Failed to send view ({resp.status_code}) -> {resp.text}")
                    return
                
                break
            except Exception as e:
                proxy_change = self.__handle_exception(str(e))
                if proxy_change:
                    proxy = Utils.get_proxy()
                    if not proxy:
                        logger.error(f"[{self.__thread_id}] No proxies left")
                        return
                    
                    self.__session.proxies = f"http://{proxy}"
        
        Statistics.views += 1
        logger.success(f"[{self.__thread_id}] Succesfully sent a view to the post {Fore.LIGHTBLACK_EX}| {Fore.LIGHTBLACK_EX}Total={Fore.RESET}{Statistics.views}")
        
        
    
    def __handle_exception(self, exception: str) -> None:
        """Exception handler"""
        if "Proxy" in exception:
            if PROXY_ERR_LOG:
                logger.error(f"[{self.__thread_id}] Proxy error -> {exception}")
            
            return True
        
        if DETAILED_EXCEPTION:
            logger.exception(f"Failed to send request (Exception) -> {exception}")
            
        else:
            logger.error(f"[{self.__thread_id}] Failed to send request (Exception) -> {exception}")
            
        return False
            

def worker(channel_name: str, post_id: str) -> None:
    """Threads worker"""
    global threads_num
    while threads_num - Statistics.fails < VIEWS_LIMIT:
        threads_num += 1
        TeleViews(threads_num).sendView(channel_name, post_id)
        
def main() -> None:
    """Main function"""
    global threads_working
    
    try:
        channel_name, post_id = parse_post_url(POST_URL)
        
        threading.Thread(target=Utils.title_worker).start()
        threading.Thread(target=Utils.file_worker).start()
        for _ in range(THREADS):
            thread = threading.Thread(target=worker, args=(channel_name, post_id))
            main_threads.append(thread)
            thread.start()
        
        while threads_num - Statistics.fails < VIEWS_LIMIT:
            time.sleep(5)
            
        for thread in main_threads:
            thread.join()
        
        threads_working = False
        
        print()
        input(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET} Views sent: {Statistics.views} ~ Fails: {Statistics.fails}...")
        os._exit(1)
        
    except Exception as exc:
        logger.exception(f"Main Exception -> {exc}")
        
if __name__ == "__main__":
    main()
    
# github.com/Churkashh
