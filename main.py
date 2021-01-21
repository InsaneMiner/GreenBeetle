#cython: language_level=3
import time 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler 
import multiprocessing
import sys
import subprocess
import config.config
import libs.colors
import libs.logging
import socket
def request_self():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client.connect((config.config.HOST,config.config.PORT))  
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % config.config.ALLOWED_HOSTS[0]
    client.send(request.encode())  
    response = client.recv(4096)  
def current_url():
    if config.config.PORT == 80:
        print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.cyan}Server address: {libs.colors.colors.fg.yellow}http://localhost/{libs.colors.colors.reset}")
    else:
        print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.cyan}Server address: {libs.colors.colors.fg.yellow}http://localhost:{str(config.config.PORT)}/{libs.colors.colors.reset}")
process = None
def restart_server():
    kill_processes()
    start_server()
def start_server():
    global process
    process = subprocess.Popen(['python3', 'main.py', 'server_no_watchdog'])
def kill_processes():
    global process
    process.kill() 
class OnMyWatch: 
    # Set the directory on watch 
    watchDirectory = "pages"
  
    def __init__(self): 
        self.observer = Observer() 
  
    def run(self): 
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(1)
                if process.poll() != None:
                    sys.exit() 
        except: 
            self.observer.stop() 
        self.observer.join() 
class Handler(FileSystemEventHandler):  
    @staticmethod
    def on_any_event(event): 
        if event.is_directory: 
            return None
  
        elif event.event_type == 'created': 
            pass
        elif event.event_type == 'modified':
            restart_server()
if __name__ == '__main__': 
    if len(sys.argv) < 2:
        libs.logging.notice("Starting Watchdog\n")
        libs.logging.notice("Starting Server\n")
        start_server()
        current_url()
        watch = OnMyWatch() 
        watch.run() 
    else:
        if sys.argv[1] == "server_no_watchdog":
            import lemon.lemon
        else:
            libs.logging.error("Error: This is not a useless run\n")
            libs.logging.good("Shutting Down\n")
            sys.exit()