from src.domain.entities import Registro


class IRegistroRepository:
    def salvar_registro(self, registro: Registro):
        pass

    def buscar_por_historico_id(self, historico_id) -> list:
        pass
