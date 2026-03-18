import os
from dotenv import load_dotenv

from functools import wraps
from flask import request, jsonify
import jwt

load_dotenv()
secret_key = os.getenv("SECRET_KEY")


def token_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            partes = auth_header.split(" ")

            if len(partes) == 2 and partes[0] == "Bearer":
                token = partes[1]

        if not token:
            return jsonify({"erro": "Token de acesso ausente"}), 401

        try:

            payload = jwt.decode(token, secret_key, algorithms=[
                                 "HS256"], options={"verify_sub": False})

            paciente_id = payload['sub']

        except jwt.ExpiredSignatureError as e:
            print(f"FALHA: Tempo expirado -> {str(e)}")
            return jsonify({"erro": "Token expirado", "detalhe_tecnico": str(e)}), 401

        except jwt.InvalidSignatureError as e:
            print(f"FALHA: Assinatura não bate -> {str(e)}")
            return jsonify({"erro": "Assinatura inválida (Chaves não batem)", "detalhe_tecnico": str(e)}), 401

        except jwt.DecodeError as e:
            print(f"FALHA: String mal formatada -> {str(e)}")
            return jsonify({"erro": "Formato do token incorreto", "detalhe_tecnico": str(e)}), 401

        except jwt.InvalidTokenError as e:
            print(f"FALHA: Erro genérico do JWT -> {str(e)}")
            return jsonify({"erro": "Token inválido", "detalhe_tecnico": str(e)}), 401

        return f(paciente_logado_id=paciente_id, *args, **kwargs)

    return decorated_function
