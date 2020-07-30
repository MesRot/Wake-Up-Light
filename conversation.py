from pocketsphinx import *
from sphinxbase import *

from os import environ, path
import pyaudio
import wave
import audioop
from collections import deque
import time
import math

#https://gist.github.com/srli/72c7938230537b4f8a4c


class SpeechDetector:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paINT16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 1
        self.PREV_AUDIO = 0.5
        self.TRESHOLD = 4500
        self.num_phrases = -1

        MODELDIR = "../../tools/pocketsphinx/model"
        DATADIR = "../../tools/pocketsphinx/test/data"

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
        config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

        self.decoder = Decoder(config)

    def setup_mic(self, num_samples=50):
        print("getting mic intensity")
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]

        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print("Finished")
        print(f"Average audio intensity: {r}")
        stream.close()
        p.terminate()

        if r < 3000:
            self.TRESHOLD = 3500
        else:
            self.TRESHOLD = r + 100

def main():
    sd = SpeechDetector
    sd.setup_mic()

if __name__ == "__main__":
    main()
