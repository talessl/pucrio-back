from flask import Blueprint, request, jsonify
from src.domain.entities import ArquivoTipo, AutorTipo
from src.domain.use_cases.adicionar_arquivo import AdicionarArquivoInputDTO
from src.infrastructure.web.middlewares.auth_middleware import token_obrigatorio

# Instanciamos o Blueprint (o agrupador de rotas do Flask)
arquivo_bp = Blueprint('arquivos', __name__)

def iniciar_arquivo_controller(use_case):
    """
    Função fábrica. Ela recebe o Use Case (injetado) e registra a rota.
    Isso garante que a rota tenha acesso ao 'use_case' sem usar variáveis globais.
    """
    
    @arquivo_bp.route('/', methods=['POST'])
    @token_obrigatorio
    def criar_arquivo(paciente_logado_id):
        dados = request.get_json()
        
        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400
        
        try:
      
            
            autor = AutorTipo(dados.get('enviado_por'))
            tipo_arquivo = ArquivoTipo(dados.get('tipo'))
        
            input_dto = AdicionarArquivoInputDTO(
            historico_id=dados.get('historico_id'),
            enviado_por=autor,
            tipo=tipo_arquivo,
            nome_original=dados.get('nome_original'),
            url=dados.get('url'),
            descricao=dados.get('descricao')
            )
            
            
            arquivo_salvo = use_case.adicionar_arquivo(
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

   
    return arquivo_bp