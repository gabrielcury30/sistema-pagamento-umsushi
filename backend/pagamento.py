from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import re, random, uuid, logging

# --- CONFIGURAÇÃO DE LOGGING BÁSICA ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MetodoPagamento(Enum):
    PIX = "Pix"
    CARTAO = "Cartão"
    DINHEIRO = "Dinheiro"

# --- ENUMS ---
class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    RECUSADO = "Recusado"


# --- STUB PEDIDO (mínimo necessário) ---
class Pedido:
    def __init__(self, cliente_nome: str, total: float):
        self.id = str(uuid.uuid4())
        self.cliente_nome = cliente_nome
        self.valor_total = total
        self.data_pedido = datetime.now()
        self.status_pagamento = StatusPagamento.PENDENTE
        self.pagamento = None 
    
    def definir_pagamento(self, pagamento):
        self.pagamento = pagamento

    def gerar_recibo(self):
        if self.pagamento and self.status_pagamento == StatusPagamento.APROVADO:
            return (
            f"--- Recibo {self.id} ---\n"
            f"Data: {self.data_pedido}\n"
            f"Cliente: {self.cliente_nome}\n"
            f"Total: R${self.valor_total:.2f}\n"
            f"Status: {self.status_pagamento.value}\n"
            f"Método de Pagamento: {self.pagamento.metodo.value}\n"
            )
        return {"erro": "Pagamento não aprovado ou inexistente"}

# --- STUB LOGGER e MENSAGERIA ---
class Logger:
    def registrar(self, mensagem: str, nivel: str = "INFO"):
        getattr(logging, nivel.lower())(mensagem)


class Mensageria:
    def enviar_notificacao(self, mensagem: str):
        print(f"[Notificação] {mensagem}")


# --- CLASSE ABSTRATA DE PAGAMENTO ---
class Pagamento(ABC):
    def __init__(self, pedido: Pedido, logger: Logger, mensageria: Mensageria, metodo: MetodoPagamento):
        self.pedido = pedido
        self.logger = logger
        self.mensageria = mensageria
        self.status = StatusPagamento.PENDENTE
        self.metodo= metodo


    @abstractmethod
    def processar_pagamento(self):
        pass


# --- SUBCLASSE PIX ---
class Pix(Pagamento):
    def __init__(self, pedido: Pedido, chave_pix: str,
                 logger: Logger, mensageria: Mensageria):
        super().__init__(pedido, logger, mensageria, MetodoPagamento.PIX)
        self.chave_pix = chave_pix
        self.codigo_transacao = None
        

    def _validar_chave(self):
        padrao = r"[^@]+@[^@]+\.[^@]+|\d{11}|[0-9A-Fa-f]{32}"
        if not re.fullmatch(padrao, self.chave_pix):
            raise ValueError(f"Chave PIX inválida: {self.chave_pix}")

    def _gerar_qr_code(self) -> str:
        total_centavos = int(self.pedido.valor_total * 100)
        return f"PIX://{self.chave_pix}/{total_centavos}-{random.randint(0,9999)}"

    def processar_pagamento(self) -> str:
        try:
            self.logger.registrar(f"[PIX] Iniciando pagamento para pedido {self.pedido.id}")
            self._validar_chave()

            # Gera QR code
            self.codigo_transacao = self._gerar_qr_code()
            # Simula 90% de chance de aprovação
            if random.random() < 0.9:
                self.status = StatusPagamento.APROVADO
                self.logger.registrar(f"[PIX] Aprovado: {self.codigo_transacao}")
                self.mensageria.enviar_notificacao(
                    f"Olá {self.pedido.cliente_nome}, seu QR Code PIX é: {self.codigo_transacao}"
                )
            else:
                raise RuntimeError("Falha simulada no PIX")

        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[PIX] Recusado: {e}", nivel="ERROR")

        finally:
            # Gera recibo e registra
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[PIX] Recibo gerado:\n{recibo}")
            return self.codigo_transacao


# --- SUBCLASSES STUB: implementação posterior ---
class Cartao(Pagamento):
    pass


class Dinheiro(Pagamento):
    pass


# --- TESTE ---
if __name__ == "__main__":
    # Cria stubs
    logger = Logger()
    mensageria = Mensageria()

    # Cria um pedido simulado de R$ 120,50
    pedido = Pedido(cliente_nome="João", total=120.50)

    # Processa PIX
    pix = Pix(pedido, chave_pix="meu@email.com",
              logger=logger, mensageria=mensageria)
    pedido.definir_pagamento(pix)
    qr = pix.processar_pagamento()
    pedido.gerar_recibo()
    print(f"\nQR Code retornado: {qr}")
    