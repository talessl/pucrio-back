from werkzeug.security import generate_password_hash, check_password_hash
from src.domain.adapters.hasher import IPasswordHasher

class FlaskPasswordHasher(IPasswordHasher):
    
    def comparar_senhas(self, senha_hash: str, senha_pura: str) -> bool:
    
        return check_password_hash(senha_hash, senha_pura)
        
    def gerar_hash(self, senha_pura: str) -> str:
    
        return generate_password_hash(senha_pura)