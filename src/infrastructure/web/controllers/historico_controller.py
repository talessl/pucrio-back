from flask import Blueprint, request, jsonify
from src.domain.use_cases.arquivar_historico import ArquivarHistoricoUseCase
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio


historico_bp = Blueprint('historicos', __name__)


def iniciar_historico_controller(historico_use_case: ArquivarHistoricoUseCase):

    @historico_bp.route('/historico/<int:historico_id>/arquivar', methods=['PATCH'])
    @token_obrigatorio
    def arquivar_historico_paciente(paciente_logado_id, historico_id):

        try:
            historico_use_case.executar_arquivamento(
                paciente_logado_id=paciente_logado_id,
                historico_id=historico_id
            )

            return jsonify({"mensagem": "Histórico arquivado com sucesso!"}), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    return historico_bp
