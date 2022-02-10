from recognizers.vosk_recognizer import VoskRecognizer
from recognizers.stt_recognizer import STTRecognizer
from streams.microphone import Microphone
import queue
import threading
class Recognizer():
    def __init__(self,model_name,model_path,sample_rate=44100):
        self.mic = Microphone(sample_rate)
        if(model_name=="vosk"):
            self.model = VoskRecognizer(model_path,self.mic.sample_rate,use_partial=False)
        elif(model_name=="vosk-partial"):
            self.model = VoskRecognizer(model_path,self.mic.sample_rate,use_partial=True)
        elif(model_name=="stt"):
            self.model = STTRecognizer(model_path,self.mic.sample_rate)  
        else:            
            raise AttributeError("Please choose from:['vosk','vosk-partial','stt']")
        self.buffer = []
        self.stopped = False
    def recognize_from_microphone(self):
        def main_loop():                
            with self.mic.stream:
                while (True):
                    try:
                        audio_data = self.mic.next_data()
                        result = self.model.inference(audio_data)
                        if(len(result)>0):
                            self.buffer.append(result)
                        if(self.stopped==True):
                            break
                    except KeyboardInterrupt:
                        break
        self.stopped = False
        thread = threading.Thread(target=main_loop)
        thread.start()
    def get_next(self):
        if(len(self.buffer)>0):
            return self.buffer.pop()
        else:
            return ""
    def stop(self):
        self.stopped = True
