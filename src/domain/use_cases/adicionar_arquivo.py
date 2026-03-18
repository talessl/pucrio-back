from src.domain.interfaces.arquivo_interface import IArquivoRepository
from src.domain.entities import ArquivoTipo, AutorTipo, Arquivo
from dataclasses import dataclass
from typing import Optional

@dataclass
class AdicionarArquivoInputDTO:
    historico_id: int
    enviado_por: AutorTipo     # 'medico' ou 'paciente'
    tipo: ArquivoTipo            # 'exame', 'laudo' ou 'documento'
    nome_original: str
    url: str
    descricao: Optional[str] = None
    

class AdicionarArquivoUseCase:
    def __init__(self, repository: IArquivoRepository):
        self.repository = repository
    
    def executar_adicao_arquivo(self, dados: AdicionarArquivoInputDTO):
        novo_arquivo = Arquivo(
            tipo=dados.tipo,
            descricao=dados.descricao,
            enviado_por=dados.enviado_por.value,
            historico_id=dados.historico_id,
            nome_original=dados.nome_original,
            url=dados.url,
        )
        
        arquivo_salvo = self.repository.salvar(novo_arquivo)

        return arquivo_salvo