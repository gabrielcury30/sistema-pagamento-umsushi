from pagamentos.base import Pagamento, StatusPagamento, Logger, Mensageria, TipoCartao
import re, random
from datetime import datetime

class Cartao(Pagamento):
    def __init__(self, pedido, numero, titular, validade, cvv, tipo, logger, mensageria):
        super().__init__(pedido, logger, mensageria)
        self.numero   = numero
        self.titular  = titular
        self.validade = validade
        self.cvv      = cvv
        self.tipo     = tipo

    def _validar_validade(self):
        if not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", self.validade):
            raise ValueError("Validade inválida")
        mes, ano = self.validade.split("/")
        ano_completo = int("20" + ano)
        mes = int(mes)
        hoje = datetime.now()
        if ano_completo < hoje.year or (ano_completo == hoje.year and mes < hoje.month):
            raise ValueError("Cartão expirado")

    def _validar_cartao(self):
        if not re.fullmatch(r"\d{16}", self.numero):
            raise ValueError("Número do cartão inválido")
        if not re.fullmatch(r"\d{3}", self.cvv):
            raise ValueError("CVV inválido")
        self._validar_validade()

class CartaoCredito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, mensageria):
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.CREDITO, logger, mensageria)

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[CREDITO] Iniciando pagamento para pedido {self.pedido.id}")
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
            self.logger.registrar(f"[DEBITO] Iniciando pagamento para pedido {self.pedido.id}")
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