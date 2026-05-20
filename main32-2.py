import speech_recognition as sr
import requests
import re
import os
import time

url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000"

def speak(option, msg) :
    os.system("espeak {} '{}'".format(option,msg))

try:
    while True :
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            
        try:
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.")
                response = requests.get(url)
                temp = re.findall(r'<temp>(.+)</temp>',response.text)
                humi = re.findall(r'<reh>(.+)</reh>',response.text)
                
                msg = '    기온은 ' + temp[0].split('.')[0] + '도 습도는 ' + humi[0] + '퍼센트 입니다'
                
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option,msg)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass
