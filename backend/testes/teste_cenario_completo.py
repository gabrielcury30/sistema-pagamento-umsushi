# Teste com todas funcionalidades do projeto (cadastro, pedidos, pagamento, exceções e relatórios)

import random
from datetime import datetime
from services.pagamento_service import PagamentoService
from clientes.cadastro import cadastrar_cliente
from services.pedidos_factory import criar_pedido_teste
from relatorios import relatorio_clientes, relatorio_pagamentos, relatorio_pedidos

def main():
    print("=" * 50)
    print("=== DEMONSTRAÇÃO COMPLETA DO SISTEMA ===")
    print("=" * 50)

    pagamento_service = PagamentoService()
    pedidos_finalizados = []

    print("\n>>> Cadastre 2 clientes:\n")
    cliente1 = cadastrar_cliente()
    cliente2 = cadastrar_cliente()

    # Lista fixa de itens para pedidos
    itens_disponiveis = [
        ("Temaki de Salmão com Cream Cheese", 26.0),
        ("Temaki Hot Filadélfia", 39.90),
        ("Combinado de Sushi (24 peças)", 89.90),
        ("Sampa 3 (62 unidades)", 152.99),
        ("Refrigerante", 8.0),
        ("Suco Natural", 12.0)
    ]

    print("\n>>> Simulando 5 Transações Aleatórias\n")

    for i in range(5):
        print(f"\n--- Transação #{i + 1} ---")

        cliente = random.choice([cliente1, cliente2])
        itens_pedido = random.choices(itens_disponiveis, k=random.randint(1, 3))

        pedido = criar_pedido_teste(cliente=cliente, itens=itens_pedido)
        pedido.data_pedido = datetime.now()

        # Definindo métodos de pagamento possíveis
        metodos = [
            ("PIX", {"chave_pix": cliente.email}),
            ("CARTAO_CREDITO", {"numero": "1111222233334444", "titular": cliente.nome, "validade": "12/28", "cvv": "123"}),
            ("CARTAO_DEBITO", {"numero": "5555666677778888", "titular": cliente.nome, "validade": "11/29", "cvv": "321"}),
            ("DINHEIRO", {"valor_pago": pedido.calcular_total() + 10})
        ]
        metodo, dados_pagamento = random.choice(metodos)

        print(f"Pedido para {cliente.nome} no valor de R${pedido.calcular_total():.2f} via {metodo}")

        try:
            status = pagamento_service.processar_pagamento(pedido, metodo, dados_pagamento)
            pedidos_finalizados.append(pedido)

            if status.name == "APROVADO":
                print("Pagamento aprovado com sucesso!")
            elif status.name == "RECUSADO":
                print("Pagamento recusado.")
            else:
                print(f"Pagamento finalizado com status inesperado: {status.name}")
        except Exception as e:
            print(f"Erro ao processar pagamento: {e}")

    print("\n" + "=" * 50)
    print("=== RELATÓRIOS FINAIS ===")
    print("=" * 50)

    # Relatório de pedidos
    print("\n--- Relatório de Pedidos Após as Transações---")
    print("Quantidade por Status:", relatorio_pedidos.quantidade_por_status(pedidos_finalizados))
    print("Top 3 Itens Mais Vendidos:", relatorio_pedidos.itens_mais_vendidos(pedidos_finalizados, top_n=3))

    # Relatório de pagamentos
    print("\n--- Relatório de Pagamentos ---")
    total_recebido = relatorio_pagamentos.total_recebido_por_metodo(pedidos_finalizados)
    total_recebido_rounded = {metodo: round(valor, 2) for metodo, valor in total_recebido.items()}

    print("Total Recebido por Método:", total_recebido_rounded)

    # Relatório de clientes
    print("\n--- Relatório de Clientes ---")
    print("Pedidos por Cliente:", relatorio_clientes.pedidos_por_cliente(pedidos_finalizados))
    print("Clientes Ativos (últimos 7 dias):", relatorio_clientes.clientes_ativos(pedidos_finalizados, dias=7))

if __name__ == "__main__":
    main()