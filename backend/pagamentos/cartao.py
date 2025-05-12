# pagamentos/cartao.py
from .base import Pagamento, TipoCartao, StatusPagamento
import re, random

class Cartao(Pagamento):
    def __init__(self, pedido, numero, titular, validade, cvv, tipo, logger, mensageria):
        super().__init__(pedido, logger, mensageria)
        self.numero   = numero
        self.titular  = titular
        self.validade = validade
        self.cvv      = cvv
        self.tipo     = tipo

    def _validar_cartao(self):
        if not re.fullmatch(r"\d{16}", self.numero):
            raise ValueError("Número do cartão inválido")
        if not re.fullmatch(r"\d{3}", self.cvv):
            raise ValueError("CVV inválido")
        if not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", self.validade):
            raise ValueError("Validade inválida")

class CartaoCredito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, mensageria):
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.CREDITO, logger, mensageria)

    def processar_pagamento(self):
        try:
            self._validar_cartao()
            if random.random() < 0.85:
                self.status = StatusPagamento.APROVADO
            else:
                raise RuntimeError("Recusa pela operadora")
        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[CREDITO] {e}", nivel="ERROR")
        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[CREDITO] Recibo:\n{recibo}")
            return self.status

class CartaoDebito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, mensageria):
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.DEBITO, logger, mensageria)

    def processar_pagamento(self):
        try:
            self._validar_cartao()
            if random.random() < 0.95:
                self.status = StatusPagamento.APROVADO
            else:
                raise RuntimeError("Falha bancária")
        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[DEBITO] {e}", nivel="ERROR")
        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[DEBITO] Recibo:\n{recibo}")
            return self.status