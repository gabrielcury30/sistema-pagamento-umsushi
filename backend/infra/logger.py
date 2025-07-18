# Logger simples para registrar mensagens em diferentes níveis.

import logging

class Logger:
    def __init__(self, log_file: str = None):  # <-- Correção aqui
        self.logger = logging.getLogger(__name__)  # <-- Correção aqui
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Arquivo (se aplicável)
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def registrar(self, mensagem: str, nivel: str = "INFO"):
        nivel = nivel.lower()
        if hasattr(self.logger, nivel):
            getattr(self.logger, nivel)(mensagem)
        else:
            self.logger.info(mensagem)