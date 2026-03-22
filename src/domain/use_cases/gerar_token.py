import secrets
from datetime import datetime, timedelta
from dataclasses import dataclass
from src.domain.entities import Token
from src.domain.interfaces.token_interface import ITokenRepository
from src.domain.interfaces.historico_interface import IHistoricoRepository


@dataclass
class GerarTokenInputDTO:
    descricao: str
    historico_id: int
    horas_validade: int = 24


class GerarTokenUseCase:
    def __init__(self, token_repository: ITokenRepository, historico_repository: IHistoricoRepository):
        self.token_repository = token_repository
        self.historico_repository = historico_repository

    def executar_criacao(self, paciente_logado_id: int, dados: GerarTokenInputDTO) -> Token:

        codigo_seguro = secrets.token_urlsafe(16)
        valor_token = f"tok_{codigo_seguro}"

        agora = datetime.now()
        expira = agora + timedelta(hours=dados.horas_validade)

        formato_data = "%Y-%m-%d %H:%M:%S"
        criado_em_str = agora.strftime(formato_data)
        expira_em_str = expira.strftime(formato_data)

        novo_token = Token(
            descricao=dados.descricao,
            valor=valor_token,
            historico_id=dados.historico_id,
            criado_em=criado_em_str,
            expira_em=expira_em_str,
            revogado=0
        )

        token_salvo = self.token_repository.salvar_token(novo_token)

        return token_salvo
