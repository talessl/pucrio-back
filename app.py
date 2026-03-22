import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from src.infrastructure.db.sqlite_database import SQLiteDatabase
from src.infrastructure.db.setup import setup_database

# repositories
from src.infrastructure.repositories.arquivo_repository import ArquivoRepository
from src.infrastructure.repositories.paciente_repository import PacienteRepository
from src.infrastructure.repositories.registro_repository import RegistroRepository
from src.infrastructure.repositories.token_repository import TokenRepository
from src.infrastructure.repositories.historico_repository import HistoricoRepository

# adapters
from src.infrastructure.repositories.auth.flask_password_hasher import FlaskPasswordHasher
from src.infrastructure.repositories.auth.jwt_auth_generator import JwtAuthGenerator

# usecases
from src.domain.use_cases.adicionar_arquivo import AdicionarArquivoUseCase
from src.domain.use_cases.fazer_login import FazerLoginUseCase
from src.domain.use_cases.adicionar_registro_paciente import AdicionarRegistroPacienteUseCase
from src.domain.use_cases.adicionar_registro_medico import AdicionarRegistroMedicoUseCase
from src.domain.use_cases.validar_token import ValidarTokenAcessoUseCase
from src.domain.use_cases.revogar_token import RevogarTokenUseCase
from src.domain.use_cases.cadastrar_paciente import CadastrarPacienteUseCase
from src.domain.use_cases.gerar_token import GerarTokenUseCase
from src.domain.use_cases.listar_registros import ListarRegistrosUseCase
from src.domain.use_cases.arquivar_historico import ArquivarHistoricoUseCase
from src.domain.use_cases.validar_dono_historico import ValidarDonoHistoricoUseCase
from src.domain.use_cases.listar_historicos_paciente import ListarHistoricosPacienteUseCase


# controllers
from src.infrastructure.web.controllers.arquivo_controller import iniciar_arquivo_controller
from src.infrastructure.web.controllers.auth_controller import iniciar_auth_controller
from src.infrastructure.web.controllers.registro_controller import iniciar_registro_controller
from src.infrastructure.web.controllers.token_controller import iniciar_token_controller
from src.infrastructure.web.controllers.historico_controller import iniciar_historico_controller


"""
1. Conexao/Criacao do banco de dados
2. Injetar dependencias (banco, repositorios)
3. Iniciar controllers
"""


def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")

    db = SQLiteDatabase("database.db")
    setup_database(db)

    jwt = JwtAuthGenerator(secret_key=secret_key, expiracao_horas=72)
    hasher = FlaskPasswordHasher()

    # repositorios
    arquivo_repository = ArquivoRepository(db)
    paciente_repository = PacienteRepository(db)
    registro_repository = RegistroRepository(db)
    token_repository = TokenRepository(db)
    historico_repository = HistoricoRepository(db)

    # usecases
    adicionar_arquivo_use_case = AdicionarArquivoUseCase(arquivo_repository)
    login_use_case = FazerLoginUseCase(
        paciente_repository, hasher=hasher, auth=jwt)
    adicionar_registro_paciente_use_case = AdicionarRegistroPacienteUseCase(
        registro_repository, paciente_repository=paciente_repository)
    adicionar_registro_medico_use_case = AdicionarRegistroMedicoUseCase(
        registro_repository=registro_repository)
    validar_token_use_case = ValidarTokenAcessoUseCase(
        token_repository=token_repository)
    revogar_token_use_case = RevogarTokenUseCase(
        token_repository=token_repository, historico_repository=historico_repository)
    cadastrar_paciente_use_case = CadastrarPacienteUseCase(
        hasher=hasher, paciente_repository=paciente_repository)
    gerar_token_use_case = GerarTokenUseCase(
        token_repository=token_repository, historico_repository=historico_repository)
    listar_registros_use_case = ListarRegistrosUseCase(
        registro_repository=registro_repository)
    arquivar_historico_use_case = ArquivarHistoricoUseCase(
        historico_repository)
    validar_dono_use_case = ValidarDonoHistoricoUseCase(historico_repository)
    listar_historicos_paciente_use_case = ListarHistoricosPacienteUseCase(
        historico_repository)

    # controllers
    auth_blueprint = iniciar_auth_controller(
        login_use_case, cadastrar_paciente_use_case=cadastrar_paciente_use_case)
    arquivo_blueprint = iniciar_arquivo_controller(adicionar_arquivo_use_case)
    registro_blueprint = iniciar_registro_controller(
        adicionar_registro_paciente_use_case, adicionar_registro_medico_use_case, validar_token_use_case=validar_token_use_case, listar_registros_use_case=listar_registros_use_case, validar_dono_use_case=validar_dono_use_case)
    token_blueprint = iniciar_token_controller(
        validar_token_use_case, revogar_token_use_case, gerar_token_use_case, validar_dono_historico=validar_dono_use_case)
    historico_blueprint = iniciar_historico_controller(
        arquivar_historico_use_case, listar_historicos_paciente_use_case)

    # rotas
    app.register_blueprint(arquivo_blueprint, url_prefix='/arquivos')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(registro_blueprint, url_prefix='/registros')
    app.register_blueprint(token_blueprint, url_prefix='/tokens')
    app.register_blueprint(historico_blueprint, url_prefix='/historicos')

    return app


if __name__ == '__main__':
    meu_app = create_app()
    meu_app.run(debug=True)
