# Módulo para criação de pedidos de teste com cliente e itens simulados.

from pedido.pedido import Pedido
from pedido.item import Item
from services.clientes_factory import criar_cliente_teste

def criar_pedido_teste(
    cliente=None,
    itens: list[tuple[str, float]] = None
) -> Pedido:
    """
    Cria um pedido de teste com cliente e lista de itens fornecida.
    Se nenhum cliente for passado, um cliente padrão é criado.
    """
    if cliente is None:
        cliente = criar_cliente_teste()

    if itens is None:
        itens = [("Combinado Salmão", 120.0), ("Refrigerante", 8.0)]

    itens_obj = [Item(nome, preco) for nome, preco in itens]
    return Pedido(cliente=cliente, itens=itens_obj)


if __name__ == "__main__":
    # Exemplo de uso da factory de pedidos em testes
    pedido = criar_pedido_teste()
    print(f"Pedido criado para: {pedido.cliente.nome}")
    for item in pedido.itens:
        print(f"- {item.nome}: R${item.preco:.2f}")
    print(f"Total: R${pedido.calcular_total():.2f}")