class ValidarTokenAcessoUseCase:
    def __init__(self, token_repository):
        self.token_repository = token_repository

    def executar_validacao(self, codigo: str):
        token = self.token_repository.buscar_por_codigo(codigo)

        if not token:
            raise ValueError("Token inválido ou não encontrado.")

        if not token.esta_valido():
            raise ValueError("Este link médico não é valido.")

        return {
            "id": token.id,
            "valor": token.valor,
            "historico_id": token.historico_id,
            "expira_em": token.expira_em,
            "descricao": token.descricao
        }
