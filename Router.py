import asyncio
from queue import Queue;
import BaseClient

LOOP_INTERVAL = 1

class Router:
    def __init__(self):
        self.messageQueue = Queue()
        self.clients = []
        self.isReady = False

    def addClient(self, client):
        if not isinstance(client, BaseClient.BaseClient):
            raise TypeError("client must be of type BaseClient")
        self.clients.append(client)

    def receiveMessage(self, client, author, message):
        """
        When a client recieves a message, it should call this
        so it can be broadcast out.
        """
        if not isinstance(client, BaseClient.BaseClient):
            raise TypeError("client must be of type BaseClient")
        if not isinstance(author, str) or not isinstance(message, str):
            raise TypeError("author and message must be strings")
        fullMessage = client.getTag() + " " + author + ": " + message
        self.messageQueue.put(fullMessage)
        print("Router, Received: " + fullMessage)

    async def run(self):
        """
        Checks the message queue and broadcasts to the other clients
        """
        # First, check if all clients are ready
        while not self.isReady:
            await asyncio.sleep(LOOP_INTERVAL)
            if not self.isReady:
                self.isReady = True
                for client in self.clients:
                    if not client.isReady:
                        self.isReady = False
                        break
        print("***All clients ready!***")
        # Manage the message queue
        while True:
            await asyncio.sleep(LOOP_INTERVAL)
            while not self.messageQueue.empty():
                message = self.messageQueue.get()
                for client in self.clients:
                    if not message.startswith(client.getTag()):
                        client.sendMessage(message)

    def start(self):
        tasks = []
        for client in self.clients:
            tasks.append(client.run())
        loop = asyncio.get_event_loop()
        groups = asyncio.gather(*tasks, self.run())
        loop.run_until_complete(groups)
