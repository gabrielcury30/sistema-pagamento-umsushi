# Teste para mosrtrar diferentes relatórios.

from datetime import datetime, timedelta
from pagamentos.base import StatusPagamento

from services.pedidos_factory import criar_pedido_teste
from services.clientes_factory import criar_cliente_teste

from relatorios.relatorio_pagamentos import total_recebido_por_metodo, pagamentos_pendentes
from relatorios.relatorio_pedidos import quantidade_por_status, pedidos_ultimos_dias
from relatorios.relatorio_clientes import pedidos_por_cliente, clientes_ativos

def criar_pedidos_demo():
    pedidos = []
    now = datetime.now()

    # DummyPag simula um pagamento para o relatório
    class DummyPag:
        def __init__(self, tipo): self._tipo = tipo
        def _get_tipo(self): return self._tipo

    cliente1 = criar_cliente_teste(nome="Maria", email="maria@teste.com")
    cliente2 = criar_cliente_teste(nome="João", email="joao@teste.com")

    # Pedido 1 - cliente1 - PIX
    pedido1 = criar_pedido_teste(cliente=cliente1, itens=[("A", 10), ("B", 20)])
    pedido1.status_pagamento = StatusPagamento.APROVADO
    pedido1.pagamento = DummyPag("PIX")
    pedido1.data_pedido = now - timedelta(days=2)
    pedidos.append(pedido1)

    # Pedido 2 - cliente1 - Cartão Crédito
    pedido2 = criar_pedido_teste(cliente=cliente1, itens=[("Z", 50)])
    pedido2.status_pagamento = StatusPagamento.APROVADO
    pedido2.pagamento = DummyPag("Cartão Crédito")
    pedido2.data_pedido = now - timedelta(days=1)
    pedidos.append(pedido2)

    # Pedido 3 - cliente2 - pendente
    pedido3 = criar_pedido_teste(cliente=cliente2, itens=[("C", 15)])
    # permanece com status PENDENTE
    pedidos.append(pedido3)

    return pedidos

if __name__ == "__main__":
    pedidos = criar_pedidos_demo()

    print("=== Relatório de Pagamentos ===")
    print("Total por método:", total_recebido_por_metodo(pedidos))
    print("Pagamentos pendentes:", [p.id for p in pagamentos_pendentes(pedidos)])

    print("\n=== Relatório de Pedidos ===")
    print("Quantidade por status:", quantidade_por_status(pedidos))
    print("Pedidos dos últimos 2 dias:", [p.id for p in pedidos_ultimos_dias(pedidos, dias=2)])

    print("\n=== Relatório de Clientes ===")
    print("Gasto por cliente:", pedidos_por_cliente(pedidos))
    print("Clientes ativos:", clientes_ativos(pedidos))