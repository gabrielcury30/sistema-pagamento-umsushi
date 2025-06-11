from pagamentos.base import Pagamento, Logger, Mensageria
from pagamentos.pix import Pix
from pagamentos.cartao import CartaoCredito, CartaoDebito
from pagamentos.dinheiro import Dinheiro
from pedido.pedido import Pedido

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
            return Dinheiro(pedido, logger, mensageria, dados_pagamento.get('troco_para', 0.0))
            
        else:
            raise ValueError(f"Método de pagamento '{metodo}' não é suportado.")