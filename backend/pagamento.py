from dataclasses import dataclass
from enum import Enum
import logging
import random

# Configuração de logging para registrar eventos, ao invés de print
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    PROCESSANDO = "Processando"
    PAGO = "Pago"
    FALHA = "Falha"
    AGUARDANDO_PAGAMENTO = "Aguardar Pagamento na Entrega"


# Criando um Enum para os métodos de pagamento
class MetodoPagamento(Enum):
    PIX = "Pix"
    CARTAO = "Cartão"
    DINHEIRO = "Dinheiro"

class PagamentoPixFalhou(Exception):
    pass

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
        self.status = StatusPagamento.PENDENTE

    def processar_pagamento(self):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

class Pix(Pagamento):
    """Classe para pagamento via Pix"""
    def __init__(self, pedido: Carrinho, chave_pix: str):
        super().__init__(pedido)
        self.chave_pix = chave_pix
        self.codigo_transacao = None # Adicionando código de transação via PIX

    def processar_pagamento(self):
        if not self.pedido.pedidos:
            logging.error("Erro: O carrinho está vazio!")
            return

        self.status = StatusPagamento.PROCESSANDO
        logging.info(f"Pagamento via PIX iniciado para {self.pedido.usuario_id}. Total: R$ {self.pedido.total_pedido():.2f}")
        logging.info(f"Use a chave PIX {self.chave_pix} para pagar.")
        
        # Simulação de pagamento com uma tratação de erros simples
        try:
            self.codigo_transacao = f"PIX-{random.randint(100000, 999999)}"       
            logging.info(f"Código de transação gerado: {self.codigo_transacao}")

            # Simulando um sucesso (90%) e falha (10%) aleatória com números apenas para teste
            if random.random() < 0.9:
                self.status = StatusPagamento.PAGO
                logging.info(f"Pagamento PIX para {self.pedido.usuario_id} APROVADO.")
            else:
                self.status = StatusPagamento.FALHA
                raise PagamentoPixFalhou("Falha na simulação do pagamento PIX")
        
        except PagamentoPixFalhou as e:
            logging.error(f"Erro no pagamento PIX: {e}")
        finally:
            logging.info(f"Status do pagamento PIX: {self.status.value}")

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
    def __init__(self, pedido: Carrinho, valor_recebido: float = None):
        super().__init__(pedido)
        self.valor_recebido = valor_recebido

    def processar_pagamento(self):
        total = self.pedido.total_pedido()
        if not self.pedido.pedidos:
            print("Erro: O carrinho está vazio!")
            return

        # Quando o pagamento em dinheiro é escolhido, o status é "Aguardando Pagamento"
        print(f"Pagamento em dinheiro selecionado. O pagamento será feito na entrega.")
        self.status = StatusPagamento.AGUARDANDO_PAGAMENTO
        print(f"Status inicial: {self.status.value}")

    def validar_pagamento(self):
        """Valida o pagamento ao receber o valor na entrega"""
        total = self.pedido.total_pedido()
        if self.valor_recebido is None:
            print("Erro: O pagamento ainda não foi realizado.")
            return

        if self.valor_recebido < total:
            print(f"Erro: Valor insuficiente. Total: R$ {total:.2f}, recebido: R$ {self.valor_recebido:.2f}")
            self.status = StatusPagamento.FALHA  
            return

        troco = self.valor_recebido - total
        print(f"Pagamento recebido de {self.pedido.usuario_id}. Total: R$ {total:.2f}")
        print(f"Valor recebido: R$ {self.valor_recebido:.2f} - Troco: R$ {troco:.2f}")
        self.status = StatusPagamento.PAGO 
        print(f"Status atualizado: {self.status.value}")


# Criando um carrinho e adicionando itens
carrinho1 = Carrinho("Usuário João")
carrinho1.adicionar_item(menu[0])
carrinho1.adicionar_item(menu[2])

# Testando pagamento via PIX
pagamento_pix = Pix(carrinho1, "chave123456")
pagamento_pix.processar_pagamento()
print()

# Testando pagamento via Cartão
pagamento_cartao = Cartao(carrinho1, "1234-5678-9012-3456", "123", "12/25", MetodoPagamento.CARTAO)
pagamento_cartao.processar_pagamento()
print()

# Testando pagamento via Dinheiro
pagamento_dinheiro = Dinheiro(carrinho1, 150.0)
pagamento_dinheiro.processar_pagamento()
pagamento_dinheiro.validar_pagamento()
print()