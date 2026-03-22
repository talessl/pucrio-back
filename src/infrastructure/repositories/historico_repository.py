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
            criado_em=linha['criado_em'],
            titulo=linha['titulo'],
            descricao=linha['descricao'],
            arquivado=linha['arquivado'],
            # criado_em=linha['criado_em']  <-- Exemplo de outros campos
        )

    def atualizar_historico(self, historico: Historico):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()

        query = """
            UPDATE historico 
            SET titulo = ?, descricao = ?, arquivado = ?
            WHERE id = ?
        """

        cursor.execute(query, (
            historico.titulo,
            historico.descricao,
            historico.arquivado,
            historico.id
        ))

        conexao.commit()

    def listar_historicos_paciente(self, paciente_id):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()

        query = """
            SELECT id, paciente_id, titulo, descricao, arquivado, criado_em 
            FROM historico 
            WHERE paciente_id = ?
            ORDER BY criado_em DESC
        """

        cursor.execute(query, (paciente_id,))
        linhas = cursor.fetchall()

        lista_historicos = []

        for linha in linhas:

            historico = Historico(
                id=linha['id'],
                paciente_id=linha['paciente_id'],
                criado_em=linha['criado_em'],
                titulo=linha['titulo'],
                descricao=linha['descricao'],
                arquivado=linha['arquivado'],

            )
            lista_historicos.append(historico)

        return lista_historicos
