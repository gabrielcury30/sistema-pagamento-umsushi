# Usa um pedido e tenta pagar, gerando recibo atualizado.
from clientes.clientes import Cliente
from clientes.endereco import Endereco
from pedido.item import Item
from pedido.pedido import Pedido
from pagamentos.pix import Pix
from pagamentos.cartao import CartaoCredito, CartaoDebito
from pagamentos.dinheiro import Dinheiro
from pagamentos.base import Logger, Mensageria

def processar_pix():
    logger     = Logger()
    mensageria = Mensageria()
    endereco_dummy = Endereco("Rua das Flores", 101, "Jardim das Acácias", "São Paulo", "12345000", "")
    cliente_dummy  = Cliente("Ana Paula", "ana.paula@example.com", "11999998888", endereco_dummy)

    itens = [Item("Produto Teste", 120.50)]
    pedido = Pedido(cliente_dummy, itens)
    chave_pix = "ana.paula@pix.com"
    pix = Pix(pedido, chave_pix, logger, mensageria)
    pix.processar_pagamento()
    print(pedido.gerar_recibo())

def processar_cartao_credito():
    logger     = Logger()
    mensageria = Mensageria()
    endereco_dummy = Endereco("Av. Teste", 123, "Bairro Teste", "Cidade Teste", "00000000", "")
    cliente_dummy  = Cliente("Maria Silva", "maria@teste.com", "81999990000", endereco_dummy)

    itens = [Item("Produto A", 200.75)]
    pedido = Pedido(cliente_dummy, itens)
    cc = CartaoCredito(
        pedido,
        numero="1234567890123456",
        titular=cliente_dummy.nome,
        validade="12/26",
        cvv="123",
        logger=logger,
        mensageria=mensageria
    )
    cc.processar_pagamento()
    print(pedido.gerar_recibo())

def processar_cartao_debito():
    logger     = Logger()
    mensageria = Mensageria()
    endereco_dummy = Endereco("Rua Exemplo", 456, "Bairro Exemplo", "Cidade Exemplo", "11111111", "")
    cliente_dummy  = Cliente("Carlos Souza", "carlos@teste.com", "81988880000", endereco_dummy)

    itens = [Item("Produto B", 150.00)]
    pedido = Pedido(cliente_dummy, itens)
    cd = CartaoDebito(
        pedido,
        numero="6543210987654321",
        titular=cliente_dummy.nome,
        validade="11/25",
        cvv="321",
        logger=logger,
        mensageria=mensageria
    )
    cd.processar_pagamento()
    print(pedido.gerar_recibo())

def processar_dinheiro():
    logger     = Logger()
    mensageria = Mensageria()
    endereco_dummy = Endereco("Travessa Teste", 789, "Bairro Legal", "Cidade Legal", "22222222", "")
    cliente_dummy  = Cliente("Rafael Lima", "rafael@teste.com", "81977770000", endereco_dummy)

    itens = [Item("Produto C", 140.00)]
    pedido = Pedido(cliente_dummy, itens)
    dinheiro = Dinheiro(pedido, 155.00, logger, mensageria)
    dinheiro.processar_pagamento()
    print(pedido.gerar_recibo())

if __name__ == "__main__":
    print("Escolha o método de pagamento:")
    print("1. PIX")
    print("2. Cartão de Crédito")
    print("3. Cartão de Débito")
    print("4. Dinheiro")
    escolha = input("Digite 1, 2, 3 ou 4: ")

    if escolha == "1":
        processar_pix()
    elif escolha == "2":
        processar_cartao_credito()
    elif escolha == "3":
        processar_cartao_debito()
    elif escolha == "4":
        processar_dinheiro()
    else:
        print("Opção inválida!")