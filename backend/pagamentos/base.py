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

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[{self._get_tipo()}] Iniciando pagamento para pedido {self.pedido.id}")
            self._realizar_cobranca()
            
            self.status = self._get_status_sucesso() 
            self.logger.registrar(f"[{self._get_tipo()}] Status definido como: {self.status.value}")
            self.mensageria.enviar_notificacao(
                f"Olá {self.pedido.cliente.nome}, o status do seu pagamento via {self._get_tipo()} é: {self.status.value}"
            )
        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[{self._get_tipo()}] Erro no pagamento: {e}", nivel="ERROR")
        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[{self._get_tipo()}] Recibo gerado:\n{recibo}")
            return self.status

@abstractmethod
def _get_tipo(self) -> str:
    pass

@abstractmethod
def _realizar_cobranca(self):
    pass

@abstractmethod
def _get_status_sucesso(self) -> StatusPagamento:
    pass