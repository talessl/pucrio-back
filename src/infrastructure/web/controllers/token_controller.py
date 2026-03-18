from flask import Blueprint, request, jsonify
from src.domain.use_cases.validar_token import ValidarTokenAcessoUseCase
from src.domain.use_cases.revogar_token import RevogarTokenUseCase
from src.domain.use_cases.gerar_token import GerarTokenInputDTO, GerarTokenUseCase
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio


token_bp = Blueprint('tokens', __name__)

def iniciar_token_controller(validar_use_case: ValidarTokenAcessoUseCase, revogar_use_case: RevogarTokenUseCase, gerar_token_use_case: GerarTokenUseCase):
    
    @token_bp.route('/medico/<codigo_token>', methods=['GET'])
    def validar_link_medico(codigo_token):
        try:
            dados_token = validar_use_case.executar_validacao(codigo_token)
            
            return jsonify({
                "mensagem": "Token válido!",
                "token": dados_token
            }), 200
            
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404 
        
    
    @token_bp.route('/paciente/<int:token_id>/revogar', methods=['PATCH'])
    @token_obrigatorio 
    def revogar_acesso_medico(paciente_logado_id, token_id):
        try:
            revogar_use_case.executar_revogacao(paciente_logado_id, token_id)
            
            return jsonify({"mensagem": "Acesso revogado com sucesso. O link não é mais válido."}), 200
            
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        
    
    @token_bp.route('/', methods=['POST'])
    @token_obrigatorio 
    def gerar_token_acesso(paciente_logado_id):
        dados = request.get_json()
        
        try:
            input_dto = GerarTokenInputDTO(
                historico_id=dados.get('historico_id'),
                horas_validade=dados.get('horas_validade', 24) 
            )
            
            token_gerado = gerar_token_use_case.executar_criacao(paciente_logado_id, input_dto)
            
            url_magica = f"https://seusite.com/acesso-medico/{token_gerado.valor}"
            
            return jsonify({
                "mensagem": "Link mágico gerado com sucesso!",
                "token": token_gerado.valor,
                "link_whatsapp": url_magica,
                "expira_em": token_gerado.expira_em
            }), 201
            
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400
        
    return token_bp

