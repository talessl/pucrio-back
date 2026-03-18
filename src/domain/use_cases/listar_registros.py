from src.domain.interfaces.registro_interface import IRegistroRepository


class ListarRegistrosUseCase:
    def __init__(self, registro_repository: IRegistroRepository):
        self.registro_repository = registro_repository

    def executar_listagem(self, historico_id: int):
        registros = self.registro_repository.buscar_por_historico_id(
            historico_id)

        resultado = []
        for reg in registros:
            resultado.append({
                "id": reg.id,
                "tipo": reg.tipo.value,
                "conteudo": reg.conteudo,
                "autor_tipo": reg.autor_tipo.value,
                "criado_em": reg.criado_em
            })

        return resultado
