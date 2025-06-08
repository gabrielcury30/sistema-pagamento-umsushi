from clientes.endereco import Endereco
from clientes.clientes import Cliente
from abc import ABC, abstractmethod
from enum import Enum
import logging

# --- ENUMS ---
class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    RECUSADO = "Recusado"
    AGUARDANDO_PAGAMENTO = "Aguardar Pagamento na Entrega"

class TipoCartao(Enum):
    CREDITO = "Crédito"
    DEBITO = "Débito"

# --- Logger e Mensageria simples ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    def registrar(self, mensagem: str, nivel: str = "INFO"):
        getattr(logging, nivel.lower())(mensagem)

class Mensageria:
    def enviar_notificacao(self, mensagem: str):
        print(f"[Notificação] {mensagem}")

# --- Classe abstrata Pagamento ---
class Pagamento(ABC):
    def __init__(self, pedido, logger: Logger, mensageria: Mensageria):
        self.pedido = pedido
        self.logger = logger
        self.mensageria = mensageria
        self.status = StatusPagamento.PENDENTE
        pedido.definir_pagamento(self)  # liga o pagamento ao pedido

    @abstractmethod
    def processar_pagamento(self):
        pass