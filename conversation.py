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
    def __init__(self, input_dev=0):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 1
        self.PREV_AUDIO = 0.5
        self.TRESHOLD = 4500
        self.num_phrases = -1

        MODELDIR = "/usr/local/share/pocketsphinx/model/"
        DATADIR = "/my/Desktop/directory/pocketsphinx-master/test/data/"

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

    def save_audio(self, data, p):
        filename = "audio_" + str(int(time.time()))
        data = 'b'.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def decode_phrase(self, wav_file):
        self.decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
            buffer = stream.read(1024)
            if buffer:
                self.decoder.process_raw(buffer, False, False)
            else:
                break
            self.decoder.end_utt()
            words = []
            [words.append(seg.word) for seg in self.decoder.seg()]
            return words

    def run(self):
        self.setup_mic()

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        print("Mic set up and listening. ")

        audio2send = []
        cur_data = ""
        rel = self.RATE/self.CHUNK
        slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
        prev_audio = deque(maxlen=int(self.PREV_AUDIO * rel))
        started = False

        while True:
            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

            if sum([x > self.TRESHOLD for x in slid_win]) > 0:
                if not started:
                    print("Starting recording of phrase")
                    started = True
                audio2send.append(cur_data)

            elif started:
                print("Finished recording, decoding atm")
                filename = self.save_audio(list(prev_audio) + audio2send, p)
                r = self.decode_phrase(filename)
                print(f"Detected: {r}")

                os.remove(filename)
                slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
                prev_audio = deque(maxlen=int(0.5 * rel))
                audio2send = []
                print("")
                print("Listening ...")

            else:
                prev_audio.append(cur_data)

        print("Done listening")
        stream.close()
        p.terminate()


def main():
    sd = SpeechDetector()
    try:
        sd.run()
    except(KeyboardInterrupt):
        print("Goodbye")
        sys.exit()
    #except Exception as e:
        #exc_type, exc_value, exc_tranceback = sys.exe_info()
        #traceback.print_exception(exc_type, exc_value, exc_traceback,
        #                          limit=2,
        #                          file=sys.stdout)
        #sys.exit()


if __name__ == "__main__":
    main()
