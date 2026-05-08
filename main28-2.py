import requests
import re
import time
import datetime
import telepot

telegram_id = '730238165'
my_token = '5400967414:AAEmAvwaQF6du8gny7A9upRniGvtHOi-Ro0'
 
bot = telepot.Bot(my_token)

def getWeather():
    url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000"
    response = requests.get(url)

    time = re.findall(r'<hour>(.+?)</hour>',response.text)
    temp = re.findall(r'<temp>(.+)</temp>',response.text)
    humi = re.findall(r'<reh>(.+?)</reh>',response.text)
    wfKor = re.findall(r'<wfKor>(.+?)</wfKor>',response.text)
    text = ""
    for i in range(8):
        text = text + "(" + str(time[i]) + "시 "
        text = text + str(temp[i]) + "C "
        text = text + str(humi[i]) + "% "
        text = text + str(wfKor[i]) + ")"
    
    return text

try:
    while True:
        now = datetime.datetime.now()
        hms = now.strftime('%H:%M:%S')
        print(hms)
        if hms == "20:15:50":
            msg = getWeather()
            print(msg)
            bot.sendMessage(chat_id = telegram_id, text = msg)
        
        time.sleep(1.0)
    
except KeyboardInterrupt:
    pass
