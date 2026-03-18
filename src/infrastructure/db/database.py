from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    
    @abstractmethod
    def get_connection(self):
        pass
    
    @abstractmethod
    def close(self):
        pass