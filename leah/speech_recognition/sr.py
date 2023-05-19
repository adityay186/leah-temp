import signal
import sys
import time
from threading import Thread
from argparse import ArgumentParser
from tabulate import tabulate

from pvleopard import create, LeopardActivationLimitError
from pvrecorder import PvRecorder


class Recorder(Thread):
    def __init__(self, audio_device_index):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = False
        self._audio_device_index = audio_device_index

    def is_recording(self):
        return self._is_recording

    def run(self):
        self._is_recording = True

        recorder = PvRecorder(device_index=self._audio_device_index, frame_length=160)
        recorder.start()

        while not self._stop:
            audio_data = recorder.read()
            self._pcm.extend(audio_data)

            # Check for silence based on a threshold (adjust as needed)
            if not self.is_speech_active(audio_data):
                self._stop = True

        recorder.stop()
        self._is_recording = False

    def stop(self):
        self._stop = True
        while self._is_recording:
            pass

        return self._pcm

    @staticmethod
    def is_speech_active(audio_data, threshold=1500):
        return any(abs(sample) > threshold for sample in audio_data)


def main():
    access_key = "61LuNHOI0Wkh4yBbrkck+HDV39muOqtQF3oevQE3Xt+DhIuiWzo1zg=="  # Replace with your actual access key

    leopard = create(access_key=access_key)

    recorder = Recorder(-1)  # You can modify the audio device index if needed
    recorder.start()
    print("Recording...")

    while True:
        time.sleep(0.1)
        if not recorder.is_recording():
            break

    audio_data = recorder.stop()

    try:
        transcript, words = leopard.process(audio_data)
        print(transcript)
        print(tabulate(words, headers=['word', 'start_sec', 'end_sec', 'confidence'], floatfmt='.2f'))
    except LeopardActivationLimitError:
        print('AccessKey has reached its processing limit.')

    leopard.delete()


if __name__ == '__main__':
    main()
