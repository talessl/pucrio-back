from src.domain.interfaces.historico_interface import IHistoricoRepository
from src.domain.entities import Historico 
from src.infrastructure.db.database import DatabaseInterface

class HistoricoRepository(IHistoricoRepository):
    def __init__(self, db_conexao: DatabaseInterface):
        self.db = db_conexao

    def buscar_historico_por_id(self, historico_id: int) -> Historico | None:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM historico WHERE id = ?", (historico_id,))
        linha = cursor.fetchone()
        
        if not linha:
            return None
            

        return Historico(
            id=linha['id'],
            paciente_id=linha['paciente_id'],
            criado_em=linha['criado_em']
            # titulo=linha['titulo'],       <-- Exemplo de outros campos
            # criado_em=linha['criado_em']  <-- Exemplo de outros campos
        )