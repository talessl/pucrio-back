from dataclasses import dataclass
from src.domain.interfaces.paciente_interface import IPacienteRepository
from src.domain.adapters.hasher import IPasswordHasher
from src.domain.adapters.autenticacao import IAuthGenerator

@dataclass
class FazerLoginDTO:
    email: str
    senha: str
    
class FazerLoginUseCase:
    def __init__(self, paciente_repositorio: IPacienteRepository, hasher: IPasswordHasher, auth: IAuthGenerator):
        self.paciente_repositorio = paciente_repositorio
        self.hasher = hasher
        self.auth = auth
    
    def executar_login(self, usuario_dto: FazerLoginDTO):
        
        paciente = self.paciente_repositorio.buscar_paciente_por_email(usuario_dto.email)
        
        
        if not paciente:
            raise ValueError("E-mail ou senha inválidos")
        
        if not self.hasher.comparar_senhas(paciente.senha, usuario_dto.senha):
            raise ValueError("E-mail ou senha inválidos")
        
       
        token = self.auth.gerar_autenticacao(paciente_id=paciente.id) 
        
        return token
        