# pagamentos/base.py
from clientes.endereco import Endereco
from clientes.clientes import Cliente
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid, logging

# --- CONFIGURAÇÃO DE LOGGING BÁSICA ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- ENUMS ---
class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    RECUSADO = "Recusado"
    AGUARDANDO_PAGAMENTO = "Aguardar Pagamento na Entrega"

class TipoCartao(Enum):
    CREDITO = "Crédito"
    DEBITO = "Débito"

# --- STUB PEDIDO (mínimo necessário) ---
class Pedido:
    def __init__(self, cliente: Cliente, total: float):
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.total = total
        self.data_pedido = datetime.now()
        self.status_pagamento = StatusPagamento.PENDENTE
        self.pagamento = None

    def definir_pagamento(self, pagamento):
        self.pagamento = pagamento

    def calcular_total(self) -> float:
        return self.total

    def gerar_recibo(self) -> str:
        if not self.pagamento:
            metodo = "N/A"
            valor_pago = troco = ""

        else:
            valor_pago = ""
            troco = ""
            
            if hasattr(self.pagamento, 'tipo'):
                metodo = self.pagamento.tipo.value
            elif self.pagamento.__class__.__name__ == "Dinheiro":
                metodo = "Dinheiro"
                valor_pago = f"Valor Pago: R${self.pagamento.valor_pago:.2f}\n"
                troco = f"Troco: R${self.pagamento.troco:.2f}\n"
            else:
                metodo = "PIX"

        return (
            f"--- Recibo {self.id} ---\n"
            f"Data: {self.data_pedido.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Cliente: {self.cliente.nome}\n"
            f"Endereço: {self.cliente.endereco.rua}, {self.cliente.endereco.numero}, {self.cliente.endereco.bairro}, {self.cliente.endereco.cidade}\n"
            f"Total: R${self.total:.2f}\n"
            f"{valor_pago}{troco}"
            f"Status: {self.status_pagamento.value}\n"
            f"Método de Pagamento: {metodo}\n"
        )


# --- STUB LOGGER e MENSAGERIA ---
class Logger:
    def registrar(self, mensagem: str, nivel: str = "INFO"):
        getattr(logging, nivel.lower())(mensagem)

class Mensageria:
    def enviar_notificacao(self, mensagem: str):
        print(f"[Notificação] {mensagem}")

# --- CLASSE ABSTRATA ---
class Pagamento(ABC):
    def __init__(self, pedido: Pedido, logger: Logger, mensageria: Mensageria):
        self.pedido = pedido
        self.logger = logger
        self.mensageria = mensageria
        self.status = StatusPagamento.PENDENTE
        pedido.definir_pagamento(self)

    @abstractmethod
    def processar_pagamento(self):
        pass
