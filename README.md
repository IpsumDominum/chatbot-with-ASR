# Test

This repository uses vosk-api and stt(speech recognition).

vosk-api has default small model included in this repo, but for more models + stt models you'd have to download them:

Coqui-STT: https://stt.readthedocs.io/en/latest/DEPLOYMENT.html

Vosk-API:  https://alphacephei.com/vosk/models

vosk works much better for me, but perhaps it is because my microphone isn't that great.

Microphone will say "input overflow" and give bad recognition results if sample rate isn't set correctly.



```
python -m venv ASRTest #Create virtual enviornment

source ASRTest/bin/activate #Activate virtual enviornment

python -m pip install -r requirements.txt

python run.py
```


