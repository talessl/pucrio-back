import os
from flask import Blueprint, request, jsonify, send_from_directory
from src.domain.entities import ArquivoTipo, AutorTipo
from src.domain.use_cases.adicionar_arquivo import AdicionarArquivoInputDTO
from src.domain.use_cases.validar_token import ValidarTokenAcessoUseCase
from src.domain.use_cases.listar_arquivos import ListarArquivosUseCase
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio

arquivo_bp = Blueprint('arquivos', __name__)


def iniciar_arquivo_controller(use_case, listar_arquivos_use_case: ListarArquivosUseCase, validar_token_use_case: ValidarTokenAcessoUseCase, validar_dono_use_case):
    """
    Função fábrica. Ela recebe o Use Case (injetado) e registra a rota.
    Isso garante que a rota tenha acesso ao 'use_case' sem usar variáveis globais.
    """

    @arquivo_bp.route('/paciente/<int:historico_id>', methods=['POST'])
    @token_obrigatorio
    def criar_arquivo_paciente(paciente_logado_id, historico_id):
        """
    Adiciona um arquivo ao histórico do paciente autenticado.
    ---
    tags:
      - Arquivos Paciente
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: historico_id
        type: integer
        required: true
        description: ID do histórico do paciente.
      - in: formData
        name: arquivo
        type: file
        required: true
        description: Arquivo a ser enviado.
      - in: formData
        name: tipo
        type: string
        required: true
        description: Tipo do arquivo.
      - in: formData
        name: descricao
        type: string
        required: false
        description: Descrição do arquivo.
      - in: formData
        name: enviado_por
        type: string
        required: true
        description: Autor do envio.
    responses:
      201:
        description: Arquivo criado com sucesso.
      400:
        description: Dados inválidos ou histórico não pertence ao usuário.
      500:
        description: Erro interno ao processar o arquivo.
    """
        dados = request.form
        arquivo = request.files.get('arquivo')

        if not arquivo or arquivo.filename == '':
            return jsonify({"erro": "Nenhum arquivo enviado."}), 400

        arquivo_bruto = arquivo.read()
        nome_original = arquivo.filename

        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        try:
            validar_dono_use_case.executar(
                paciente_logado_id=paciente_logado_id,
                historico_id=historico_id
            )

            autor = AutorTipo(dados.get('enviado_por'))
            tipo_arquivo = ArquivoTipo(dados.get('tipo'))

            input_dto = AdicionarArquivoInputDTO(
                historico_id=historico_id,
                enviado_por=autor,
                tipo=tipo_arquivo,
                nome_original=nome_original,
                url=dados.get('url'),
                descricao=dados.get('descricao'),
                arquivo_bruto=arquivo_bruto
            )

            arquivo_salvo = use_case.executar_adicao_arquivo(input_dto)

            return jsonify({
                "id": arquivo_salvo.id,
                "status": "sucesso"
            }), 201

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            return jsonify({"erro": "Erro interno ao processar o arquivo", "detalhes": str(e)}), 500

    @arquivo_bp.route('/medico/<codigo_token>', methods=['POST'])
    def criar_arquivo_medico(codigo_token):
        """
    Adiciona um arquivo ao histórico via token de acesso médico.
    ---
    tags:
      - Arquivos Médico
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: codigo_token
        type: string
        required: true
        description: Token de acesso médico válido.
      - in: formData
        name: arquivo
        type: file
        required: true
        description: Arquivo a ser enviado.
      - in: formData
        name: tipo
        type: string
        required: true
        description: Tipo do arquivo.
      - in: formData
        name: descricao
        type: string
        required: false
        description: Descrição do arquivo.
      - in: formData
        name: enviado_por
        type: string
        required: true
        description: Autor do envio.
    responses:
      201:
        description: Arquivo criado com sucesso.
      400:
        description: Token inválido ou dados incorretos.
      500:
        description: Erro interno ao processar o arquivo.
    """
        dados_token = validar_token_use_case.executar_validacao(
            codigo=codigo_token)
        historico_id_seguro = dados_token['historico_id']

        dados = request.form
        arquivo = request.files.get('arquivo')

        if not arquivo or arquivo.filename == '':
            return jsonify({"erro": "Nenhum arquivo enviado."}), 400

        arquivo_bruto = arquivo.read()
        nome_original = arquivo.filename

        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}),

        try:

            autor = AutorTipo(dados.get('enviado_por'))
            tipo_arquivo = ArquivoTipo(dados.get('tipo'))

            input_dto = AdicionarArquivoInputDTO(
                historico_id=historico_id_seguro,
                enviado_por=autor,
                tipo=tipo_arquivo,
                nome_original=nome_original,
                url=dados.get('url'),
                descricao=dados.get('descricao'),
                arquivo_bruto=arquivo_bruto
            )

            arquivo_salvo = use_case.executar_adicao_arquivo(
                input_dto
            )

            return jsonify({
                "id": arquivo_salvo.id,
                "status": "sucesso"
            }), 201

        except ValueError as e:

            return jsonify({"erro": str(e)}), 400
        except Exception as e:

            import traceback
            traceback.print_exc()

            return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

    @arquivo_bp.route('/medico/<codigo_token>', methods=['GET'])
    def listar_arquivos_medico(codigo_token):
        """
    Lista os arquivos de um histórico via token de acesso médico.
    ---
    tags:
      - Arquivos Médico
    parameters:
      - in: path
        name: codigo_token
        type: string
        required: true
        description: Token de acesso médico válido.
    responses:
      200:
        description: Lista de arquivos recuperada com sucesso.
      404:
        description: Token inválido ou histórico não encontrado.
    """
        try:
            dados_token = validar_token_use_case.executar_validacao(
                codigo=codigo_token)
            historico_id_seguro = dados_token['historico_id']

            lista_arquivos = listar_arquivos_use_case.executar_listagem(
                historico_id=historico_id_seguro)

            return jsonify({
                "historico_id": historico_id_seguro,
                "arquivos": [
                    {
                        "id": arquivo.id,
                        "nome_original": arquivo.nome_original,
                        "url": arquivo.url,
                        "tipo": arquivo.tipo.value if hasattr(arquivo.tipo, 'value') else arquivo.tipo,
                        "enviado_por": arquivo.enviado_por.value if hasattr(arquivo.enviado_por, 'value') else arquivo.enviado_por,
                        "descricao": arquivo.descricao,
                        "criado_em": str(arquivo.criado_em)
                    } for arquivo in lista_arquivos
                ]
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @arquivo_bp.route('/paciente/historico/<int:historico_id>', methods=['GET'])
    @token_obrigatorio
    def listar_arquivos_paciente(paciente_logado_id, historico_id):
        """
    Lista os arquivos de um histórico específico do paciente autenticado.
    ---
    tags:
      - Arquivos Paciente
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
        description: Lista de arquivos recuperada com sucesso.
      400:
        description: Erro na listagem ou histórico não pertence ao usuário.
    """
        try:
            validar_dono_use_case.executar(
                paciente_logado_id=paciente_logado_id,
                historico_id=historico_id
            )

            lista_arquivos = listar_arquivos_use_case.executar_listagem(
                historico_id=historico_id)

            return jsonify({
                "historico_id": historico_id,
                "arquivos": [
                    {
                        "id": arquivo.id,
                        "nome_original": arquivo.nome_original,
                        "url": arquivo.url,
                        "tipo": arquivo.tipo.value if hasattr(arquivo.tipo, 'value') else arquivo.tipo,
                        "enviado_por": arquivo.enviado_por.value if hasattr(arquivo.enviado_por, 'value') else arquivo.enviado_por,
                        "descricao": arquivo.descricao,
                        "criado_em": str(arquivo.criado_em)
                    } for arquivo in lista_arquivos
                ]
            }), 200

        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @arquivo_bp.route('/assets/uploads/<nome_arquivo>', methods=['GET'])
    def servir_arquivo(nome_arquivo):
        """
    Serve um arquivo estático da pasta de uploads.
    ---
    tags: 
      - Arquivos
    parameters:
      - in: path
        name: nome_arquivo
        type: string
        required: true
        description: Nome do arquivo a ser servido.
    responses:
      200:
        description: Arquivo retornado com sucesso.
      404:
        description: Arquivo não encontrado.
    """
        pasta = os.path.join(os.getcwd(), 'assets', 'uploads')
        return send_from_directory(pasta, nome_arquivo)

    return arquivo_bp
