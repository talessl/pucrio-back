from src.domain.interfaces.arquivo_interface import IArquivoRepository
from src.domain.interfaces.upload_interface import IUploadRepository
from src.domain.entities import ArquivoTipo, AutorTipo, Arquivo
from dataclasses import dataclass
from typing import Optional
from werkzeug.datastructures import FileStorage


@dataclass
class AdicionarArquivoInputDTO:
    historico_id: int
    enviado_por: AutorTipo     # 'medico' ou 'paciente'
    tipo: ArquivoTipo            # 'exame', 'laudo' ou 'documento'
    nome_original: str
    url: str
    arquivo_bruto: Optional[FileStorage]
    descricao: Optional[str] = None


class AdicionarArquivoUseCase:
    def __init__(self, repository: IArquivoRepository, upload_repo: IUploadRepository):
        self.repository = repository
        self.upload_repo = upload_repo

    def executar_adicao_arquivo(self, dados: AdicionarArquivoInputDTO):

        url_gerada = self.upload_repo.salvar_fisicamente(
            nome_original=dados.nome_original, arquivo_bruto=dados.arquivo_bruto
        )

        novo_arquivo = Arquivo(
            tipo=dados.tipo,
            descricao=dados.descricao,
            enviado_por=dados.enviado_por.value,
            historico_id=dados.historico_id,
            nome_original=dados.nome_original,
            url=url_gerada,
        )

        arquivo_salvo = self.repository.salvar_arquivo(novo_arquivo)

        return arquivo_salvo
