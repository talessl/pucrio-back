from dataclasses import dataclass
from src.domain.interfaces.historico_interface import IHistoricoRepository
from src.domain.entities import Historico


@dataclass
class CriarHistoricoDTO:
    titulo: str
    descricao: str
    paciente_id: int


class AdicionarHistoricoUseCase:
    def __init__(self, historico_repo: IHistoricoRepository):
        self.historico_repo = historico_repo

    def executar_adicao_historico(self, dados: CriarHistoricoDTO):

        if not dados.descricao:
            raise ValueError(
                "É necessária uma descrição para identificar o histórico.")

        novo_historico = Historico(
            descricao=dados.descricao,
            paciente_id=dados.paciente_id,
            criado_em=None,
            titulo=dados.titulo,
            arquivado=0,
            id=None
        )

        historico_salvo = self.historico_repo.criar_historico(novo_historico)

        return historico_salvo
