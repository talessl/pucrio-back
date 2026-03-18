from src.domain.interfaces.paciente_interface import IPacienteRepository
from src.infrastructure.db.database import DatabaseInterface
from src.domain.entities import Paciente

class PacienteRepository(IPacienteRepository):
    def __init__(self, db: DatabaseInterface):
        self.db = db
        
    def buscar_paciente_por_email(self, email):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        query = """
            SELECT id, nome, email, senha 
            FROM paciente 
            WHERE email = ?
        """
        cursor.execute(query, (email,))
        linha = cursor.fetchone()
        
        if not linha:
            return None
        
        paciente_encontrado = Paciente(
            id=linha['id'],
            nome=linha['nome'],
            email=linha['email'],
            senha=linha['senha'] 
        )
        
        return paciente_encontrado
    
    def buscar_paciente_por_id(self, paciente_id):
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM paciente WHERE id = ?", (paciente_id,))
        linha = cursor.fetchone()
        
        if not linha:
            return None
            
        return Paciente(
            id=linha['id'],
            nome=linha['nome'],
            email=linha['email'],
            senha=linha['senha']
        )
        
    def salvar_paciente(self, paciente: Paciente) -> Paciente:
        conexao = self.db.get_connection()
        cursor = conexao.cursor()
        
        cursor.execute(
            "INSERT INTO paciente (nome, email, senha) VALUES (?, ?, ?)",
            (paciente.nome, paciente.email, paciente.senha)
        )
        conexao.commit()
        
        paciente.id = cursor.lastrowid
        return paciente