import speech_recognition as sr
from state import State
from audio import Audio
from speaker import Speaker

class Listener:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.state = State()
    
    def listen(self):
        '''
        Listens for audio and converts it to text using Google Speech Recognition
        and returns the text.
        '''
        command_executed = self.state.command_executed
        r:sr.Recognizer = self.recognizer

        with sr.Microphone() as source:
            if command_executed:
                Audio.play('/System/Library/Sounds/Glass.aiff', False)
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
            try:
                return r.recognize_google(audio)
            except sr.UnknownValueError as e:
                self.state.command_executed = False
                return None
            except sr.RequestError as e:
                Speaker.say("Could not request results from Google Speech Recognition service; {0}".format(e))
                self.state.command_executed = False
                return None