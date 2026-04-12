from flask import Blueprint, request, jsonify
from src.domain.use_cases.adicionar_historico import CriarHistoricoDTO
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio


historico_bp = Blueprint('historicos', __name__)


def iniciar_historico_controller(criar_historico_use_case, listar_use_case):

    @historico_bp.route('', methods=['POST'])
    @token_obrigatorio
    def criar_historico(paciente_logado_id):
        """
        Cria um novo histórico para o paciente logado.
        ---
        tags:
          - Históricos
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            description: Dados do histórico (O paciente_id é extraído automaticamente do seu Token).
            required: true
            schema:
              type: object
              properties:
                titulo:
                  type: string
                  example: "Acompanhamento Cardiológico"
                descricao:
                  type: string
                  example: "Exames de rotina e receituários do coração."
        responses:
          201:
            description: Histórico criado com sucesso.
          400:
            description: Erro na criação do histórico.
        """
        try:

            body = request.get_json()

            dados = CriarHistoricoDTO(
                titulo=body.get('titulo'),
                descricao=body.get('descricao'),
                paciente_id=paciente_logado_id
            )

            historico_criado = criar_historico_use_case.executar_adicao_historico(
                dados)

            return jsonify({
                "mensagem": "Histórico criado com sucesso",
                "historico": {
                    "id": historico_criado.id,
                    "paciente_id": historico_criado.paciente_id,
                    "titulo": historico_criado.titulo,
                    "descricao": historico_criado.descricao,
                    "arquivado": historico_criado.arquivado,
                    "criado_em": historico_criado.criado_em
                }

            }), 201

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

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
