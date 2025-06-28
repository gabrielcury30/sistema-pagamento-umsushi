# Testa as formas de pagamentos.
from services.pagamento_service import PagamentoService
from services.clientes_factory import criar_cliente_teste
from services.pedidos_factory import criar_pedido_teste

def exemplo_pagamento(metodo, dados_pagamento):
    cliente = criar_cliente_teste()
    pedido = criar_pedido_teste(cliente)
    service = PagamentoService()
    status = service.processar_pagamento(pedido, metodo, dados_pagamento)
    print(pedido.gerar_recibo())

if __name__ == "__main__":
    print("Escolha o método de pagamento:")
    print("1. PIX")
    print("2. Cartão de Crédito")
    print("3. Cartão de Débito")
    print("4. Dinheiro")
    escolha = input("Digite 1, 2, 3 ou 4: ")

    if escolha == "1":
        dados = {"chave_pix": "ana.paula@pix.com"}
        exemplo_pagamento("PIX", dados)

    elif escolha == "2":
        dados = {
            "numero": "1234567890123456",
            "titular": "Ana Paula",
            "validade": "12/26",
            "cvv": "123"
        }
        exemplo_pagamento("CARTAO_CREDITO", dados)

    elif escolha == "3":
        dados = {
            "numero": "6543210987654321",
            "titular": "Ana Paula",
            "validade": "11/25",
            "cvv": "321"
        }
        exemplo_pagamento("CARTAO_DEBITO", dados)

    elif escolha == "4":
        dados = {"troco_para": 150.00}
        exemplo_pagamento("DINHEIRO", dados)

    else:
        print("Opção inválida!")
