# Teste de formas de pagamentos.

from services.pagamento_service import PagamentoService
from clientes.clientes import Cliente
from clientes.endereco import Endereco
from pedido.item import Item
from pedido.pedido import Pedido

def criar_pedido(cliente_nome, email, telefone, rua, numero, bairro, cidade, cep, complemento, itens_info):
    endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
    cliente = Cliente(cliente_nome, email, telefone, endereco)
    itens = [Item(nome, preco) for nome, preco in itens_info]
    return Pedido(cliente, itens)

def exemplo_pagamento(metodo, dados_pagamento, cliente_info, endereco_info, itens_info):
    pedido = criar_pedido(*cliente_info, *endereco_info, itens_info)
    service = PagamentoService()
    status = service.processar_pagamento(pedido, metodo, dados_pagamento)

if __name__ == "__main__":
    print("Escolha o método de pagamento:")
    print("1. PIX")
    print("2. Cartão de Crédito")
    print("3. Cartão de Débito")
    print("4. Dinheiro")
    escolha = input("Digite 1, 2, 3 ou 4: \n")

    cliente_info = ("Ana Paula", "ana.paula@example.com", "11999998888")
    endereco_info = ("Rua das Flores", 101, "Jardim das Acácias", "São Paulo", "12345000", "")
    itens_info = [("Produto Teste", 120.50)]

    if escolha == "1":
        dados = {"chave_pix": "ana.paula@pix.com"}
        exemplo_pagamento("PIX", dados, cliente_info, endereco_info, itens_info)

    elif escolha == "2":
        dados = {
            "numero": "1234567890123456",
            "titular": "Ana Paula",
            "validade": "12/26",
            "cvv": "123"
        }
        exemplo_pagamento("CARTAO_CREDITO", dados, cliente_info, endereco_info, itens_info)

    elif escolha == "3":
        dados = {
            "numero": "6543210987654321",
            "titular": "Ana Paula",
            "validade": "11/25",
            "cvv": "321"
        }
        exemplo_pagamento("CARTAO_DEBITO", dados, cliente_info, endereco_info, itens_info)

    elif escolha == "4":
        dados = {"troco_para": 150.00}
        exemplo_pagamento("DINHEIRO", dados, cliente_info, endereco_info, itens_info)

    else:
        print("Opção inválida!")
