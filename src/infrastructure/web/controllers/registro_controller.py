from flask import Blueprint, request, jsonify
from src.domain.use_cases.adicionar_registro_paciente import AdicionarRegistroPacienteInputDTO, AdicionarRegistroPacienteUseCase
from src.domain.use_cases.adicionar_registro_medico import AdicionarRegistroMedicoInputDTO, AdicionarRegistroMedicoUseCase
from src.domain.use_cases.validar_token import ValidarTokenAcessoUseCase
from src.domain.use_cases.listar_registros import listarRegistrosPacienteUseCase
from src.domain.use_cases.validar_dono_historico import ValidarDonoHistoricoUseCase
from src.domain.entities import RegistroTipo
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio

registro_bp = Blueprint('registros', __name__)


def iniciar_registro_controller(adicionar_registro_paciente_use_case: AdicionarRegistroPacienteUseCase,
                                adicionar_registro_medico_use_case: AdicionarRegistroMedicoUseCase,
                                validar_token_use_case: ValidarTokenAcessoUseCase,
                                listar_registros_use_case: listarRegistrosPacienteUseCase,
                                validar_dono_use_case: ValidarDonoHistoricoUseCase):

    @registro_bp.route('/medico/<codigo_token>', methods=['POST'])
    def criar_registro_medico(codigo_token):
        """
        Adiciona um diagnóstico/registro médico usando um token mágico.
        ---
        tags:
          - Registros Médico
        parameters:
          - in: path
            name: codigo_token
            type: string
            required: true
            description: Código do token de acesso do médico.
          - in: body
            name: body
            description: Dados do diagnóstico médico.
            required: true
            schema:
              type: object
              properties:
                autor_nome:
                  type: string
                  example: "Dr. Carlos Silva"
                autor_crm:
                  type: string
                  example: "123456/SP"
                tipo:
                  type: string
                  example: "diagnostico"
                conteudo:
                  type: string
                  example: "Paciente apresenta quadro de enxaqueca."
        responses:
          201:
            description: Diagnóstico médico salvo com sucesso.
          400:
            description: Erro de validação ou dados incompletos.
        """
        dados = request.get_json()

        autor_nome = dados.get('autor_nome')
        autor_crm = dados.get('autor_crm')

        if not autor_nome or not autor_crm:
            return jsonify({"erro": "O nome do médico e o CRM são de preenchimento obrigatório."}), 400

        try:
            dados_token = validar_token_use_case.executar_validacao(
                codigo_token)

            input_dto = AdicionarRegistroMedicoInputDTO(
                historico_id=dados_token['historico_id'],
                tipo=RegistroTipo(dados.get('tipo')),
                conteudo=dados.get('conteudo'),
                autor_crm=autor_crm,
                autor_nome=autor_nome
            )

            registro_salvo = adicionar_registro_medico_use_case.executar_adicao_registro_medico(
                input_dto)

            return jsonify({
                "mensagem": "Diagnóstico médico salvo com sucesso!",
                "id": registro_salvo.id
            }), 201

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @registro_bp.route('/medico/<codigo_token>', methods=['GET'])
    def listar_registros_medico(codigo_token):
        """
        Lista os registros de um histórico para o médico usando o token.
        ---
        tags:
          - Registros Médico
        parameters:
          - in: path
            name: codigo_token
            type: string
            required: true
            description: Código do token de acesso mágico.
        responses:
          200:
            description: Lista de registros recuperada com sucesso.
          404:
            description: Token inválido ou não encontrado.
        """
        try:
            dados_token = validar_token_use_case.executar_validacao(
                codigo_token)

            historico_id_seguro = dados_token['historico_id']
            lista_registros = listar_registros_use_case.executar_listagem(
                historico_id_seguro)

            return jsonify({
                "nome_medico": dados_token['descricao'],
                "expira_em": dados_token['expira_em'],
                "historico_id": historico_id_seguro,
                "registros": lista_registros
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @registro_bp.route('/paciente/historico/<int:historico_id>', methods=['GET'])
    @token_obrigatorio
    def listar_registros_paciente(paciente_logado_id, historico_id):
        """
        Lista os registros de um histórico específico do paciente.
        ---
        tags:
          - Registros Paciente
        security:
          - Bearer: []
        parameters:
          - in: path
            name: historico_id
            type: integer
            required: true
            description: ID do histórico do paciente.
        responses:
          200:
            description: Lista de registros recuperada com sucesso.
          400:
            description: Erro na listagem ou histórico não pertence ao usuário.
        """
        try:

            validar_dono_use_case.executar(
                paciente_logado_id=paciente_logado_id,
                historico_id=historico_id
            )

            lista_registros = listar_registros_use_case.executar_listagem(
                historico_id=historico_id
            )

            return jsonify({
                "historico_id": historico_id,
                "registros": [
                    {
                        "id": r.id,
                        "historico_id": r.historico_id,
                        "autor_tipo": r.autor_tipo,
                        "autor_nome": r.autor_nome,
                        "autor_crm": r.autor_crm,
                        "tipo": r.tipo,
                        "conteudo": r.conteudo,
                        "visivel": r.visivel,
                        "criado_em": str(r.criado_em)
                    }
                    for r in lista_registros
                ]
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    return registro_bp
