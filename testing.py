#port knocking server using watchdog and scapy
#!/usr/bin/env python3

import os
import sys
import scapy.all as scapy
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import datetime

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_mod = datetime.datetime.now()

    def on_modified(self, event):
        if datetime.datetime.now() - self.last_mod < datetime.timedelta(seconds=1):
            return
        else:
            self.last_mod = datetime.datetime.now()
        print(event.event_type)
        if event.event_type == 'modified':
            #read the new line added to file
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    last_line = lines[-1]
                    print(last_line)
                    #parse the line
                    


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/var/log/firewall-droppd.log', recursive=False)
    observer.start()
    #if the file is modified, send a UDP packet to port 1000
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()