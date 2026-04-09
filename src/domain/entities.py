from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime


class ArquivoTipo(Enum):
    EXAME = "exame"
    LAUDO = "laudo"
    DOCUMENTO = "documento"


class RegistroTipo(Enum):
    DIAGNOSTICO = "diagnostico"
    CONDUTA = "conduta"
    INFORMACAO = "informacao"
    SINTOMA = "sintoma"


class AutorTipo(Enum):
    MEDICO = "medico"
    PACIENTE = "paciente"


@dataclass
class Paciente:
    nome: str
    email: str
    senha: str
    id: Optional[int] = None


@dataclass
class Arquivo:
    tipo: ArquivoTipo
    url: str
    enviado_por: str
    historico_id: int
    nome_original: str
    descricao: str
    visivel: int = 1
    criado_em: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Historico:
    paciente_id: int
    criado_em: str
    titulo: str
    arquivado: int = 0
    descricao: Optional[str] = None
    id: Optional[int] = None

    def arquivar(self):
        self.arquivado = 1


@dataclass
class Registro:
    historico_id: int
    autor_tipo: AutorTipo
    autor_nome: str
    tipo: RegistroTipo
    conteudo: str
    criado_em: Optional[str] = None
    autor_crm: Optional[str] = None
    visivel: Optional[int] = 1
    id: int = 1


@dataclass
class Token:
    valor: str
    historico_id: int
    criado_em: str
    expira_em: str
    descricao: str
    revogado: int = 0
    id: Optional[int] = None

    def esta_valido(self) -> bool:
        """
        Verifica se o momento atual é menor que a data de expiração do token.
        """
        agora = datetime.now()

        if self.revogado == 1:
            return False

        if isinstance(self.expira_em, str):
            data_expiracao = datetime.strptime(
                self.expira_em, "%Y-%m-%d %H:%M:%S")
        else:
            data_expiracao = self.expira_em

        return agora < data_expiracao

    def revogar(self):
        """Cancela o acesso deste token imediatamente."""
        self.revogado = 1
