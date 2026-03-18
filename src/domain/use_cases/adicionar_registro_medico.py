import re
from src.domain.entities import Registro
from src.domain.entities import AutorTipo, RegistroTipo
from src.domain.interfaces.registro_interface import IRegistroRepository
from dataclasses import dataclass


@dataclass
class AdicionarRegistroMedicoInputDTO:
    autor_nome: str
    autor_crm: str
    tipo: RegistroTipo
    conteudo: str
    historico_id: int


class AdicionarRegistroMedicoUseCase:
    def __init__(self, registro_repository: IRegistroRepository):
        self.registro_repository = registro_repository

    def executar_adicao_registro_medico(self, dados: AdicionarRegistroMedicoInputDTO):

        padrao_crm = re.compile(r'^\d{4,10}[-/ ]?[A-Z]{2}$')
        crm_limpo = dados.autor_crm.strip().upper()

        if not padrao_crm.match(crm_limpo):
            raise ValueError(
                "Formato de CRM inválido. Utilize o padrão com o estado, ex: '123456/SP'.")

        novo_registro = Registro(
            historico_id=dados.historico_id,
            id=None,
            autor_tipo=AutorTipo.MEDICO,
            autor_nome=dados.autor_nome,
            autor_crm=crm_limpo,
            tipo=dados.tipo,
            conteudo=dados.conteudo,
            visivel=True
        )

        registro_salvo = self.registro_repository.salvar_registro(
            novo_registro)

        return registro_salvo
