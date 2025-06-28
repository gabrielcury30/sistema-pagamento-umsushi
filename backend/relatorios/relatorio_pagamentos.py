# Módulo de geração de relatórios e estatísticas sobre pagamentos.

from datetime import datetime
from pagamentos.base import StatusPagamento
from pedido.pedido import Pedido
from typing import List, Dict

def total_recebido_por_metodo(pedidos: List[Pedido]) -> Dict[str, float]:
    """
    Retorna um dicionário com o total recebido por cada método de pagamento.
    Ex: {"PIX": 1200.0, "Cartão Crédito": 2500.0, ...}
    """
    resumo: Dict[str, float] = {}
    for pedido in pedidos:
        if pedido.status_pagamento == StatusPagamento.APROVADO:
            metodo = pedido.pagamento._get_tipo()
            resumo.setdefault(metodo, 0.0)
            resumo[metodo] += pedido.calcular_total()
    return resumo

def pagamentos_pendentes(pedidos: List[Pedido]) -> List[Pedido]:
    """
    Retorna a lista de pedidos cujo status de pagamento é PENDENTE ou AGUARDANDO_PAGAMENTO.
    """
    pendentes = [
        pedido for pedido in pedidos
        if pedido.status_pagamento in (StatusPagamento.PENDENTE, StatusPagamento.AGUARDANDO_PAGAMENTO)
    ]
    return pendentes

def relatorio_pagamentos_periodo(
    pedidos: List[Pedido],
    data_inicio: datetime,
    data_fim: datetime
) -> Dict[str, float]:
    """
    Total recebido por método no intervalo [data_inicio, data_fim].
    """
    filtrados = [
        p for p in pedidos
        if data_inicio <= p.data_pedido <= data_fim and p.status_pagamento == StatusPagamento.APROVADO
    ]
    return total_recebido_por_metodo(filtrados)
