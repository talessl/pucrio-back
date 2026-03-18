from src.domain.entities import RegistroTipo, AutorTipo, Registro
from src.domain.interfaces.registro_interface import IRegistroRepository
from src.domain.interfaces.paciente_interface import IPacienteRepository
from dataclasses import dataclass

@dataclass
class AdicionarRegistroPacienteInputDTO:
    historico_id: int
    tipo: RegistroTipo 
    conteudo: str

class AdicionarRegistroPacienteUseCase:
    def __init__(self, registro_repository: IRegistroRepository, paciente_repository: IPacienteRepository):
        self.registro_repository = registro_repository
        self.paciente_repository = paciente_repository

    def executar_adicao_registro_paciente(self, paciente_id: int, dados: AdicionarRegistroPacienteInputDTO):
        paciente = self.paciente_repository.buscar_paciente_por_id(paciente_id)
        if not paciente:
            raise ValueError("Paciente não encontrado no sistema.")

        if dados.tipo in [RegistroTipo.DIAGNOSTICO, RegistroTipo.CONDUTA]:
            raise ValueError("Pacientes só podem registrar 'sintomas' ou 'informações'.")

        novo_registro = Registro(
            id=None,
            historico_id=dados.historico_id,
            autor_tipo=AutorTipo.PACIENTE,  
            autor_nome=paciente.nome,       
            autor_crm=None,                 
            tipo=dados.tipo,
            conteudo=dados.conteudo,
            visivel=True
        )

        registro_salvo = self.registro_repository.salvar(novo_registro)
        
        return registro_salvo
    