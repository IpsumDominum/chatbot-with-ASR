import os
import sounddevice as sd
from asr.recognizer import Recognizer
from utils import Chatbot
import openai
#-------------------------
#Coqui-STT (Requires Download Model, See: https://stt.readthedocs.io/en/latest/DEPLOYMENT.html)
#rec = Recognizer("stt",os.path.join("asr","models","model.tflite"),sample_rate=16000)
#-------------------------

#-------------------------
#Vosk-API (Also Requires Downloading Model, See https://alphacephei.com/vosk/models)
rec = Recognizer("vosk",os.path.join("asr","models","small-model"),sample_rate=16000)
#-------------------------

#-------------------------
#Vosk-API but Partial Results
#rec = Recognizer("vosk-partial",os.path.join("asr","models","small-model"),sample_rate=16000)
#-------------------------
rec.recognize_from_microphone() #Is a thread

print("Microphone started")
#Might have to adjust samplerate if "input overflow" shows up. 
#set sample_rate = -1 for auto finding default sample rate

chatbot = Chatbot(API_KEY="") #Put your openai api key here for openai chatbot
while True:
    if(rec.stopped):
        break
    else:  
        next = " ".join(rec.get_next())
        if(next!=""):
            print("Human> "+next)                
            if("exit" in next.lower() or "quit" in next.lower() or "stop" in next.lower()):
                rec.stop()
            else:
                print("Skynet> "+chatbot.next_message(next).replace("\n",""))
