# backend/main.py
from pagamentos.pix         import Pix
from pagamentos.cartao      import CartaoCredito, CartaoDebito
from pagamentos.dinheiro     import Dinheiro
from pagamentos.base        import Pedido, Logger, Mensageria

def processar_pix():
    logger     = Logger()
    mensageria = Mensageria()
    pedido     = Pedido("João", 120.50)
    pix        = Pix(pedido, "meu@email.com", logger, mensageria)
    pix.processar_pagamento()

def processar_cartao_credito():
    logger     = Logger()
    mensageria = Mensageria()
    pedido     = Pedido("Maria", 200.75)
    cc         = CartaoCredito(
        pedido,
        numero="1234567890123456",
        titular="Maria Silva",
        validade="12/26",
        cvv="123",
        logger=logger,
        mensageria=mensageria
    )
    cc.processar_pagamento()

def processar_cartao_debito():
    logger     = Logger()
    mensageria = Mensageria()
    pedido     = Pedido("Carlos", 150.00)
    cd         = CartaoDebito(
        pedido,
        numero="6543210987654321",
        titular="Carlos Souza",
        validade="11/25",
        cvv="321",
        logger=logger,
        mensageria=mensageria
    )
    cd.processar_pagamento()

def processar_dinheiro():
    logger = Logger()
    mensageria = Mensageria()
    pedido = Pedido("Rafael", 140.00)
    dinheiro = Dinheiro(pedido, 155.00, logger, mensageria)
    dinheiro.processar_pagamento()

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
