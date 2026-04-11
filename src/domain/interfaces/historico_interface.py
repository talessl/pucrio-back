from src.domain.entities import Historico


class IHistoricoRepository:
    def buscar_historico_por_id(self, historico_id) -> Historico:
        pass

    def atualizar_historico(self, historico: Historico) -> Historico:
        pass

    def listar_historicos_paciente(self, paciente_id) -> list[Historico]:
        pass

    def criar_historico(self, historico: Historico) -> Historico:
        pass
