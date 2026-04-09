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

    def listar_por_historico(self, historico_id: int) -> list:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()

        query = "SELECT * FROM arquivo WHERE historico_id = ? ORDER BY id DESC"
        cursor.execute(query, (historico_id,))

        linhas = cursor.fetchall()

        lista_arquivos = []

        for linha in linhas:
            arquivo = Arquivo(
                id=linha['id'],
                historico_id=linha['historico_id'],
                enviado_por=linha['enviado_por'],
                tipo=linha['tipo'],
                nome_original=linha['nome_original'],
                url=linha['url'],
                descricao=linha['descricao'],
                visivel=linha['visivel'],
                criado_em=linha['criado_em']
            )
            lista_arquivos.append(arquivo)

        return lista_arquivos
