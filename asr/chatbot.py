import openai

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