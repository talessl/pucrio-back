from datetime import datetime
from src.infrastructure.db.database import DatabaseInterface
from src.domain.interfaces.token_interface import ITokenRepository
from src.domain.entities import Token

class TokenRepository(ITokenRepository):
    
    def __init__(self, db: DatabaseInterface):
        self.db = db
    
    def buscar_por_codigo(self, codigo_token):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        query = "SELECT * FROM token WHERE valor = ?"
        
        cursor.execute(query, (codigo_token,))
        linha = cursor.fetchone()
        
        if not linha:
            return None
            
     
        return Token(
            id=linha['id'],
            valor=linha['valor'],
            historico_id=linha['historico_id'],
            criado_em=linha['criado_em'],
            expira_em=linha['expira_em'],
            revogado=linha['revogado']
        )
        
    def buscar_por_id(self, token_id: int):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM token WHERE id = ?", (token_id,))
        linha = cursor.fetchone()
        
        if not linha:
            return None
            
        return Token(
            id=linha['id'],
            valor=linha['valor'], 
            historico_id=linha['historico_id'],
            criado_em=linha['criado_em'],
            expira_em=linha['expira_em'],
            revogado=bool(linha['revogado'])
        )

    def atualizar_revogado(self, token):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        valor_revogado = 1 if token.revogado else 0
        
        cursor.execute("""
            UPDATE token 
            SET revogado = ? 
            WHERE id = ?
        """, (valor_revogado, token.id))
        
        conexao.commit()
        
    def salvar_token(self, token: Token) -> Token:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        query = """
            INSERT INTO token (valor, historico_id, criado_em, expira_em, revogado)
            VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            token.valor,
            token.historico_id,
            token.criado_em,
            token.expira_em,
            token.revogado 
        ))
        
        conexao.commit()
        
        token.id = cursor.lastrowid
        
        return token
        