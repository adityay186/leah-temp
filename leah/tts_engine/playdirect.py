from pydub import AudioSegment
from pydub.playback import play
import io
import httpx
import time

class PlayDirectFromURL:
    def __init__(self, url):
        self.url = url
        self.audio_file = None

    def fetch_data_content(self):
        with httpx.stream('GET', self.url) as response:
            self.data_content = response.read()

    def create_audio_file(self):
        self.audio_file = AudioSegment.from_file(io.BytesIO(self.data_content))

    def play_audio_file(self):
        play(self.audio_file)

    def play(self):
        start_time = time.time()
        print(":: fetching audio data")
        self.fetch_data_content()
        print(":: creating audio file")
        self.create_audio_file()
        end_time = time.time()

        time_taken = end_time - start_time

        print(":: playing audio")
        self.play_audio_file()

        return time_taken
