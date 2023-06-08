import subprocess
import re
import threading
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from state import State
from config import Config
from audio import Audio

state = State()
config = Config()

class Speaker:
    @staticmethod
    def say(text, thread=True):
        if thread:
            sentences = re.split(':|\.|\?|\!|\n', text) if text else []
            threads = []
            for i, sentence in enumerate(sentences):
                if sentence:
                    thread = threading.Thread(target=Speaker._synthesize_and_play, args=(sentence, i))
                    threads.append(thread)
                    thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Remove the audio files
            subprocess.Popen(['rm', 'output-*.mp3'])
        else:
            Speaker._synthesize_and_play(text)
    
    @staticmethod
    def _synthesize_and_play(text:str, count:int=1):

        authenticator = IAMAuthenticator(config.ibm.key)
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(config.ibm.url)

        filename = f'output-{count}.mp3'
        with open(filename, 'wb') as audio_file:
            res = text_to_speech.synthesize(
                text,
                accept='audio/mp3',
                voice='en-US_EmmaExpressive',
                rate_percentage=2
            )
            audio_file.write(res.get_result().content)

        # Play the audio file, blocking
        Audio.play(filename)
        # Remove the audio file
        subprocess.Popen(['rm', filename])