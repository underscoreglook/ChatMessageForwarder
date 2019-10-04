from abc import ABC, abstractmethod
import Router

# The class that holds shared functionality for interfacing with chat services
class BaseClient(ABC):
    def __init__(self, router):
        if not isinstance(router, Router.Router):
            raise TypeError("client must be of type BaseClient")
        # FIXME: I'm afraid these two could be easily forgettable. Maybe think about alternative
        #   architecture that isn't so fragile.
        self.router = router # used for receiving msgs. Should use router.receiveMessage()
        self.isReady = False # once the client is ready, set this to True.

    @abstractmethod
    def getTag(self):
        """
        Returns a string that identifies all messages from this client.
        It is prepended to all messages coming from this client.
        """
        pass

    @abstractmethod
    def sendMessage(self, message):
        """
        Takes the message and sends it to the channel/chat room this client is connected to
        """
        pass

    @abstractmethod
    async def run(self):
        """
        Runs the logic of the client, typically an infinite loop.
        Should probably use asyncio.sleep to not burn the CPU.
        """
        pass
