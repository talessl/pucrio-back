from flask import Blueprint, request, jsonify
from src.domain.use_cases.adicionar_registro_paciente import AdicionarRegistroPacienteInputDTO, AdicionarRegistroPacienteUseCase
from src.domain.use_cases.adicionar_registro_medico import AdicionarRegistroMedicoInputDTO, AdicionarRegistroMedicoUseCase
from src.domain.use_cases.validar_token import ValidarTokenAcessoUseCase
from src.domain.use_cases.listar_registros import ListarRegistrosUseCase
from src.domain.use_cases.validar_dono_historico import ValidarDonoHistoricoUseCase
from src.domain.entities import RegistroTipo
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio

registro_bp = Blueprint('registros', __name__)


def iniciar_registro_controller(adicionar_registro_paciente_use_case: AdicionarRegistroPacienteUseCase,
                                adicionar_registro_medico_use_case: AdicionarRegistroMedicoUseCase,
                                validar_token_use_case: ValidarTokenAcessoUseCase,
                                listar_registros_use_case: ListarRegistrosUseCase,
                                validar_dono_use_case: ValidarDonoHistoricoUseCase):

    @registro_bp.route('/paciente', methods=['POST'])
    @token_obrigatorio
    def criar_registro_paciente(paciente_logado_id):
        dados = request.get_json()

        try:

            input_dto = AdicionarRegistroPacienteInputDTO(
                historico_id=dados.get('historico_id'),
                tipo=RegistroTipo(dados.get('tipo')),
                conteudo=dados.get('conteudo')
            )

            registro_salvo = adicionar_registro_paciente_use_case.executar_adicao_registro_paciente(
                paciente_logado_id, input_dto)

            return jsonify({"mensagem": "Registro criado", "id": registro_salvo.id}), 201

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @registro_bp.route('/medico/<codigo_token>', methods=['POST'])
    def criar_registro_medico(codigo_token):
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
        try:
            dados_token = validar_token_use_case.executar_validacao(
                codigo_token)

            historico_id_seguro = dados_token['historico_id']
            lista_registros = listar_registros_use_case.executar_listagem(
                historico_id_seguro)

            return jsonify({
                "historico_id": historico_id_seguro,
                "registros": lista_registros
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @registro_bp.route('/paciente/historico/<int:historico_id>', methods=['GET'])
    @token_obrigatorio
    def listar_registros_paciente(paciente_logado_id, historico_id):
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
                        "autor_tipo": r.autor_tipo.value,
                        "autor_nome": r.autor_nome,
                        "autor_crm": r.autor_crm,
                        "tipo": r.tipo.value,
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
