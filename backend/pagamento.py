from dataclasses import dataclass
from enum import Enum

# Criando um Enum para os métodos de pagamento
class MetodoPagamento(Enum):
    PIX = "Pix"
    CARTAO = "Cartão"
    DINHEIRO = "Dinheiro"

@dataclass
class ItemMenu:
    nome: str
    preco: float

menu = [ 
    ItemMenu("Ovo de salmão fresco", 75.90),
    ItemMenu("Ovo de salmão maçaricado", 75.90), 
    ItemMenu("Hot balls - queijo", 22.99)
]

class Carrinho:
    def __init__(self, usuario_id: str):
        self.usuario_id = usuario_id
        self.pedidos = []

    def adicionar_item(self, item: ItemMenu):
        self.pedidos.append(item)
    
    def remover_item(self, item: ItemMenu):
        if item in self.pedidos:
            self.pedidos.remove(item)

    def total_pedido(self) -> float:
        return sum(item.preco for item in self.pedidos)

class Pagamento:
    """Classe base para processar pagamentos"""
    def __init__(self, pedido: Carrinho):
        self.pedido = pedido
        self.status = "Pendente"

    def processar_pagamento(self):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

class Pix(Pagamento):
    """Classe para pagamento via Pix"""
    def __init__(self, pedido: Carrinho, chave_pix: str):
        super().__init__(pedido)
        self.chave_pix = chave_pix

    def processar_pagamento(self):
        if not self.pedido.pedidos:
            print("Erro: O carrinho está vazio!")
            return

        print(f"Pagamento via PIX iniciado para {self.pedido.usuario_id}. Total: R$ {self.pedido.total_pedido():.2f}")
        print(f"Use a chave PIX {self.chave_pix} para pagar.")
        self.status = "Pago"

class Cartao(Pagamento):
    """Classe para pagamento via Cartão"""
    def __init__(self, pedido: Carrinho, numero: str, cvv: str, validade: str, tipo: MetodoPagamento):
        super().__init__(pedido)
        self.numero = numero
        self.cvv = cvv
        self.validade = validade
        self.tipo = tipo

    def processar_pagamento(self):
        if not self.pedido.pedidos:
            print("Erro: O carrinho está vazio!")
            return

        print(f"Processando pagamento via Cartão ({self.tipo.value}) para {self.pedido.usuario_id}. Total: R$ {self.pedido.total_pedido():.2f}")
        self.status = "Pago"

class Dinheiro(Pagamento):
    """Classe para pagamento em Dinheiro"""
    def __init__(self, pedido: Carrinho, valor_recebido: float):
        super().__init__(pedido)
        self.valor_recebido = valor_recebido

    def processar_pagamento(self):
        total = self.pedido.total_pedido()
        if not self.pedido.pedidos:
            print("Erro: O carrinho está vazio!")
            return

        if self.valor_recebido < total:
            print(f"Erro: Valor insuficiente. Total: R$ {total:.2f}, recebido: R$ {self.valor_recebido:.2f}")
            return

        troco = self.valor_recebido - total
        print(f"Pagamento em dinheiro recebido de {self.pedido.usuario_id}. Total: R$ {total:.2f}")
        print(f"Valor recebido: R$ {self.valor_recebido:.2f} - Troco: R$ {troco:.2f}")
        print(f"Pagamento em dinheiro selecionado. O valor será recebido na entrega.")
        self.status = "Aguardando Pagamento"
	


# Criando um carrinho e adicionando itens
carrinho1 = Carrinho("Usuário João")
carrinho1.adicionar_item(menu[0])
carrinho1.adicionar_item(menu[2])

# Testando pagamento via PIX
pagamento_pix = Pix(carrinho1, "chave123456")
pagamento_pix.processar_pagamento()

# Testando pagamento via Cartão
pagamento_cartao = Cartao(carrinho1, "1234-5678-9012-3456", "123", "12/25", MetodoPagamento.CARTAO)
pagamento_cartao.processar_pagamento()

# Testando pagamento via Dinheiro
pagamento_dinheiro = Dinheiro(carrinho1, 150.0)
pagamento_dinheiro.processar_pagamento()