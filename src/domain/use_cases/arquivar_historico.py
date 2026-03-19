from src.domain.interfaces.historico_interface import IHistoricoRepository


class ArquivarHistoricoUseCase:
    def __init__(self, historico_repository: IHistoricoRepository):
        self.historico_repository = historico_repository

    def executar_arquivamento(self, paciente_logado_id: int, historico_id: int):
        historico = self.historico_repository.buscar_historico_por_id(
            historico_id)

        if not historico:
            raise ValueError("Histórico não encontrado!")

        if historico.paciente_id != paciente_logado_id:
            raise ValueError(
                "Acesso negado. Este histórico não pertence a você.")

        if historico.arquivado:
            raise ValueError("O Histórico já está arquivado!")

        historico.arquivar()

        self.historico_repository.atualizar_historico(historico)

        return historico
