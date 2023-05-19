import httpx
import os
import time
from playdirect import PlayDirectFromURL

class HeisenbergTTS:
    def __init__(self, text, lang="Matthew"):
        self.url = "https://ttsmp3.com/makemp3_new.php"
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-type": "application/x-www-form-urlencoded",
            "Cookie": "cookieconsent_status=allow",
            "Host": "ttsmp3.com",
            "Origin": "https://ttsmp3.com",
            "Referer": "https://ttsmp3.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }
        self.text = text
        self.lang = lang

    def play(self):
        data = {"msg": self.text, "lang": self.lang, "source": "ttsmp3"}
        print(":: sending request to server")
        start_time = time.time()
        response = httpx.post(self.url, headers=self.headers, data=data)
        print(":: received response")
        if response.status_code == 200:
            response_json = response.json()
            audio_url = response_json["URL"]
            end_time = time.time()
            time_taken = end_time - start_time
            print(":: calling playdirect")
            player = PlayDirectFromURL(audio_url).play()
            print(f":: time taken : {player+time_taken:.2f} sec")
        else:
            print("Error:", response.status_code)
