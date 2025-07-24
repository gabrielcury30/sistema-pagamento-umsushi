# Módulo para validação e processamento de pagamentos com cartão.

import re
import random
from datetime import datetime
from abc import ABC
from pagamentos.base import Pagamento, StatusPagamento, TipoCartao

class ValidacaoCartaoException(Exception):
    """Erro de validação dos dados do cartão."""
    pass

def validar_nome_titular(nome: str) -> str:
    """Valida se o nome do titular contém nome e sobrenome com pelo menos 2 letras cada."""
    partes = nome.strip().split()
    if len(partes) < 2 or any(len(part) < 2 for part in partes):
        raise ValidacaoCartaoException("Nome do titular deve conter nome e sobrenome (mínimo 2 letras cada)")
    if not all(part.isalpha() for part in partes):
        raise ValidacaoCartaoException("Nome do titular deve conter apenas letras")
    return " ".join(partes)

class Cartao(Pagamento, ABC):
    def __init__(self, pedido, numero, titular, validade, cvv, tipo: TipoCartao, logger, notificacao):
        """Inicializa os dados do cartão sem validar ainda."""
        super().__init__(pedido, logger, notificacao)
        self.numero = numero
        self.titular = titular
        self.validade = validade
        self.cvv = cvv
        self.tipo = tipo

    def _get_status_sucesso(self) -> StatusPagamento:
        return StatusPagamento.APROVADO

    def _validar_cartao(self):
        validar_nome_titular(self.titular)
        if not re.fullmatch(r"\d{16}", self.numero):
            raise ValidacaoCartaoException("Número do cartão deve conter 16 dígitos numéricos.")
        if not re.fullmatch(r"\d{3}", self.cvv):
            raise ValidacaoCartaoException("CVV deve conter 3 dígitos numéricos.")
        self._validar_validade()

    def _validar_validade(self):
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", self.validade):
            raise ValidacaoCartaoException("Validade deve estar no formato MM/AA.")
        mes, ano = map(int, self.validade.split("/"))
        ano_completo = 2000 + ano
        hoje = datetime.now()
        if ano_completo < hoje.year or (ano_completo == hoje.year and mes < hoje.month):
            raise ValidacaoCartaoException("Cartão expirado.")
        

class CartaoCredito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, notificacao):
        """Configura um pagamento com cartão de crédito."""
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.CREDITO, logger, notificacao)

    def _get_tipo(self) -> str:
        """Retorna o tipo do cartão como crédito."""
        return self.tipo.value

    def _realizar_cobranca(self):
        """Valida o cartão e simula a cobrança, com 15% de chance de recusa."""
        self._validar_cartao()

        if random.random() >= 0.85:
            raise RuntimeError("Pagamento recusado pela operadora do cartão de crédito.")

class CartaoDebito(Cartao):
    def __init__(self, pedido, numero, titular, validade, cvv, logger, notificacao):
        """Configura um pagamento com cartão de débito."""
        super().__init__(pedido, numero, titular, validade, cvv, TipoCartao.DEBITO, logger, notificacao)

    def _get_tipo(self) -> str:
        """Retorna o tipo do cartão como débito."""
        return self.tipo.value

    def _realizar_cobranca(self):
        """Valida o cartão e simula a cobrança, com 5% de chance de recusa."""
        self._validar_cartao()

        if random.random() >= 0.95:
            raise RuntimeError("Pagamento recusado pela operadora do cartão de débito.")