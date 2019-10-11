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
* Facebook Messenger
* PLANNED: GroupMe

# Requirements
This was designed to run with Python 3.7. It also requires:
* asyncio (pip install asyncio)
* pyyaml (pip install pyyaml)
* discord.py (pip install -U discord.py)
* pyppeteer (pip install pyppeteer)
* flask (pip install -U Flask)
* ngrok (http://ngrok.com)

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

## Facebook Messenger
* If you don't have an FB App already, go through the Test drive here: https://developers.facebook.com/docs/messenger-platform/getting-started/test-drive
* You should now have everything already set up. Now, set up config.yaml:
** enabled: true
** apiUrl: Shouldn't change
** verifyToken: Put in some arbitrary string here
** pageAccessToken: This can be found in developers.facebook.com, go to your app, go to Messenger->Settings, then go to "Access Tokens" and click "Generate Token".
** users: This is a dictionary between psId and the name of the user. Put in as many as want to be part of the group. They will also be have to be set up as "Testers" in your app (go to Roles -> Roles in the app page). The psId is not easily gettable, so the console will print this out, along with a file "facebookPsIds.txt" being created for messages sent with psIds we don't have info for.
* Start the program. The Facebook Messanger will automatically start Flask on port 5000.
* Start ngrok server in terminal with "ngrok http 5000". When it starts, note the https Forwarding address. Keep ngrok running.
* Back in Facebook's developer page (Messenger -> Set Up), go to Webhooks, and add the forwarding url + "fb_webhook". I.E. "https://c29387597285379327573275.ngrok.io/fb_webhook"
* The verify token should be the arbitrary string you put in the config.yaml.
* (Note: Verifying the webhook needs to be done every time the ngrok url changes, such as on computer/server restart)
* It should verify the new webhook and messages should be sending and receiving.
* Give the Messenger link or page link to anyone who wants to join, and get their FB ID. Add them as testers and add them to the config. Remember that fbIds have to be strings in the config.
