from src.domain.interfaces.historico_interface import IHistoricoRepository
from src.domain.entities import Historico


class ListarHistoricosPacienteUseCase:
    def __init__(self, historico_repository: IHistoricoRepository):
        self.historico_repository = historico_repository

    def executar_listagem(self, paciente_id) -> list:
        historicos = self.historico_repository.listar_historicos_paciente(
            paciente_id=paciente_id)

        if not historicos:
            return []

        return historicos
