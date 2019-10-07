import asyncio
import flask
import requests
import threading
import yaml

from BaseClient import BaseClient

class FacebookClient(BaseClient):
    def __init__(self, router):
        BaseClient.__init__(self, router)
        with open('config.yaml') as configFile:
            data = yaml.load(configFile, Loader=yaml.FullLoader)
            self.API_URL = data["facebook"]["apiUrl"]
            self.VERIFY_TOKEN = data["facebook"]["verifyToken"]
            self.PAGE_ACCESS_TOKEN = data["facebook"]["pageAccessToken"]
            self.users = data["facebook"]["users"]

    def getTag(self):
        return "[F]"

    def sendMessage(self, message):
        print("(Facebook Received) " + message)
        for fbId in self.users:
            self.sendToSpecificUser(fbId, message)

    def sendToSpecificUser(self, fbId, message):
        payload = {
            'message': {
                'text': message
            },
            'recipient': {
                'id': fbId
            },
            'notification_type': 'regular'
        }
        auth = {
            'access_token': self.PAGE_ACCESS_TOKEN
        }
        response = requests.post(
            self.API_URL,
            params=auth,
            json=payload
        )

    async def run(self):
        app = flask.Flask(__name__)

        def isUserMessage(message):
            """Check if the message is a message from the user"""
            print(message)
            return (message.get('message') and
                    message['message'].get('text') and
                    not message['message'].get("is_echo"))

        @app.route("/fb_webhook", methods=['GET', 'POST'])
        def listen():
            request = flask.request
            # Verify webhook
            if request.method == 'GET':
                if request.args.get("hub.verify_token") == self.VERIFY_TOKEN:
                    return request.args.get("hub.challenge")
                else:
                    return "incorrect"

            # HAndle messages
            if request.method == 'POST':
                payload = request.json
                event = payload['entry'][0]['messaging']
                for x in event:
                    if isUserMessage(x):
                        text = x['message']['text']
                        senderId = x['sender']['id']
                        senderName = self.users[str(senderId)]
                        print(f"Facebook message recieved -- {senderName} ({senderId}): {text}")
                        # Send to other fb users
                        fbMsg = senderName + ": " + text
                        for fbId in self.users:
                            print("* Compare " + str(fbId) + " to " + str(senderId))
                            if fbId != str(senderId):
                                self.sendToSpecificUser(fbId, fbMsg)
                        # Send to other clients
                        self.router.receiveMessage(self, senderName, text)

            # Just show success
            return "ok"

        def startApp(flaskApp):
            flaskApp.run()

        appThread = threading.Thread(target=startApp, args=(app,))
        appThread.daemon = True
        appThread.start()
        print("FACEBOOK READY")
        self.isReady = True
