from flask import Blueprint, request, jsonify
from src.domain.use_cases.cadastrar_paciente import CadastrarPacienteInputDTO
from src.domain.use_cases.fazer_login import FazerLoginDTO

auth_bp = Blueprint('auth', __name__)


def iniciar_auth_controller(login_use_case, cadastrar_paciente_use_case):
    """
    Função fábrica para injetar o Use Case de Login na rota.
    """

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Realiza o login do paciente.
        ---
        tags:
          - Autenticação
        parameters:
          - in: body
            name: body
            description: Credenciais de acesso do paciente.
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: "joao@email.com"
                senha:
                  type: string
                  example: "senha123"
        responses:
          200:
            description: Login realizado com sucesso.
          400:
            description: E-mail e senha são obrigatórios.
          401:
            description: Credenciais inválidas.
        """
        dados = request.get_json()

        if not dados or not dados.get('email') or not dados.get('senha'):
            return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

        try:
            login_dto = FazerLoginDTO(
                email=dados.get('email'),
                senha=dados.get('senha')
            )

            token_gerado = login_use_case.executar_login(login_dto)

            return jsonify({
                "mensagem": "Login realizado com sucesso",
                "token": token_gerado
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 401

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"erro": "Erro interno no servidor"}), 500

    @auth_bp.route('/cadastrar', methods=['POST'])
    def cadastrar():
        """
        Cadastra um novo paciente no sistema.
        ---
        tags:
          - Autenticação
        parameters:
          - in: body
            name: body
            description: Dados do novo paciente.
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  example: "João Silva"
                email:
                  type: string
                  example: "joao@email.com"
                senha:
                  type: string
                  example: "senha123"
        responses:
          201:
            description: Paciente cadastrado com sucesso.
          400:
            description: Dados incompletos ou inválidos.
        """
        dados = request.get_json()

        if not dados or not dados.get('nome') or not dados.get('email') or not dados.get('senha'):
            return jsonify({"erro": "Nome, e-mail e senha são obrigatórios"}), 400

        try:
            input_dto = CadastrarPacienteInputDTO(
                nome=dados['nome'],
                email=dados['email'],
                senha=dados['senha']
            )

            paciente_salvo = cadastrar_paciente_use_case.executar_cadastro(
                input_dto)

            return jsonify({
                "mensagem": "Paciente cadastrado com sucesso!",
                "id": paciente_salvo.id,
                "nome": paciente_salvo.nome
            }), 201

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    return auth_bp
