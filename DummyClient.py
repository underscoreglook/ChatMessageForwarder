import asyncio
import random
import string
import threading
import yaml
from BaseClient import BaseClient

class DummyClient(BaseClient):
    def __init__(self, router):
        BaseClient.__init__(self, router)
        with open('config.yaml') as configFile:
            data = yaml.load(configFile, Loader=yaml.FullLoader)
            self.SEND_EVERY_SECONDS = data["dummy"]["sendEverySeconds"]
        self.isReady = True
        print("DUMMY CLIENT INITIALIZED")

    def getTag(self):
        return "[_]"

    def sendMessage(self, message):
        print(
            '========================\n'
            'DUMMY MESSAGE Received: ' + message +
            '\n========================\n'
        )

    async def run(self):
        """
        Every however many seconds, we "send a message" every self.SEND_EVERY_SECONDS
        """
        if self.SEND_EVERY_SECONDS < 0:
            return
        while True:
            await asyncio.sleep(self.SEND_EVERY_SECONDS)
            author = ''.join([random.choice(string.ascii_letters) for n in range(8)])
            content = ''.join([random.choice(string.ascii_letters) for n in range(40)])
            self.router.receiveMessage(self, author, content)
