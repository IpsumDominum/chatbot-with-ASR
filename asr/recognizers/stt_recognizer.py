import sys
import os
import numpy as np
from stt import Model, version
from utils import BASE_DIR

class STTRecognizer():
    def __init__(self,model_path,sample_rate=44100):        
        model_path = model_path
        self.model = Model(model_path)
        self.sample_rate = self.model.sampleRate()
        if(sample_rate!=self.sample_rate):
            print("Warning: Model's original trained sample rate ({}) is different than {}hz.".format(
                self.sample_rate,sample_rate
            ),file=sys.stderr)
    def inference(self,audio_data):
        audio_data = np.frombuffer(audio_data,dtype=np.int16)
        transcript = self.model.sttWithMetadata(audio_data, 1).transcripts[0]
        _,words_list_raw = self.words_from_candidate_transcript(transcript)
        return words_list_raw
    def words_from_candidate_transcript(self,metadata):
        word = ""
        word_list_with_duration = []
        word_list_raw = []
        word_start_time = 0
        # Loop through each character
        for i, token in enumerate(metadata.tokens):
            # Append character to word if it's not a space
            if token.text != " ":
                if len(word) == 0:
                    # Log the start time of the new word
                    word_start_time = token.start_time

                word = word + token.text
            # Word boundary is either a space or the last character in the array
            if token.text == " " or i == len(metadata.tokens) - 1:
                word_duration = token.start_time - word_start_time

                if word_duration < 0:
                    word_duration = 0
                each_word = dict()
                each_word["word"] = word
                each_word["start_time"] = round(word_start_time, 4)
                each_word["duration"] = round(word_duration, 4)
                word_list_with_duration.append(each_word)
                word_list_raw.append(word)
                # Reset
                word = ""
                word_start_time = 0
        return word_list_with_duration,word_list_raw