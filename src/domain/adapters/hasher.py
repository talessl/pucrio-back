from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    
    @abstractmethod
    def comparar_senhas(self, senha_hash: str, senha_pura: str) -> bool:
        """Verifica se a senha digitada bate com o hash salvo no banco"""
        pass

    @abstractmethod
    def gerar_hash(self, senha_pura: str) -> str:
        """Transforma a senha em um hash seguro para salvar no banco"""
        pass