import requests
import telepot as tp
from datetime import date

class Chat_Bot():
    def __init__(self, usrID, token):
        self.bot = tp.Bot(token)
        self.usrID = usrID
        self.token = token

    def sendMSG(self, msg):
        self.bot.sendMessage(chat_id=self.usrID, text=msg)    

    def sendPhoto(self, photo_loc):
        self.bot.sendPhoto(chat_id=self.usrID, photo=open(photo_loc, "rb"))

if __name__ == "__main__":
    #Main is used for testing the messaging system
    cb = Chat_Bot()
    today = date.today()
    message = f'date today is {today}'
    photo="bill.jpg"

    cb.sendMSG(message)
    cb.sendPhoto(photo)
    
