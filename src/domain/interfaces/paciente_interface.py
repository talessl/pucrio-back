from src.domain.entities import Paciente

class IPacienteRepository:
    def buscar_paciente_por_email(self, email: str) -> Paciente:
        pass
    
    def buscar_paciente_por_id(self, paciente_id: int):
        pass
    
    def salvar_paciente(paciente: Paciente) -> Paciente:
        pass