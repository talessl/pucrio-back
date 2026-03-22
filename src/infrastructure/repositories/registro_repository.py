from src.infrastructure.db.database import DatabaseInterface
from src.domain.entities import Registro, AutorTipo, RegistroTipo
from src.domain.interfaces.registro_interface import IRegistroRepository


class RegistroRepository(IRegistroRepository):
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def salvar_registro(self, registro: Registro):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()

        query = """
            INSERT INTO registro (
                historico_id, 
                autor_tipo, 
                autor_nome, 
                autor_crm, 
                tipo, 
                conteudo, 
                visivel
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        valores = (
            registro.historico_id,
            registro.autor_tipo.value,  # ('medico' ou 'paciente')
            registro.autor_nome,
            registro.autor_crm,
            registro.tipo.value,       # ('diagnostico', 'conduta', etc)
            registro.conteudo,
            registro.visivel
        )

        cursor.execute(query, valores)
        conexao.commit()

        # id criado de volta para a entidade
        registro.id = cursor.lastrowid

        return registro

    def buscar_por_historico_id(self, historico_id: int) -> list:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()

        query = "SELECT * FROM registro WHERE historico_id = ? ORDER BY criado_em DESC"
        cursor.execute(query, (historico_id,))

        linhas = cursor.fetchall()

        lista_registros = []

        for linha in linhas:
            registro = Registro(
                id=linha['id'],
                historico_id=linha['historico_id'],
                autor_tipo=AutorTipo(linha['autor_tipo']).value,
                autor_nome=linha['autor_nome'],
                autor_crm=linha['autor_crm'],
                tipo=RegistroTipo(linha['tipo']).value,
                conteudo=linha['conteudo'],
                visivel=linha['visivel'],
                criado_em=linha['criado_em']
            )
            lista_registros.append(registro)

        return lista_registros
