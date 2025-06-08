import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="sistema_pagamento.log",  # Salvar os logs em um arquivo
    filemode="a"  
)

def registrar_evento(mensagem, nivel=logging.INFO):
  
    logging.log(nivel, mensagem)
