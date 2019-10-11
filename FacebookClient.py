import flask
import requests
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

    def usesFlask(self):
        return True

    def sendMessage(self, message):
        print("(Facebook Received) " + message)
        for fbId in self.users:
            self.sendToSpecificUser(fbId, message)

    def sendToSpecificUser(self, psId, message):
        payload = {
            'message': {'text': message},
            'recipient': {'id': psId},
            'notification_type': 'regular'
        }
        auth = {'access_token': self.PAGE_ACCESS_TOKEN}
        response = requests.post(self.API_URL, params=auth, json=payload)

    def setupFlask(self, app):
        def isUserMessage(message):
            """Check if the message is a message from the user"""
            print(message)
            return (message.get('message') and
                    message['message'].get('text') and
                    not message['message'].get("is_echo"))

        @app.route("/fb_webhook", methods=['GET', 'POST'])
        def facebookWebhook():
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
                        senderId = str(x['sender']['id'])
                        if senderId not in self.users:
                            print("\nFACEBOOK SENDER ID NOT FOUND: " + senderId + ": " + text + "\n")
                            f=open("facebookPsIds.txt", "a+")
                            f.write(senderId + ": " + text)
                            f.close()
                            continue
                        senderName = self.users[senderId]
                        print(f"Facebook message recieved -- {senderName} ({senderId}): {text}")
                        # Send to other fb users
                        fbMsg = senderName + ": " + text
                        for psId in self.users:
                            print("* Compare " + str(psId) + " to " + senderId)
                            if psId != str(senderId):
                                self.sendToSpecificUser(psId, fbMsg)
                        # Send to other clients
                        self.router.receiveMessage(self, senderName, text)

            # Just show success
            return "ok"

        print("FACEBOOK INITIALIZED")
        self.isReady = True
