import openai
from dataclasses import dataclass
from gpt.history import History, HistoryItem
from config import Config

ChatMessage = HistoryItem

@dataclass
class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: str

@dataclass
class ChatUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ChatResponse:
    id: str
    object: str
    created: int
    choices: ChatChoice

class Chat():
    def __init__(
        self,
        persistent_history:History,
        model:str="gpt-3.5-turbo", 
        history_limit:int=10,
        max_tokens:int=150,
    ):
        config = Config()
        self.model = model
        self.history_limit = history_limit
        self.max_tokens = max_tokens
        self.persistent_history = persistent_history
        openai.organization = config.openai.org
        openai.api_key = config.openai.key
        self.chat_log = History()
        self.chat_log.set(self.persistent_history.get())

    def get_response(self, user_input):
        self._update_chat_log(user_input)
        messages = [{'role': message.role, 'content': message.content} for message in self.chat_log.get()]
        response = openai.ChatCompletion.create(model=self.model, messages=messages, max_tokens=self.max_tokens)
        reply = response['choices'][0]['message']['content']
        self._update_chat_log(reply)
        return reply
        
    def _update_chat_log(self, message):
        if len(self.chat_log.get()) >= self.history_limit:
            self.chat_log.get().pop(0)
        self.chat_log.add(ChatMessage(role="user", content=message))
