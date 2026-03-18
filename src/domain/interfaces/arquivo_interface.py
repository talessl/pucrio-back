from src.domain.entities import Arquivo

class IArquivoRepository:
    def salvar_arquivo(self, arquivo: Arquivo) -> Arquivo:
        pass
    