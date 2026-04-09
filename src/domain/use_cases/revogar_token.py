from src.domain.interfaces.token_interface import ITokenRepository
from src.domain.interfaces.historico_interface import IHistoricoRepository


class RevogarTokenUseCase:
    def __init__(self, token_repository: ITokenRepository, historico_repository: IHistoricoRepository):
        self.token_repository = token_repository
        self.historico_repository = historico_repository

    def executar_revogacao(self, paciente_logado_id: int, token_id: int):
        token = self.token_repository.buscar_por_id(token_id)
        if not token:
            raise ValueError("Token não encontrado.")

        historico = self.historico_repository.buscar_historico_por_id(
            token.historico_id)
        if not historico or int(historico.paciente_id) != int(paciente_logado_id):
            raise ValueError(
                "Acesso negado: Você não tem permissão para revogar este link.")

        if token.revogado:
            raise ValueError("Este link já foi revogado anteriormente.")

        token.revogar()

        self.token_repository.atualizar_revogado(token)

        return True
