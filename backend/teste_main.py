# Testa todos os módulos em conjunto.
import random
from clientes.cadastro import cadastrar_cliente
from pedido.pedido import Pedido, Item
from pagamentos.pix import Pix
from pagamentos.cartao import CartaoCredito, CartaoDebito
from pagamentos.dinheiro import Dinheiro
from pagamentos.base import Logger, Mensageria

teste_rapido = True  # True para usar dados fixos, False para input manual.

print("=== Cadastro de Cliente ===")

def cadastrar_cliente():
    if teste_rapido:
        from clientes.endereco import Endereco
        from clientes.clientes import Cliente
        endereco = Endereco("Rua Teste", 123, "Bairro Teste", "Cidade Teste", "12345678", "Complemento Teste")
        cliente = Cliente("Teste Nome", "teste@email.com", "999999999", endereco)
        print(f"[Teste Rápido] Cliente criado: {cliente.nome}, {cliente.email}, {cliente.telefone}, {endereco.rua}, {endereco.numero}")
        return cliente

    # Código original com inputs
    # Nome
    nome = input("Nome: ")
    while nome.isdigit() or len(nome.strip()) < 2:
        print("Nome inválido. Deve conter letras e ter pelo menos 2 caracteres.")
        nome = input("Nome: ")

    # Email
    email = input("Email: ")
    while "@" not in email or "." not in email:
        print("Email inválido. Digite um email válido.")
        email = input("Email: ")

    # Telefone
    while True:
        telefone = input("Telefone (8-11 dígitos, somente números): ")
        try:
            _ = int(telefone)
            if len(telefone) < 8 or len(telefone) > 11:
                print("Telefone deve ter entre 8 e 11 dígitos.")
                continue
            break
        except ValueError:
            print("Telefone deve conter apenas números.")

    print("=== Endereço ===")
    from clientes.cadastro import validar_texto_com_letra

    rua    = validar_texto_com_letra(input("Rua: "), "Rua")
    bairro = validar_texto_com_letra(input("Bairro: "), "Bairro")
    cidade = validar_texto_com_letra(input("Cidade: "), "Cidade")

    while True:
        numero_str = input("Número: ")
        try:
            numero = int(numero_str)
            break
        except ValueError:
            print("Número deve ser um número inteiro.")

    while True:
        cep = input("CEP (8 dígitos numéricos): ")
        if cep.isdigit() and len(cep) == 8:
            break
        else:
            print("CEP inválido. Deve conter exatamente 8 números.")

    complemento = input("Complemento (opcional): ")

    from clientes.endereco import Endereco
    from clientes.clientes import Cliente
    endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
    cliente = Cliente(nome, email, telefone, endereco)
    return cliente


def criar_pedido(cliente):
    if teste_rapido:
        itens = [
            Item("Combinado de Salmão", 120.0),
            Item("Coca-Cola 1L", 8.0)
        ]
        pedido = Pedido(cliente=cliente, itens=itens)
        print(f"[Teste Rápido] Pedido criado para {cliente.nome} com os itens:")
        for item in pedido.itens:
            print(f" - {item.nome}: R${item.preco:.2f}")
        print(f"[Teste Rápido] Total do pedido: R${pedido.calcular_total():.2f}")
        return pedido

    while True:
        produto = input("Produto (ou ENTER para terminar): ")
        if not produto:
            break
        preco_str = input(f"Preço do {produto}: R$")
        try:
            preco = float(preco_str)
        except ValueError:
            print("Preço inválido. Digite um número.")
            continue
        item = Item(nome=produto, preco=preco)
        pedido.itens.append(item)

    print(f"Total do pedido: R${pedido.calcular_total():.2f}")
    return pedido


def escolher_pagamento(pedido, logger, mensageria):
    if teste_rapido:
        opcao = random.randint(1, 4)
        print(f"[Teste Rápido] Método de pagamento sorteado: {opcao}")

        if opcao == 1:
            chave = "teste-pix-chave"
            pagamento = Pix(pedido, chave, logger, mensageria)
            print("[Teste Rápido] Pagamento via PIX simulado.")
        elif opcao == 2:
            numero = "1111222233334444"
            titular = "Teste Cartao Credito"
            validade = "12/30"
            cvv = "123"
            pagamento = CartaoCredito(pedido, numero, titular, validade, cvv, logger, mensageria)
            print("[Teste Rápido] Pagamento via Cartão de Crédito simulado.")
        elif opcao == 3:
            numero = "5555666677778888"
            titular = "Teste Cartao Debito"
            validade = "11/29"
            cvv = "321"
            pagamento = CartaoDebito(pedido, numero, titular, validade, cvv, logger, mensageria)
            print("[Teste Rápido] Pagamento via Cartão de Débito simulado.")
        else:
            valor_pago = pedido.calcular_total() + 50.0  # valor pago maior para simular troco
            pagamento = Dinheiro(pedido, valor_pago, logger, mensageria)
            print(f"[Teste Rápido] Pagamento em dinheiro simulado com valor pago R${valor_pago:.2f}")
        
        return pagamento


def main():
    logger = Logger()
    mensageria = Mensageria()

    cliente = cadastrar_cliente()
    pedido = criar_pedido(cliente)

    print("\n=== Pagamento ===")
    pagamento = escolher_pagamento(pedido, logger, mensageria)
    if pagamento:
        status = pagamento.processar_pagamento()
        print(f"\nStatus do pagamento: {status.name}")
        print(pedido.gerar_recibo())
    else:
        print("Pagamento não realizado.")


if __name__ == "__main__":
    main()