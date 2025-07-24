# Módulo que define a classe Pedido para gerenciar pedidos de clientes.

import uuid
from datetime import datetime
from pagamentos.base import StatusPagamento
from clientes.clientes import Cliente
from .item import Item

class PedidoInvalidoException(Exception):
    """Exceção para pedidos inválidos."""
    pass

class Pedido:
    def __init__(self, cliente: Cliente, itens: list[Item]):
        """
        Inicializa um pedido com cliente e lista de itens,
        realizando validações básicas.
        """
        # --- Validações ---
        if not isinstance(cliente, Cliente):
            raise TypeError("cliente deve ser uma instância de Cliente.")

        if not isinstance(itens, list) or not all(isinstance(i, Item) for i in itens):
            raise TypeError("itens deve ser uma lista de instâncias da classe Item.")

        if not itens:
            raise PedidoInvalidoException("Não é possível criar um pedido sem itens.")

        # --- Atributos principais ---
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.itens = itens
        self.data_pedido = datetime.now()
        self.status_pagamento = StatusPagamento.PENDENTE
        self.pagamento = None

    def definir_pagamento(self, pagamento):
        """Associa um método de pagamento ao pedido."""
        self.pagamento = pagamento

    def calcular_total(self) -> float:
        """Calcula o valor total somando os preços de todos os itens do pedido."""
        return sum(item.preco for item in self.itens)

    def gerar_recibo(self) -> str:
        """
        Gera uma string formatada contendo os detalhes do pedido,
        itens, total, status e método de pagamento.
        """
        metodo = "N/A"
        valor_pago = troco = ""

        if self.pagamento:
            if hasattr(self.pagamento, 'tipo'):
                metodo = self.pagamento.tipo.value  # Enum (Cartão)
            elif self.pagamento.__class__.__name__ == "Dinheiro":
                metodo = "Dinheiro"
                valor_pago = f"Valor Pago: R${self.pagamento.valor_pago:.2f}\n"
                troco = f"Troco: R${self.pagamento.troco:.2f}\n"
            else:
                metodo = "PIX"

        itens_desc = "\n".join(f"- {item.nome}: R${item.preco:.2f}" for item in self.itens)
        total = self.calcular_total()

        return (
            f"--- Recibo {self.id} ---\n"
            f"Data: {self.data_pedido.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Cliente: {self.cliente.nome}\n"
            f"Endereço: {self.cliente.endereco.rua}, {self.cliente.endereco.numero}, "
            f"{self.cliente.endereco.bairro}, {self.cliente.endereco.cidade}\n"
            f"Itens:\n{itens_desc}\n"
            f"Total: R${total:.2f}\n"
            f"{valor_pago}{troco}"
            f"Status: {self.status_pagamento.value}\n"
            f"Método de Pagamento: {metodo}\n"
        )