# Teste rápido de todas funcionalidades (cadastro, criação de pedido e pagamento) em conjunto.

import random
from services.clientes_factory import criar_cliente_teste
from services.pedidos_factory import criar_pedido_teste
from services.pagamento_service import PagamentoService
from pagamentos.base import PagamentoException

def main():
    print("=== INICIANDO TESTE COMPLETO DO FLUXO ===")

    # Cria cliente e pedido via factories
    cliente = criar_cliente_teste()
    pedido = criar_pedido_teste(cliente)

    print(f"[Teste] Cliente criado: {cliente.nome}, {cliente.email}, {cliente.telefone}, {cliente.endereco.rua}, {cliente.endereco.numero}")
    print(f"[Teste] Pedido criado para {cliente.nome} com os itens:")
    for item in pedido.itens:
        print(f" - {item.nome}: R${item.preco:.2f}")
    print(f"[Teste] Total do pedido: R${pedido.calcular_total():.2f}")

    # Instancia serviço de pagamento
    servico_de_pagamento = PagamentoService()

    # Cenários de pagamento
    cenarios_pagamento = [
        ("PIX", {"chave_pix": "71999998888"}),
        ("CARTAO_CREDITO", {"numero": "1111222233334444", "titular": "Teste Credito", "validade": "12/30", "cvv": "123"}),
        ("CARTAO_DEBITO", {"numero": "5555666677778888", "titular": "Teste Debito", "validade": "11/29", "cvv": "321"}),
        ("DINHEIRO", {"troco_para": pedido.calcular_total() + 20.0})
    ]

    metodo_escolhido, dados_pagamento_escolhido = random.choice(cenarios_pagamento)
    print(f"\n>>> [Teste] Cenário sorteado: {metodo_escolhido} <<<")

    try:
        status_final = servico_de_pagamento.processar_pagamento(
            pedido=pedido,
            metodo=metodo_escolhido,
            dados_pagamento=dados_pagamento_escolhido
        )
        print(f"\nResultado Final no Main: Status do pagamento: {status_final.name}")
    except PagamentoException as e:
        print(f"Erro no pagamento: {e}")
    except ValueError as e:
        print(f"Erro de valor inválido: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()