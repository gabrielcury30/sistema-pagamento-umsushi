# Módulo de geração de relatórios e estatísticas sobre pedidos.

from pedido.pedido import Pedido
from typing import List, Dict
from datetime import datetime, timedelta

def quantidade_por_status(pedidos: List[Pedido]) -> Dict[str, int]:
    """
    Retorna quantos pedidos existem em cada status (Pendente, Aprovado, etc).
    """
    contagem: Dict[str, int] = {}
    for pedido in pedidos:
        status = pedido.status_pagamento.value
        contagem[status] = contagem.get(status, 0) + 1
    return contagem

def itens_mais_vendidos(pedidos: List[Pedido], top_n: int = 5) -> List[Dict[str, float]]:
    """
    Retorna os top_n itens mais vendidos e a quantidade vendida de cada um.
    """
    vendas: Dict[str, int] = {}
    for pedido in pedidos:
        for item in pedido.itens:
            vendas[item.nome] = vendas.get(item.nome, 0) + 1
    # ordenar por quantidade
    mais = sorted(vendas.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    return [{"nome": nome, "quantidade": qtd} for nome, qtd in mais]

def relatorio_receita_por_pedido(pedidos: List[Pedido]) -> List[Dict[str, float]]:
    """
    Para cada pedido, retorna id e valor total.
    """
    return [{"pedido_id": p.id, "total": p.calcular_total()} for p in pedidos]

def pedidos_ultimos_dias(pedidos, dias=7):
    """
    Retorna os pedidos no período dos últimos 7 dias.
    """
    limite = datetime.now() - timedelta(days=dias)
    return [p for p in pedidos if p.data_pedido >= limite]
