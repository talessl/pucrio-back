from src.domain.interfaces.arquivo_interface import IArquivoRepository
from src.infrastructure.db.database import DatabaseInterface
from src.domain.entities import Arquivo

class ArquivoRepository(IArquivoRepository):
    def __init__(self, db: DatabaseInterface):
        self.db = db
    
    def salvar_arquivo(self, arquivo: Arquivo) -> Arquivo:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        query = """
            INSERT INTO arquivo (
                historico_id, 
                enviado_por, 
                tipo, 
                nome_original, 
                url, 
                descricao, 
                visivel
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        valores = (
            arquivo.historico_id,
            arquivo.enviado_por,
            arquivo.tipo.value,    
            arquivo.nome_original,
            arquivo.url,
            arquivo.descricao,
            arquivo.visivel
        )
        
        
        cursor.execute(query, valores)
        conexao.commit()
        
        arquivo.id = cursor.lastrowid
        
        return arquivo