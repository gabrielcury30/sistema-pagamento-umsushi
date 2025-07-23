import random
from datetime import datetime
from services.pagamento_service import PagamentoService
# from services.clientes_factory import criar_cliente_teste
from clientes.cadastro import cadastrar_cliente
from services.pedidos_factory import criar_pedido_teste
from relatorios import relatorio_clientes, relatorio_pagamentos, relatorio_pedidos

def main():
    print("=" * 40)
    print("=== DEMONSTRAÇÃO COMPLETA DO SISTEMA ===")
    print("=" * 40)

    pagamento_service = PagamentoService()
    pedidos_finalizados = []

    # cliente1 = criar_cliente_teste(nome = "Ana Silva", email = "ana.silva@email.com")
    # cliente2 = criar_cliente_teste(nome = "Bruno Costa", email = "bruno.costa@email.com")
    cliente1 = cadastrar_cliente()
    cliente2 = cadastrar_cliente()

    itens_disponiveis = [
        ("Temaki de Salmão com Cream Cheese", 26.0), ("Temaki Hot Filadélfia", 39.90),
        ("Combinado de Sushi (24 peças)", 89.90), ("Sampa 3 (62 unidades)", 152.99),
        ("Refrigerante", 8.0), ("Suco Natural", 12.0)
    ]

    print("\n--- [FASE 1] Simulando 5 Transações da Loja ---")

    for i in range(5):
        print(f"\n--- Processando Transação #{i + 1} ---")

        cliente_da_vez = random.choice([cliente1, cliente2])
        itens_do_pedido = random.choices(itens_disponiveis, k = random.randint(1, 3))

        pedido = criar_pedido_teste(cliente = cliente_da_vez, itens = itens_do_pedido)

        pedido.data_pedido = datetime.now()

        metodos = [
            ("PIX", {"chave_pix": cliente_da_vez.email}),
            ("CARTAO_CREDITO", {"numero": "1111222233334444", "titular": cliente_da_vez.nome, "validade": "12/28", "cvv": "123"}),
            ("DINHEIRO", {"valor_pago": pedido.calcular_total() + 10})
        ]
        metodo, dados = random.choice(metodos)

        print(f"Pedido para '{cliente_da_vez.nome}' com total R${pedido.calcular_total(): .2f} via {metodo}")

        pagamento_service.processar_pagamento(pedido, metodo, dados)
        pedidos_finalizados.append(pedido)

        print("\n\n" + "=" * 40)
        print("=== [FASE 2] Gerando Relatórios com Base nas Transações ===")
        print("=" * 40)

        print("\n--- Relatórios de Pedidos ---")
        print("Quantidade por Status:", relatorio_pedidos.quantidade_por_status(pedidos_finalizados))
        print("Top 3 Itens Mais Vendidos:", relatorio_pedidos.itens_mais_vendidos(pedidos_finalizados, top_n = 3))

        print("\n--- Relatório de Pagamentos ---")
        print("Total Recebido (Aprovados) por Métodos:", relatorio_pagamentos.total_recebido_por_metodo(pedidos_finalizados))

        print("\n--- Relatório de Clientes ---")
        print("Total de Pedidos por Cliente:", relatorio_clientes.pedidos_por_cliente(pedidos_finalizados))
        print("Clientes Ativos (últimos 7 dias):", relatorio_clientes.clientes_ativos(pedidos_finalizados, dias = 7))

if __name__ == "__main__":
    main()
