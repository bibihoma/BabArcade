from gtts import gTTS
import os
tts = gTTS(text='red 3; blue 5', lang='en')
tts.save("Jeremy.mp3")
os.system("mpg321 Jeremy.mp3")
