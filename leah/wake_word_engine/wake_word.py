import struct
import pyaudio
import pvporcupine

def detect_wake_word():
    porcupine = None
    pa = None
    audio_stream = None

    keys = {
            "adityay186@gmail.com" : "61LuNHOI0Wkh4yBbrkck+HDV39muOqtQF3oevQE3Xt+DhIuiWzo1zg==",
            "20190802060@dypiu.ac.in" : "Zb5nW42pBDH0wOptYTK1neJ1fyrYWPJZv0T0IfkFQKmzXTlQZuo24w=="
    }

    try:
        porcupine = pvporcupine.create(access_key = keys["adityay186@gmail.com"],
                                        keyword_paths = ["hey_leah-linux/hey_leah-linux.ppn"])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Hotword Detected")
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()