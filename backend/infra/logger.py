# Logger simples para registrar mensagens em diferentes níveis.

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    def _init_(self, log_file: str = None):
        """Inicializa o logger com opção de arquivo de log."""
        self.logger = logging.getLogger(_name_)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Handler para console
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # Handler para arquivo, se especificado
        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def registrar(self, mensagem: str, nivel: str = "INFO"):
        nivel = nivel.upper()
        if hasattr(self.logger, nivel.lower()):
            getattr(self.logger, nivel.lower())(mensagem)
        else:
            self.logger.info(mensagem)