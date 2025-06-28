# Teste para capturar exceções em diferentes situações.

from pagamentos.cartao import CartaoCredito, CartaoDebito, ValidacaoCartaoException
from pagamentos.base import PagamentoException
from pagamentos.dinheiro import Dinheiro
from pagamentos.pix import Pix, ValidacaoPixException
from services.clientes_factory import criar_cliente_teste
from services.pedidos_factory import criar_pedido_teste
from pedido.pedido import Pedido, PedidoInvalidoException 
from infra.logger import Logger
from infra.mensageria import Mensageria

logger = Logger()
mensageria = Mensageria()
cliente = criar_cliente_teste()
pedido = criar_pedido_teste(cliente)


# EXCEÇÕES DE CARTÃO
def testar_validacao_cartao_credito():
    """
    Testa as validações do cartão de crédito,
    esperando capturar exceções em dados inválidos como número com menos de 16 dígitos.
    """
    try:
        cartao = CartaoCredito(pedido, "123", "Teste", "12/26", "123", logger, mensageria)
        cartao._validar_cartao()
    except ValidacaoCartaoException as e:
        print(f"Cartão Crédito - Erro capturado como esperado: {e}")
    except Exception as e:
        print(f"Cartão Crédito - Erro inesperado: {e}")

def testar_validacao_cartao_debito():
    """
    Testa as validações do cartão de débito,
    esperando capturar exceções para CVV inválido e validade expirada.
    """
    try:
        cartao = CartaoDebito(pedido, "1234567890123456", "Teste", "11/20", "12", logger, mensageria)
        cartao._validar_cartao()
    except ValidacaoCartaoException as e:
        print(f"Cartão Débito - Erro capturado como esperado: {e}")
    except Exception as e:
        print(f"Cartão Débito - Erro inesperado: {e}")


# EXCEÇÕES DE DINHEIRO
def testar_pagamento_dinheiro_valor_negativo():
    """
    Testa o pagamento em dinheiro com valor pago negativo,
    esperando capturar exceção durante a tentativa de cobrança.
    """
    valor_pago = -50
    try:
        dinheiro = Dinheiro(pedido, valor_pago, logger, mensageria)
        dinheiro._realizar_cobranca()
    except PagamentoException as e:
        print(f"Erro capturado como esperado (valor negativo): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def testar_pagamento_dinheiro_valor_menor():
    """
    Testa o pagamento em dinheiro com valor pago menor que o total do pedido,
    esperando capturar exceção na cobrança.
    """
    dinheiro = Dinheiro(pedido, valor_pago=50.0, logger=logger, mensageria=mensageria)
    try:
        dinheiro._realizar_cobranca()
    except PagamentoException as e:
        print(f"Erro capturado como esperado: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def testar_pagamento_dinheiro_valor_igual():
    """
    Testa o pagamento em dinheiro com valor exato igual ao total do pedido,
    esperando que o pagamento seja aceito sem troco.
    """
    valor_pago = pedido.calcular_total()
    dinheiro = Dinheiro(pedido, valor_pago, logger, mensageria)
    try:
        dinheiro._realizar_cobranca()
        print("Pagamento em dinheiro com valor exato realizado com sucesso.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def testar_pagamento_dinheiro_com_troco():
    """
    Testa o pagamento em dinheiro com valor maior que o total do pedido,
    verificando se o troco é calculado corretamente.
    """
    valor_pago = pedido.calcular_total() + 20
    dinheiro = Dinheiro(pedido, valor_pago, logger, mensageria)
    try:
        dinheiro._realizar_cobranca()
        print(f"Pagamento com troco realizado com sucesso. Troco: R${dinheiro.troco:.2f}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    
# EXCEÇÕES DE PIX
def testar_validacao_chave_pix_invalida():
    """
    Testa a validação da chave PIX inválida.
    Espera capturar uma exceção ValidacaoPixException ao criar o objeto Pix com chave inválida.
    """
    try:
        pix = Pix(pedido, "chave_invalida", logger, mensageria)
    except ValidacaoPixException as e:
        print(f"PIX - Erro capturado como esperado: {e}")

def testar_rejeicao_operadora_pix():
    """
    Testa o cenário em que a operadora PIX rejeita o pagamento simulando
    uma resposta negativa da API externa.
    Espera capturar um PagamentoException.
    """
    pix = Pix(pedido, "teste@pix.com", logger, mensageria)

    # Monkeypatch para simular resposta negativa da API externa
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return {"answer": "no"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    import requests
    # Salvar referência original para restaurar depois (opcional)
    original_get = requests.get
    requests.get = mock_get

    try:
        pix._realizar_cobranca()
    except PagamentoException as e:
        print(f"PIX - Erro capturado como esperado (recusa operadora): {e}")
    finally:
        # Restaurar método original para não afetar outros testes
        requests.get = original_get


# EXCEÇÕES PEDIDOS
def testar_pedido_sem_itens():
    try:
        cliente = criar_cliente_teste()
        pedido = Pedido(cliente, [])
    except PedidoInvalidoException as e:
        print(f"Pedido - Erro capturado como esperado: {e}")


if __name__ == "__main__":
    print("\n=== Exceções de Cartão ===\n")
    testar_validacao_cartao_credito()
    testar_validacao_cartao_debito()

    print("\n=== Exceções de Dinheiro ===\n")
    testar_pagamento_dinheiro_valor_negativo()
    testar_pagamento_dinheiro_valor_menor()
    testar_pagamento_dinheiro_valor_igual()
    testar_pagamento_dinheiro_com_troco()

    print("\n=== Testes de exceções PIX ===\n")
    testar_validacao_chave_pix_invalida()
    testar_rejeicao_operadora_pix()

    print("\n=== Exceção de Pedido ===\n")
    testar_pedido_sem_itens()