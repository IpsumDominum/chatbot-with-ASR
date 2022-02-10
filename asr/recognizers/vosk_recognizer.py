import sys
import os
import vosk
import time
from utils import BASE_DIR
#Disable vosk logging
from vosk import SetLogLevel
SetLogLevel(-1)
class VoskRecognizer():
    def __init__(self,model_path,sample_rate=44100,use_partial=False):        
        model_path = model_path
        self.model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(self.model,sample_rate)
        self.word_read_num = 0
        self.clear = False
        self.use_partial = use_partial
    def audio_to_words(self,audio):
        if self.rec.AcceptWaveform(audio):
            res = eval(self.rec.Result())["text"].split(" ")
            self.clear = True
        else:
            if(self.use_partial==True):
                res = eval(self.rec.PartialResult())["partial"].split(" ")
            else:
                res = []
        return res
    def inference(self,audio_data):
        words = self.audio_to_words(audio_data)
        #If only want the last partial words
        for token_loc,token in enumerate(words):
            if(token_loc>=self.word_read_num and token!=""):
                self.word_read_num +=1
        if(self.clear==True):
            self.word_read_num = 0
            self.clear = False
        return words
