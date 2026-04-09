from src.domain.entities import Arquivo
from src.domain.interfaces.arquivo_interface import IArquivoRepository


class ListarArquivosUseCase:
    def __init__(self, arquivo_repository: IArquivoRepository):
        self.arquivo_repo = arquivo_repository

    def executar_listagem(self, historico_id):

        arquivos = self.arquivo_repo.listar_por_historico(
            historico_id=historico_id)

        if not arquivos:
            return []

        return arquivos
