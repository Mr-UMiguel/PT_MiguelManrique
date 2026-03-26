from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self):
        pass

    def update(self,message:object):
        pass