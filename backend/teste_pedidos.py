# Cria o pedido e mostra o recibo.
from clientes.clientes import Cliente
from clientes.endereco import Endereco
from pedido.item import Item
from pedido.pedido import Pedido

def main():
    # Criar endereço e cliente
    endereco = Endereco("Rua A", 123, "Bairro B", "Cidade C", "12345-678", "")
    cliente = Cliente("João Silva", "joao@email.com", "11999998888", endereco)

    # Criar itens
    item1 = Item("Produto 1", 50.0)
    item2 = Item("Produto 2", 30.0)

    # Criar pedido
    pedido = Pedido(cliente, [item1, item2])

    # Calcular total e imprimir
    total = pedido.calcular_total()
    print(f"Total do pedido: R${total:.2f}")

    # Gerar recibo e imprimir
    recibo = pedido.gerar_recibo()
    print(recibo)

if __name__ == "__main__":
    main()