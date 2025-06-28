# Logger simples para registrar mensagens em diferentes níveis.

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    def registrar(self, mensagem: str, nivel: str = "INFO"):
        nivel = nivel.lower()
        if hasattr(logging, nivel):
            getattr(logging, nivel)(mensagem)
        else:
            logging.info(mensagem)
