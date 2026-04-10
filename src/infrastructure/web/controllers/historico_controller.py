from flask import Blueprint, request, jsonify
from src.domain.use_cases.arquivar_historico import ArquivarHistoricoUseCase
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio


historico_bp = Blueprint('historicos', __name__)


def iniciar_historico_controller(historico_use_case: ArquivarHistoricoUseCase, listar_use_case):

    @historico_bp.route('/historico', methods=['GET'])
    @token_obrigatorio
    def listar_historicos_paciente(paciente_logado_id):
        """
        Lista todos os históricos do paciente logado.
        ---
        tags:
          - Históricos
        security:
          - Bearer: []
        responses:
          200:
            description: Lista de históricos recuperada com sucesso.
          400:
            description: Erro na busca dos históricos.
        """
        try:

            lista_historicos = listar_use_case.executar_listagem(
                paciente_id=paciente_logado_id)

            historicos_json = []
            for h in lista_historicos:
                historicos_json.append({
                    "id": h.id,
                    "paciente_id": h.paciente_id,
                    "titulo": h.titulo,
                    "descricao": h.descricao,
                    "arquivado": h.arquivado,
                    "criado_em": h.criado_em
                })

            return jsonify(historicos_json), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    return historico_bp
