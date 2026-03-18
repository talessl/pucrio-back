# src/infrastructure/auth/jwt_auth_generator.py
import jwt
from datetime import datetime, timedelta, timezone
from src.domain.adapters.autenticacao import IAuthGenerator

class JwtAuthGenerator(IAuthGenerator):
    def __init__(self, secret_key: str, expiracao_horas: int = 24):
        self.secret_key = secret_key
        self.expiracao_horas = expiracao_horas

    def gerar_autenticacao(self, paciente_id: int) -> str:
        agora = datetime.now(timezone.utc)
        
        payload = {
            "sub": str(paciente_id), 
            
            "exp": agora + timedelta(hours=self.expiracao_horas),
            
            "iat": agora
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        return token