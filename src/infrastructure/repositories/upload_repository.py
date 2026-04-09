import os
import time
from src.domain.interfaces.upload_interface import IUploadRepository


class UploadRepository(IUploadRepository):
    def __init__(self, pasta_destino="uploads"):
        self.pasta_destino = pasta_destino
        os.makedirs(self.pasta_destino, exist_ok=True)

    def salvar_fisicamente(self, arquivo_bruto, nome_original) -> str:
        nome_unico = f"{int(time.time())}_{nome_original}"
        caminho_completo = os.path.join(self.pasta_destino, nome_unico)

        with open(caminho_completo, "wb") as f:
            f.write(arquivo_bruto)

        return f"/{self.pasta_destino}/{nome_unico}"
