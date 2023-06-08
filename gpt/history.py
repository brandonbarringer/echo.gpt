from dataclasses import dataclass
from typing import Literal, List

@dataclass
class HistoryItem:
    role:Literal['user', 'assistant', 'system']
    content:str

class History:
    def __init__(self) -> None:
        self.history:List[HistoryItem] = []

    def get(self) -> List[HistoryItem]:
        '''
        Returns the history.
        '''
        return self.history
    
    def add(self, history:HistoryItem) -> None:
        '''
        Adds a history item.
        '''
        self.history.append(history)
    
    def set(self, history:List[HistoryItem]) -> None:
        '''
        Sets the history.
        '''
        self.history = history
