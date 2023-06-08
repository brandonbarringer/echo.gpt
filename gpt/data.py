import os
from gpt.history import HistoryItem
from config import Config

class Data():
    def __init__(self):
        self.config = Config()

    @classmethod
    def get(cls, name:str):
        return getattr(cls(), name)
    
    def get_all(self):
        return [
            getattr(self, name) 
            for name in dir(self) 
            if not name.startswith('__') 
            and not callable(getattr(self, name))
            and not name == 'config'
        ]

    @property
    def system(self):
        root_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
        return [
            HistoryItem('system', f'''
                Your name is Echo. You are a computer assistant for a user named {self.config.user.name}. 
                Your responses will activate preset programs in the terminal. 
                The execution will be in the terminal. You will wrap terminal commands with "```"
                if a response requires a google search or access to the internet use trafilatura as the terminal command and the url as the argument.
                Any response that is not wrapped in "```" will be spoken by the computer.

                Here is some relevant information:
                {self.config.user.name} is using a macOS.
                {self.config.user.name} is using python 3.10.0.
                {self.config.user.name} is located in Dayton, Nevada.
                {self.config.user.name} uses VSCode for coding and editing text files.
                {self.config.user.name} uses Google Chrome for browsing the web.
                {self.config.user.name} uses Youtube for watching videos.
                {self.config.user.name} uses Youtube Music for listening to music.
                {self.config.user.name} uses Warp for a terminal.
                The templates directory is located at {os.path.join(root_path, 'templates')}
                current directory: {root_path}
                '''.strip())
        ]

    @property
    def song(self):
        return [
            HistoryItem('user', 'Play a song by the Beatles'),
            HistoryItem('assistant', f'''
            Okay, playing a song by the Beatles.
            ```open https://music.youtube.com/search?q=the%20beatles```
            '''.strip())
        ]

    @property
    def weather(self):
        return [
            HistoryItem('user', 'What is the current weather?'),
            HistoryItem('assistant', f'''
            One moment.
            ```curl wttr.in/{self.config.user.city},{self.config.user.state}?format=%C,%t,%w,%p```
            '''.strip())
        ]

    @property
    def place(self):
        return [
            HistoryItem('user', 'Is Home Depot open?'),
            HistoryItem('assistant', f'''
            One moment.
            ```date +"%T" && trafilatura -u "https://www.google.com/search?q=hours+for+home+depot+{self.config.user.city}+{self.config.user.state}" | grep -i "store hours"```
            '''.strip())
        ]

    @property
    def reminder(self):
        return [
            HistoryItem('user', 'Remind me to go to the DMV tomorrow at 10 AM for my appointment at 11'),
            HistoryItem('assistant', '''
            Okay!
            ```osascript -e 'tell application "Reminders"
                set newReminder to make new reminder with properties {name:"Go To the DMV at 11 AM", due date:date "tomorrow 10:00 AM"}
            end tell'```
            '''.strip())
        ]

    @property
    def calendar(self):
        return [
            HistoryItem('user', 'What is on my agenda for today?'),
            HistoryItem('assistant', f'''
            One moment, grabbing your agenda from Google Calendar.
            ```gcalcli gcalcli agenda --calendar={self.config.user.name}```
            '''.strip())
        ]
