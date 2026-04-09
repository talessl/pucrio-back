from src.domain.interfaces.registro_interface import IRegistroRepository
from src.domain.entities import Registro


class listarRegistrosPacienteUseCase:
    def __init__(self, registro_repository: IRegistroRepository):
        self.registro_repository = registro_repository

    def executar_listagem(self, historico_id: int) -> list:
        registros = self.registro_repository.buscar_por_historico_id(
            historico_id)

        if not registros:
            return []

        return registros
