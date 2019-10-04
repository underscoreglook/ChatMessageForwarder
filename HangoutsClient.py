import asyncio
import threading
import yaml
from pyppeteer import launch
from queue import Queue

from BaseClient import BaseClient

async def getAttr(element, attribute):
    property = await element.getProperty(attribute)
    return await property.jsonValue()

async def getText(element):
    return await getAttr(element, "innerText")

async def getId(element):
    return await getAttr(element, "id")

class HangoutsClient(BaseClient):
    def __init__(self, router):
        BaseClient.__init__(self, router)
        self.outgoingMessages = Queue()
        with open('config.yaml') as configFile:
            data = yaml.load(configFile, Loader=yaml.FullLoader)
            self.LOOPTIME = data["hangouts"]["loopTime"]
            self.USERNAME = data["hangouts"]["username"]
            self.PASSWORD = data["hangouts"]["password"]
            self.CHATNAME = data['hangouts']['chatName']

    def getTag(self):
        return "[H]"

    def sendMessage(self, message):
        self.outgoingMessages.put(message)
        print("(Hangouts Received) " + message)

    async def run(self):
        print("Hangouts Client Start Init")

        # First, start browser and get to login
        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
        page = await browser.newPage()
        await page.goto('https://hangouts.google.com')
        await page.click("a.gb_de.gb_1.gb_pb")

        # Next, log in
        await page.type("input[type=email]", self.USERNAME)
        await page.keyboard.press('Enter')
        await page.waitForSelector("input[type=password]")
        await page.type("input[type=password]", self.PASSWORD)
        await page.keyboard.press('Enter')
        await page.waitForSelector('#hangout-landing-chat-moles')
        await page.waitFor(5000)

        # Next, open the chat room
        chatRoomSelectorFrame = None
        for frame in page.mainFrame.childFrames:
            if frame.url.startswith("https://hangouts.google.com/webchat/frame3?"):
                chatRoomSelectorFrame = frame
                break
        frameContents = await chatRoomSelectorFrame.content()
        index = frameContents.find(">" + self.CHATNAME + "<")
        index = frameContents.rfind('id="', 0, index)
        endIndex = frameContents.find('"', index + 5)
        id = frameContents[index + 4: endIndex]
        await chatRoomSelectorFrame.click('*[id="' + id + '"]')
        await page.waitFor(5000)

        # Get the correct iFrame for the chat room
        chatRoomFrame = None
        for frame in page.mainFrame.childFrames:
            if frame.url.startswith("https://hangouts.google.com/webchat/frame3?"):
                if not frame == chatRoomSelectorFrame:
                    chatRoomFrame = frame
                    break

        # Then, get all of the dom elements we need,
        chatInput = await chatRoomFrame.J(".editable")
        chatRoom = await chatRoomFrame.J("div.fkp8p")

        # Lastly, grab the initial state of the chat room
        lastChatMessage = (await chatRoom.JJ("span.tL8wMe.EMoHub"))[-1]

        self.isReady = True
        print("Hangouts Client Finish Init")

        while True:
            await asyncio.sleep(self.LOOPTIME)

            # First, send any outgoing messages
            messageToSend = ""
            while not self.outgoingMessages.empty():
                if messageToSend:
                    messageToSend = messageToSend + "\n" + self.outgoingMessages.get()
                else:
                    messageToSend = self.outgoingMessages.get()
            if messageToSend:
                print("Hangouts Sending Message:\n=============\n" + messageToSend + "\n=========")
                await chatInput.type(messageToSend[:1500])
                await chatInput.press('Enter')

            # Next, check to see if the last message is new, and loop if same
            lastChatMessageId = await getId(lastChatMessage)
            chatMessages = await chatRoom.JJ("span.tL8wMe.EMoHub")
            currentMessage = chatMessages[-1]
            currentMessageId = await getId(currentMessage)
            if lastChatMessageId == currentMessageId:
                continue

            # Otherwise, grab all of the new messages since last time in a stack
            newMessages = []
            while len(chatMessages) > 0:
                currentMessage = chatMessages.pop()
                currentMessageId = await getId(currentMessage)
                if currentMessageId != lastChatMessageId:
                    newMessages.append(currentMessage)
                else:
                    break

            # Now that we have the new messages
            while len(newMessages) > 0:
                lastChatMessage = newMessages.pop() # Side benefit:
                #   This also sets lastChatMessage when we're done to latest message

                # Now get the author (do some funky dom navigation)
                parentElement = await lastChatMessage.Jx("../../../..")
                parentElement = parentElement[0]
                imgElement = await parentElement.J('img')
                if not imgElement:
                    continue # If there's no image, we sent this message
                author = await getAttr(imgElement, "alt")

                # Lastly, broadcast the full message
                self.router.receiveMessage(self, author, await getText(lastChatMessage))
