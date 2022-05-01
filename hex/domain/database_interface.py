from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def create_order(self, order):
        pass
    