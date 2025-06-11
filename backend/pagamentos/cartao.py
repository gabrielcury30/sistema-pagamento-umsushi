from pagamentos.base import Pagamento, StatusPagamento, Logger, Mensageria, TipoCartao
import re, random
from datetime import datetime
from abc import ABC, abstractmethod

class Cartao(Pagamento, ABC):
    def __init__(self, pedido, numero, titular, validade, cvv, tipo, logger, mensageria):
        super().__init__(pedido, logger, mensageria)
        self.numero   = numero
        self.titular  = titular
        self.validade = validade
        self.cvv      = cvv
        self.tipo     = tipo

    def _get_status_sucesso(self) -> StatusPagamento:
        return StatusPagamento.APROVADO

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

    def _get_tipo(self) -> str:
        return "CREDITO"

    def _realizar_cobranca(self):
        self._validar_cartao()
        if random.random() >= 0.85:
            raise RuntimeError("Recusa pela operadora do cartão de crédito")


class CartaoDebito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, mensageria):
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.DEBITO, logger, mensageria)

    def _get_tipo(self) -> str:
        return "DEBITO"
    
    def _realizar_cobranca(self):
        self._validar_cartao()
        if random.random() >= 0.95:
            raise RuntimeError("Recusa pela operadora do cartão de débito")