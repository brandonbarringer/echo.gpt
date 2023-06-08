import subprocess
import threading
import json
from speaker import Speaker
from gpt.chat import Chat
# from watcher import watch
from state import State
from config import Config
from gpt.data import Data
from gpt.history import History
from listener import Listener
from pprint import pprint

state = State()
config = Config()
listener = Listener()

def parse_response(response:str, chatbot:Chat):
    '''
    Parses the response from the chatbot and executes the commands.
    '''
    print(response)
    commands = response.split('```')
    text_before = commands.pop(0).strip() if len(commands) > 0 else None
    text_after = commands.pop(-1).strip() if len(commands) > 0 else None
    command = commands if len(commands) > 0 else []
    
    Speaker.say(text_before) if text_before else None

    for c in command:
        try:
            output = subprocess.check_output(c, shell=True)
            print(output.decode('utf-8'))
            res = chatbot.get_response(output.decode('utf-8'))
        except Exception as e:
            res = chatbot.get_response(f'There was an error: {output.decode("utf-8")}')
        parse_response(res, chatbot)
    
    Speaker.say(text_after) if text_after else None

    state.command_executed = True

def listen_background(chat:Chat):
    while True:
        command = listener.listen()
        if command is not None:
            print(command)
            response = chat.get_response(command)
            parse_response(response, chat)

def set_config():
    with open('config.json', 'r') as f:
        c:dict = json.load(f)
    config.user = c['user']
    config.openai = c['openai']
    config.ibm = c['ibm']
    config.music = c['music']

def setup():
    set_config()
    p_history = History()
    gpt_data = Data()
    # flatten the 2d array
    items = [item for sublist in gpt_data.get_all() for item in sublist]
    p_history = History()
    p_history.set(items)
    state.chat = Chat(
        persistent_history = p_history,
    )
    state.command_executed = True

def main():
    setup()
    listen_thread = threading.Thread(target=listen_background, args=(state.chat,))
    listen_thread.start()

if __name__ == "__main__":
    main() 