from services.payment_factory import PagamentoFactory
from pedido.pedido import Pedido
from pagamentos.base import Logger, Mensageria

class PagamentoService:
    def __init__(self):
        self.logger = Logger()
        self.mensageria = Mensageria()
        self.factory = PagamentoFactory()

    def processar_pagamento(self, pedido: Pedido, metodo: str, dados_pagamento: dict):
        self.logger.registrar(f"--- SERVIÇO DE PAGAMENTO INICIADO PARA MÉTODO {metodo} ---")
        
        pagamento_obj = self.factory.criar(
            metodo=metodo,
            pedido=pedido,
            dados_pagamento=dados_pagamento,
            logger=self.logger,
            mensageria=self.mensageria
        )
        
        resultado = pagamento_obj.processar_pagamento()
        
        self.logger.registrar(f"--- SERVIÇO DE PAGAMENTO FINALIZADO COM STATUS: {resultado.name} ---")
        return resultado