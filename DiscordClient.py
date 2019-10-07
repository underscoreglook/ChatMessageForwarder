import asyncio
import discord
import yaml

from BaseClient import BaseClient

class DiscordClient(discord.Client, BaseClient):
    def __init__(self, router):
        BaseClient.__init__(self, router)
        discord.Client.__init__(self)
        self.guild = {}
        self.channel = {}
        self.eventLoop = asyncio.get_event_loop()
        with open('config.yaml') as configFile:
            data = yaml.load(configFile, Loader=yaml.FullLoader)
            self.TOKEN = data["discord"]["token"]
            self.GUILD_NAME = data["discord"]["guild"]
            self.CHANNEL_NAME = data["discord"]["channel"]

    def getTag(self):
        return "[D]"

    def sendMessage(self, message):
        asyncio.run_coroutine_threadsafe(
            self.channel.send(message), self.eventLoop)
        print("(Discord Sent) " + message)

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=self.GUILD_NAME)
        print(
            'DISCORD ON READY\n'
            f'{self.user} is connected to the following guild:\n'
            f'{self.guild.name}(id: {self.guild.id})'
        )
        self.channel = discord.utils.get(self.guild.text_channels, name=self.CHANNEL_NAME)
        self.isReady = True

    async def on_message(self, message):
        if message.author == self.user:
            return;
        name = message.author.nick or message.author.name
        print(f"(Discord Thread) {name}: {message.content}")
        self.router.receiveMessage(self, name, message.content)

    async def run(self):
        asyncio.ensure_future(self.start(self.TOKEN))
