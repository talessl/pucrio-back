
from dataclasses import dataclass
from src.domain.adapters.hasher import IPasswordHasher
from src.domain.interfaces.paciente_interface import IPacienteRepository
from src.domain.entities import Paciente

@dataclass
class CadastrarPacienteInputDTO:
    nome: str
    email: str
    senha: str
    
class CadastrarPacienteUseCase:
    
    def __init__(self, hasher: IPasswordHasher, paciente_repository: IPacienteRepository):
        self.hasher = hasher
        self.paciente_repository = paciente_repository
        
    def executar_cadastro(self, dados: CadastrarPacienteInputDTO) -> Paciente:
        paciente_existente = self.paciente_repository.buscar_paciente_por_email(dados.email)
        if paciente_existente:
            raise ValueError("Este e-mail já está em uso por outro paciente.")
        
        senha_criptografada = self.hasher.gerar_hash(dados.senha)
        
        novo_paciente = Paciente(
            nome=dados.nome,
            email=dados.email,
            senha=senha_criptografada
        )

        paciente_salvo = self.paciente_repository.salvar_paciente(novo_paciente)
        
        return paciente_salvo