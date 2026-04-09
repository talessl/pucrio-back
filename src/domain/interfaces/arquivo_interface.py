from src.domain.entities import Arquivo


class IArquivoRepository:
    def salvar_arquivo(self, arquivo: Arquivo) -> Arquivo:
        pass

    def listar_por_historico(self, historico_id) -> list:
        pass
