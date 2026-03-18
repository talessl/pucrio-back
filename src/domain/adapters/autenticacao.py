from abc import ABC, abstractmethod

class IAuthGenerator(ABC):
    @abstractmethod
    def gerar_autenticacao(self, usuario_id):
        pass