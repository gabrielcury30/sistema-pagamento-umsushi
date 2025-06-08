from src.clientes import Cliente, Endereco  
import sys
sys.path.append("caminho_para_pasta_src")  # Substitua pelo caminho correto


from pedidos import Carrinho, ItemMenu
from pagamentos.pix import Pix

# Criando um cliente
cliente1 = Cliente("João Silva", "joao@email.com", "11999999999", Endereco("Rua A", 123, "Centro", "São Paulo", "12345-678", ""))

# Criando um pedido
carrinho1 = Carrinho(cliente1.nome)
carrinho1.adicionar_item(ItemMenu("Hot Balls - queijo", 22.99))

# Testando pagamento via PIX
pagamento_pix = Pix(carrinho1, "chave_pix123")
pagamento_pix.processar_pagamento()
