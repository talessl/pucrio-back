from src.domain.entities import Token


class ITokenRepository:
    def buscar_por_codigo(codigo_token) -> Token | None:
        pass

    def buscar_por_id(self, token_id: int):
        pass

    def atualizar_revogado(self, token):
        pass

    def salvar_token(self, token):
        pass

    def buscar_por_historico(self, historico_id) -> list:
        pass
