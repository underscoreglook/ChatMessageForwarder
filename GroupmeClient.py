import flask
import requests
import yaml
from BaseClient import BaseClient

class GroupmeClient(BaseClient):
    def __init__(self, router):
        BaseClient.__init__(self, router)
        with open('config.yaml') as configFile:
            data = yaml.load(configFile, Loader=yaml.FullLoader)
            self.API_URL = data["groupme"]["apiUrl"]
            self.BOT_ID = data["groupme"]["botId"]

    def getTag(self):
        return "[G]"

    def usesFlask(self):
        return True

    def sendMessage(self, message):
        print("(GroupMe Received) " + message)
        payload = {
            'bot_id': self.BOT_ID,
            'text': message
        }
        response = requests.post(self.API_URL, json=payload)

    def setupFlask(self, app):
        @app.route("/groupme", methods=['GET', 'POST'])
        def groupmeWebhook():
            request = flask.request
            # Verify webhook
            if request.method == 'POST':
                payload = request.json
                if payload['sender_type'] == "user":
                    self.router.receiveMessage(self, payload['name'], payload['text'])

            # Just show success
            return "ok"

        print("GROUPME INITIALIZED")
        self.isReady = True
