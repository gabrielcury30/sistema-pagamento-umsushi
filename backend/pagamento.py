from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import re, random, uuid, logging
import requests
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
        self.total = total
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
            f"Total: R${self.total:.2f}\n"
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
        total_centavos = int(self.pedido.total * 100)
        return f"PIX://{self.chave_pix}/{total_centavos}-{random.randint(0,9999)}"
 
    def processar_pagamento(self) -> str:
        try:
            self.logger.registrar(f"[PIX] Iniciando pagamento para pedido {self.pedido.id}")
            self._validar_chave()

        # Gera QR code 
            self.codigo_transacao = self._gerar_qr_code()

        # Chama a API externa
            resp = requests.get("https://yesno.wtf/api", timeout=5)
            resp.raise_for_status()
            data = resp.json()

            # Decide aprovação com base no "answer" ("yes" : aprovado, "no" : recusado)
            if data.get("answer") == "yes":
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
            # Atualiza o pedido e gera recibo
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[PIX] Recibo gerado:\n{recibo}")
            return self.codigo_transacao

# --- SUBCLASSE CARTÃO ---
class Cartao(Pagamento):
    def __init__(self, pedido: Pedido, numero_cartao: str, nome_titular: str,
                 validade: str, cvv: str, logger: Logger, mensageria: Mensageria, metodo: MetodoPagamento):
        super().__init__(pedido, logger, mensageria, metodo)
        self.numero_cartao = numero_cartao
        self.nome_titular = nome_titular
        self.validade = validade
        self.cvv = cvv

    def _validar_cartao(self):
        if not re.fullmatch(r"\d{16}", self.numero_cartao):
            raise ValueError("Número do cartão inválido")
        if not re.fullmatch(r"\d{3}", self.cvv):
            raise ValueError("CVV inválido")
        if not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", self.validade):
            raise ValueError("Validade inválida")

# --- SUBCLASSE CARTÃO DE CRÉDITO ---
class CartaoCredito(Cartao):
    def __init__(self, pedido: Pedido, numero_cartao: str, nome_titular: str,
                 validade: str, cvv: str, logger: Logger, mensageria: Mensageria):
        super().__init__(pedido, numero_cartao, nome_titular, validade, cvv,
                         logger, mensageria, MetodoPagamento.CARTAO)

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[CRÉDITO] Processando pagamento para pedido {self.pedido.id}")
            self._validar_cartao()

            

            if random.random() < 0.85:
                self.status = StatusPagamento.APROVADO
                self.logger.registrar("[CRÉDITO] Pagamento aprovado.")
                self.mensageria.enviar_notificacao(f"Pagamento no crédito aprovado para {self.pedido.cliente_nome}")
            else:
                raise RuntimeError("Transação recusada pela operadora")

        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[CRÉDITO] Pagamento recusado: {e}", nivel="ERROR")

        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[CRÉDITO] Recibo gerado:\n{recibo}")
            return self.status


# --- SUBCLASSE CARTÃO DE DÉBITO ---
class CartaoDebito(Cartao):
    def __init__(self, pedido: Pedido, numero_cartao: str, nome_titular: str,
                 validade: str, cvv: str, logger: Logger, mensageria: Mensageria):
        super().__init__(pedido, numero_cartao, nome_titular, validade, cvv,
                         logger, mensageria, MetodoPagamento.CARTAO)

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[DÉBITO] Processando pagamento para pedido {self.pedido.id}")
            self._validar_cartao()

            

            if random.random() < 0.95:
                self.status = StatusPagamento.APROVADO
                self.logger.registrar("[DÉBITO] Pagamento aprovado.")
                self.mensageria.enviar_notificacao(f"Pagamento no débito aprovado para {self.pedido.cliente_nome}")
            else:
                raise RuntimeError("Falha na autenticação bancária")

        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[DÉBITO] Pagamento recusado: {e}", nivel="ERROR")

        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[DÉBITO] Recibo gerado:\n{recibo}")
            return self.status

class Dinheiro(Pagamento):
    pass


# --- TESTE ---
if __name__ == "__main__":
    # Cria stubs
    logger = Logger()
    mensageria = Mensageria()

    # Cria um pedido simulado de R$ 120,50
    pedido = Pedido("João", 120.50)

    # Processa PIX
    pix = Pix(pedido, "meu@email.com",
              logger, mensageria)
    pedido.definir_pagamento(pix)
    qr = pix.processar_pagamento()
    pedido.gerar_recibo()
    print(f"\nQR Code retornado: {qr}")

    
     # Processa CARTÃO DE CRÉDITO
    cartao_credito = CartaoCredito(pedido, numero_cartao="1234567812345678",
                                   nome_titular="Joao da Silva", validade="12/26", cvv="123",
                                   logger=logger, mensageria=mensageria)
    pedido.definir_pagamento(cartao_credito)
    cartao_credito.processar_pagamento()
    print(pedido.gerar_recibo())

    
    # OU CARTÃO DE DÉBITO
    cartao_debito = CartaoDebito(pedido, numero_cartao="8765432187654321",
                                  nome_titular="Joao da Silva", validade="11/25", cvv="321",
                                  logger=logger, mensageria=mensageria)
    pedido.definir_pagamento(cartao_debito)
    cartao_debito.processar_pagamento()
    print(pedido.gerar_recibo())

    