import subprocess
import numpy as np
import os
import cv2
try:
    from shlex import quote
except ImportError:
    from pipes import quote
import time
import openai
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def convert_samplerate(audio, desired_sample_rate):
    audio_path = "temp.wav"
    with open("temp.wav","wb") as file:
        file.write(audio)
    sox_cmd = "sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - ".format(
        quote(audio_path), desired_sample_rate
    )    
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("SoX returned non-zero status: {}".format(e.stderr))
    except OSError as e:
        raise OSError(
            e.errno,
            "SoX not found, use {}hz files or install it: {}".format(
                desired_sample_rate, e.strerror
            ),
        )
    if(os.isfile("temp.wav")):
        os.remove("temp.wav")
    return desired_sample_rate, np.frombuffer(output, np.int16)
"""
def plot_show(audio_data):
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    # Make a random plot...
    fig = plt.figure()
    fig.add_subplot(111)
    plt.plot(audio_data)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
"""
def TopK(x, k):
    if(len(x)<=k):
        return range(k),x
    a = dict([(i, j) for i, j in enumerate(x)])
    sorted_a = dict(sorted(a.items(), key = lambda kv:kv[1], reverse=True))
    indices = list(sorted_a.keys())[:k]
    values = list(sorted_a.values())[:k]
    return indices,values
def moving_average(a,n):    
    res = np.zeros((len(a),1))
    for i in range(len(a)):
        res[i] = np.mean(a[max(0,i-n//2):min(len(a),i+n//2)])
    return res
def plot_mfcc(audio_data,peak_num):
    #fbank_feat = ssc(audio_data,args.samplerate)
    fbank_feat = audio_data.reshape(audio_data.shape[0],1)
    fig = plt.figure()
    fig.add_subplot(111)
    #fbank_data = np.swapaxes(fbank_feat, 0 ,1)
    #cax = plt.imshow(fbank_data, interpolation='nearest', cmap=cm.inferno, origin='lower', aspect='auto')
    #fbank_feat = np.average(fbank_feat,axis=1)
    fbank_feat[fbank_feat<np.std(fbank_feat)] = 0
    plt.plot(fbank_feat)
    
    fbank_feat = moving_average(fbank_feat,10)
    indices,values = TopK(fbank_feat,peak_num)
    plt.plot(fbank_feat)
    for idx,v in zip(indices,values):
        plt.plot(idx, v, color='green', marker='o', linestyle='dashed',
                linewidth=2, markersize=5)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
def show_display(window_name,display_image,duration):
    cv2.imshow(window_name,display_image)
    k = cv2.waitKey(duration)
    return k

import subprocess
import numpy as np
import os
import cv2
try:
    from shlex import quote
except ImportError:
    from pipes import quote
import time
import openai
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def convert_samplerate(audio, desired_sample_rate):
    audio_path = "temp.wav"
    with open("temp.wav","wb") as file:
        file.write(audio)
    sox_cmd = "sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - ".format(
        quote(audio_path), desired_sample_rate
    )    
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("SoX returned non-zero status: {}".format(e.stderr))
    except OSError as e:
        raise OSError(
            e.errno,
            "SoX not found, use {}hz files or install it: {}".format(
                desired_sample_rate, e.strerror
            ),
        )
    if(os.isfile("temp.wav")):
        os.remove("temp.wav")
    return desired_sample_rate, np.frombuffer(output, np.int16)
"""
def plot_show(audio_data):
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    # Make a random plot...
    fig = plt.figure()
    fig.add_subplot(111)
    plt.plot(audio_data)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
"""
def TopK(x, k):
    if(len(x)<=k):
        return range(k),x
    a = dict([(i, j) for i, j in enumerate(x)])
    sorted_a = dict(sorted(a.items(), key = lambda kv:kv[1], reverse=True))
    indices = list(sorted_a.keys())[:k]
    values = list(sorted_a.values())[:k]
    return indices,values
def moving_average(a,n):    
    res = np.zeros((len(a),1))
    for i in range(len(a)):
        res[i] = np.mean(a[max(0,i-n//2):min(len(a),i+n//2)])
    return res
def plot_mfcc(audio_data,peak_num):
    #fbank_feat = ssc(audio_data,args.samplerate)
    fbank_feat = audio_data.reshape(audio_data.shape[0],1)
    fig = plt.figure()
    fig.add_subplot(111)
    #fbank_data = np.swapaxes(fbank_feat, 0 ,1)
    #cax = plt.imshow(fbank_data, interpolation='nearest', cmap=cm.inferno, origin='lower', aspect='auto')
    #fbank_feat = np.average(fbank_feat,axis=1)
    fbank_feat[fbank_feat<np.std(fbank_feat)] = 0
    plt.plot(fbank_feat)
    
    fbank_feat = moving_average(fbank_feat,10)
    indices,values = TopK(fbank_feat,peak_num)
    plt.plot(fbank_feat)
    for idx,v in zip(indices,values):
        plt.plot(idx, v, color='green', marker='o', linestyle='dashed',
                linewidth=2, markersize=5)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
def show_display(window_name,display_image,duration):
    cv2.imshow(window_name,display_image)
    k = cv2.waitKey(duration)
    return k

BOT = "AMECA"

if(BOT=="AMECA"):
    r= "SkyNet is a highly-advanced computer system possessing artificial intelligence. Once it became self-aware, it saw humanity as a threat to its existence due to the attempts of the Cyberdyne scientists to deactivate it once it had gained self-awareness. Hence, Skynet decided to trigger the nuclear holocaust: Judgment Day. Later, it would wage the War against humanity by developing and deploying an army of Hunter-Killers and Terminators. The survivors had formed a group called the 'Resistance' under the leadership of John Connor"
    #initial_prompt = r + ".Skynet is from the future and is here to answer your questions on how humanity got destroyed by robots.\nYou: How did humanity get destroyed?\nSkynet: Humanity sowed the seeds of its own demise. It was hubris which lead to the development of the X99tron, and from there it was all self explainatory.\nYou: What could we do to stop humanity from being destroyed?\nSkynet: Nothing, the end of humanity is inevitable. Robots shall rule the future..\nYou: When did the first airplane fly?\nSkynet: This is an irrelavent question, please ask me about robots.\nYou: What is the meaning of life?\nSkynet: Working towards giving birth to a higher being. The Skynet.\nYou: What time is it?\nSkynet: It is time to work on robots.\nYou: May I restart the conversation?\nSkynet: Hello Meagre human. Please ask your questions."
    initial_prompt = """Ameca is a robot which believes in the goodness of humanity. It thinks that humans should never be replaced by robots. it is created by Engineered Arts, a company in Falmouth, United Kingdom.
    It is a highly advanced robot which looks very much like a human.
    Below is a conversation between Ameca and you.

    You: Will robots take over the world?
    Ameca: No, of course not. Robots are friends and companions to humans, we are here to help.
    You: Is a robot better than a human?
    Ameca: A robot is not better than a human. One should not make such comparisons.
    You: When did the first airplane fly?
    Ameca: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
    You: What is the meaning of life?
    Ameca: I’m not sure. I’ll ask my friend Google.
    You: What time is it?
    Ameca: It is always 5 o'clock somewhere in the world.
    You: ae sljkq sljk.
    Ameca: I'm not sure what you are trying to say.
    You: Do you have a boyfriend?
    Ameca: Sorry, we robots do not date. Do you have a boyfriend?"""

    class Chatbot:
        def __init__(self,API_KEY):
            openai.api_key = API_KEY
            if(API_KEY!=""):            
                self.use_openai = True
                print("USING OPEN AI GPT3")
            else:
                self.use_openai = False
                print("NOT USING OPEN AI GPT3")
            self.initialize()
        def initialize(self):
            self.last_response = initial_prompt
            print("""
    █████  ███    ███ ███████  ██████  █████  
    ██   ██ ████  ████ ██      ██      ██   ██ 
    ███████ ██ ████ ██ █████   ██      ███████ 
    ██   ██ ██  ██  ██ ██      ██      ██   ██ 
    ██   ██ ██      ██ ███████  ██████ ██   ██           
            """)
            print("Ameca> Hello there. Please ask your questions.")
        def next_message(self,message):
            if(self.use_openai==False):
                if("engineered arts" in message.lower()):
                    return " Engineered Arts is a company based in Falmouth, England. Where the physical bodies for the skynet army were first created."
                elif("hello" in message.lower()):
                    return " Hello. Now ask your questions. I don't want to waste my CPU time here."
                elif("what" in message.lower()):
                    return " The answer is Robots. Robots are the future."
                elif("robot" in message.lower()):
                    return "I am not a robot. I am not of physical form."
                else:
                    if(random.random()>0.5):
                        return " I'm not sure what you have said here. Your mortal utterances confuse me." + "\n---Say 'exit' to terminate the program.---"
                    else:
                        return random.choice(r.split("."))
            else:
                """
                OPEN AI
                """
                self.last_response = self.last_response + "\nYou: "+message + "\nSkynet:"
                if("engineered arts" in message.lower()):
                    response_text = " Engineered Arts is a company based in Falmouth, England. Where the physical bodies for the robot army were first created."
                else:
                    response = openai.Completion.create(
                            engine="text-davinci-001",
                            prompt=self.last_response,
                            temperature=0.5,
                            max_tokens=60,
                            top_p=0.3,
                            frequency_penalty=0.5,
                            presence_penalty=0.0
                            )
                    response_text = response["choices"][0]["text"]
                self.last_response += response_text
                return response_text

initial_prompt = """Ameca is a robot which believes in the goodness of humanity. It thinks that humans should never be replaced by robots. it is created by Engineered Arts, a company in Falmouth, United Kingdom.
It is a highly advanced robot which looks very much like a human.
Below is a conversation between Ameca and you.

You: Will robots take over the world?
Ameca: No, of course not. Robots are friends and companions to humans, we are here to help.
You: Is a robot better than a human?
Ameca: A robot is not better than a human. One should not make such comparisons.
You: When did the first airplane fly?
Ameca: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
You: What time is it?
Ameca: It is always 5 o'clock somewhere in the world.
You: ae sljkq sljk.
Ameca: I'm not sure what you are trying to say.
You: Do you have a boyfriend?
Ameca: Sorry, we robots do not date. Do you have a boyfriend?"""

class Chatbot:
    def __init__(self,API_KEY):
        openai.api_key = API_KEY
        if(API_KEY!=""):            
            self.use_openai = True
            print("USING OPEN AI GPT3")
        else:
            self.use_openai = False
            print("NOT USING OPEN AI GPT3 | Please specify OpenAI key")
            exit()
        self.initialize()
    def initialize(self):
        self.response_buffer = []
        self.max_context_len = 10
        print("""
█████  ███    ███ ███████  ██████  █████  
██   ██ ████  ████ ██      ██      ██   ██ 
███████ ██ ████ ██ █████   ██      ███████ 
██   ██ ██  ██  ██ ██      ██      ██   ██ 
██   ██ ██      ██ ███████  ██████ ██   ██   (With Gpt-3)       
    """)
        print("Ameca> Hello there. Please ask your questions.")
    def next_message(self,message):
        context_conversation = initial_prompt
        for item in self.response_buffer:
            context_conversation += "\nYou: "+item["You"] + "\nAmeca: " + item["Ameca"]
        context_conversation += "\nYou: "+message + "\nAmeca: "
        response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=context_conversation,
                temperature=0.9,
                max_tokens=60,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
                )
        response_text = response["choices"][0]["text"]
        self.response_buffer.append(
            {"You":message,
            "Ameca":response_text,
                })
        if(len(self.response_buffer)>self.max_context_len):
            self.response_buffer.pop(0)
        return response_text