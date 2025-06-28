# Módulo responsável por instanciar objetos de pagamento conforme o método selecionado.

from pagamentos.base import Pagamento, PagamentoException
from pagamentos.pix import Pix
from pagamentos.cartao import CartaoCredito, CartaoDebito
from pagamentos.dinheiro import Dinheiro
from pedido.pedido import Pedido
from pedido.item import Item
from clientes.endereco import Endereco
from clientes.clientes import Cliente
from infra.logger import Logger
from infra.mensageria import Mensageria

class PagamentoFactory:
    """
    Fábrica de objetos de pagamento.
    Retorna a instância correta com base no método informado.
    """
    def criar(self, metodo: str, pedido: Pedido, dados_pagamento: dict, logger: Logger, mensageria: Mensageria) -> Pagamento:
        metodo = metodo.upper()
        args_comuns = {"pedido": pedido, "logger": logger, "mensageria": mensageria}

        if metodo == "PIX":
            chave_pix = dados_pagamento.get("chave_pix")
            if not chave_pix:
                raise PagamentoException("Campo 'chave_pix' é obrigatório para pagamento via PIX.")
            return Pix(**args_comuns, chave_pix=chave_pix)

        elif metodo == "CARTAO_CREDITO":
            return CartaoCredito(**args_comuns, **dados_pagamento)

        elif metodo == "CARTAO_DEBITO":
            return CartaoDebito(**args_comuns, **dados_pagamento)

        elif metodo == "DINHEIRO":
            valor_pago = dados_pagamento.get("troco_para")
            if valor_pago is None:
                raise PagamentoException("Campo 'troco_para' é obrigatório para pagamento em dinheiro.")
            return Dinheiro(**args_comuns, valor_pago=valor_pago)

        else:
            raise PagamentoException(f"Método de pagamento '{metodo}' não é suportado.")

        
if __name__ == "__main__":
    # Exemplo de uso da fábrica de pagamentos com dados fictícios

    endereco = Endereco("Rua Exemplo", 10, "Bairro", "Cidade", "12345678", "")
    cliente = Cliente("Teste", "teste@email.com", "999999999", endereco)
    itens = [Item("Sushi", 50.0), Item("Temaki", 35.0)]
    pedido = Pedido(cliente, itens)

    logger = Logger()
    mensageria = Mensageria()

    factory = PagamentoFactory()

    dados_pagamento = {"troco_para": 100.0}
    pagamento = factory.criar("DINHEIRO", pedido, dados_pagamento, logger, mensageria)
    status = pagamento.processar_pagamento()

    print(f"Status: {status.name}")
    print(pedido.gerar_recibo())