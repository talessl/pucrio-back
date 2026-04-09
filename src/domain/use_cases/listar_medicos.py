from src.domain.interfaces.token_interface import ITokenRepository


class ListarMedicosUseCase:
    def __init__(self, token_repository: ITokenRepository):
        self.token_repo = token_repository

    def exectuar_listagem(self, historico_id):
        medicos = self.token_repo.buscar_por_historico(
            historico_id=historico_id)

        if not medicos:
            return []

        return medicos
