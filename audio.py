import os
import subprocess

class Audio:
    @staticmethod
    def play(filename:str, blocking:bool=True):
        if blocking:
            os.system(f"afplay {filename}")
        else:
            subprocess.Popen(['afplay', filename])