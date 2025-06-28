from pagamentos.base import Pagamento, Logger, Mensageria
from pagamentos.pix import Pix
from pagamentos.cartao import CartaoCredito, CartaoDebito
from pagamentos.dinheiro import Dinheiro
from pedido.pedido import Pedido
from pedido.item import Item
from clientes.endereco import Endereco
from clientes.clientes import Cliente

class PagamentoFactory:
    def criar(self, metodo: str, pedido: Pedido, dados_pagamento: dict, logger: Logger, mensageria: Mensageria) -> Pagamento:
        metodo = metodo.upper()
        
        if metodo == "PIX":
            return Pix(pedido, dados_pagamento['chave_pix'], logger, mensageria)
        
        elif metodo == "CARTAO_CREDITO":
            return CartaoCredito(pedido, **dados_pagamento, logger=logger, mensageria=mensageria)

        elif metodo == "CARTAO_DEBITO":
            return CartaoDebito(pedido, **dados_pagamento, logger=logger, mensageria=mensageria)
        
        elif metodo == "DINHEIRO":
            return Dinheiro(pedido, dados_pagamento.get('troco_para', 0.0), logger, mensageria)
            
        else:
            raise ValueError(f"Método de pagamento '{metodo}' não é suportado.")
        
if __name__ == "__main__":

    # Setup fictício
    endereco = Endereco("Rua Exemplo", 10, "Bairro", "Cidade", "12345678", "")
    cliente = Cliente("Teste", "teste@email.com", "999999999", endereco)
    itens = [Item("Sushi", 50.0), Item("Temaki", 35.0)]
    pedido = Pedido(cliente, itens)

    logger = Logger()
    mensageria = Mensageria()

    factory = PagamentoFactory()

    # Exemplo com pagamento em dinheiro
    dados_pagamento = {"troco_para": 100.0}
    pagamento = factory.criar("DINHEIRO", pedido, dados_pagamento, logger, mensageria)
    status = pagamento.processar_pagamento()

    print(f"Status: {status.name}")
    print(pedido.gerar_recibo())
