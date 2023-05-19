# gtts

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import time

class GoogleTTS:
    def __init__(self, text, lang = "en", tld = "us"):
        self.text = text
        self.lang = lang
        self.tld = tld
        self.audio = None

    def create_audio(self):
        print(":: creating gTTS object")
        tts = gTTS(self.text, lang=self.lang, tld = self.tld)
        print(":: writing audio data to BytesIO object")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        print(":: loading audio into PyDub")
        self.audio = AudioSegment.from_file(audio_bytes, format="mp3")

    def play_audio(self):
        print(":: playing audio")
        play(self.audio)

    def play(self):
        start_time = time.time()
        self.create_audio()
        end_time = time.time()
        self.play_audio()
        print(f":: time taken: {end_time-start_time:.2f} sec")
