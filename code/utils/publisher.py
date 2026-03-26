
from abc import ABC, abstractmethod

from utils.observer import Observer

class Publisher(ABC):
    def __init__(self):
        self._observers = []
        pass

    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def notify(self, message: object):
        for observer in self._observers:
            observer.update(message)