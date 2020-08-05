from pocketsphinx import *
from sphinxbase import *

from os import environ, path
import pyaudio
import wave
import audioop
from collections import deque
import time
import math
import gtts
import speech_recognition as sr


class Assistant:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.language = 'en'

    def speak(self, text):
        myobj = gtts.gTTS(text=text, lang=self.language, slow=False)
        myobj.save("temp.mp3")
        os.system("mpg321 temp.mp3")

    def run(self):
        adjusted = False
        while True:
            with self.mic as source:
                if not adjusted:
                    self.speak("Adjusting microphone levels, please stay quiet")
                    self.r.adjust_for_ambient_noise(source)
                    adjusted = True

                self.speak("Listening for speech")
                audio = self.r.listen(source)
                self.speak("Converting speech to text:")

            try:
                words = self.r.recognize_sphinx(audio)
                self.speak(f"You said: {words}")
            except sr.UnknownValueError as e:
                self.speak("No words recognised")

def main():
    ass = Assistant()
    ass.run()

    #https://minimaxir.com/2019/09/howto-gpt2/


if __name__ == "__main__":
    main()







