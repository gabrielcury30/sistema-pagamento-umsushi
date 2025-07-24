# Módulo de geração de relatórios e estatísticas sobre clientes.

from clientes.clientes import Cliente
from pedido.pedido import Pedido
from typing import List, Dict
from collections import Counter
from datetime import datetime, timedelta

def pedidos_por_cliente(pedidos: List[Pedido]) -> Dict[str, int]:
    """
    Quantidade de pedidos feitos por cada cliente (nome ou email).
    """
    contador = Counter()
    for p in pedidos:
        contador[p.cliente.email] += 1
    return dict(contador)

def gasto_medio_por_cliente(pedidos: List[Pedido]) -> Dict[str, float]:
    """
    Gasto médio por cliente (soma de totais / número de pedidos).
    """
    soma: Dict[str, float] = {}
    conta: Dict[str, int] = {}
    for p in pedidos:
        chave = p.cliente.email
        soma[chave] = soma.get(chave, 0.0) + p.calcular_total()
        conta[chave] = conta.get(chave, 0) + 1
    return {c: soma[c] / conta[c] for c in soma}

def clientes_ativos(pedidos, dias=7):
    """
    Lista os emails de clientes com pelo menos 'minimo' pedidos.
    """
    limite = datetime.now() - timedelta(days=dias)
    ativos = {p.cliente.email for p in pedidos if p.data_pedido >= limite}
    return list(ativos)