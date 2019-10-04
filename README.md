# What is Chat Message Forwarder?
Chat Message Forwarder was made with this problem in mind:
* There are a lot of different chat clients, and everyone is spread between so many services, and it's annoying to manage them.
* While many have multiple clients installed, most only use a subset of the clients out there, and in many cases are unwilling to install another client, so if you have a group you want to start but not everyone has the same client, it can be impossible to do.

The way that this program goes about solving this is to link a chat room in each of the chat clients used together via message forwarder bots. So if a friend uses Hangouts and another uses Discord, you could create a chat group in hangouts, say "Hangouts Group", and a guild/server in Discord, say "Discord Group". Whenever someone types something in "Hangouts Group", it will send that message to "Discord Group" and vice versa.

This program was made with the Raspberry Pi in mind as the server that would run this 24/7, though it can run on any machine that is always on.

In addition, you'll need a bot on every chat client that has read/write access to the chat rooms you want to connect (see "Setup" section for the client).

# Supported Clients
* Discord
* Hangouts (Classic, uses headless Chrome)
* PLANNED: GroupMe
* MAYBE, DEPENDING ON API SUPPORT: Facebook Messenger

# Requirements
This was designed to run with Python 3.7. It also requires:
* asyncio (pip install asyncio)
* pyyaml (pip install pyyaml)
* discord.py (pip install -U discord.py)
* pyppeteer (pip install pyppeteer)

This was tested in Linux, though it should theoretically work on Windows and OSX, but I haven't personally spent time verifying it.

# Setup
This section contains sub sections for all the supported chat clients and how to set up the bot for that service, along with what part of the config you'll need to change.

In addition, in order for the program to work, you need to copy sample-config.yaml to config.yaml.

## Discord
* Go to the Discord Developer Portal: http://discordapp.com/developers/applications
* Log in
* Create an Application
* Create a Bot
* Add the Bot to your Guild/Server using the Oauth section.
* Give it read and message permissions.
* In config.yaml, fill in the information in the "discord" portion, including enable to true.
* See https://realpython.com/how-to-make-a-discord-bot-python/ for more info.

## Hangouts
* Create or reuse an existing Google account.
* Make sure that Google account is join into a particular Conversation.
* Go to config.yaml and type in the relevant information in the "hangouts" portion, including enable to true.
