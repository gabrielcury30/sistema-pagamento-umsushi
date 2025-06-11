from pedido.pedido import Pedido
from pagamentos.base import Pagamento, StatusPagamento, Logger, Mensageria
import re, random

class Dinheiro(Pagamento):
    def __init__(self, pedido: Pedido, valor_pago: float, logger: Logger, mensageria: Mensageria):
        super().__init__(pedido, logger, mensageria)
        self.valor_pago = valor_pago
        self.troco = 0.0

    def _get_tipo(self) -> str:
        return "DINHEIRO"
    
    def _get_status_sucesso(self) -> StatusPagamento:
        return StatusPagamento.AGUARDANDO_PAGAMENTO
    
    def _realizar_cobranca(self):
        self.logger.registrar(f"[DINHEIRO] Verificando valor para troco.")
        total_pedido = self.pedido.calcular_total()

        if self.valor_pago < total_pedido and self.valor_pago > 0:
            raise ValueError(f"Valor pago ({self.valor_pago}) é menor que o total do pedido ({total_pedido}).")
        
        if self.valor_pago > 0:
            self.troco = self.valor_pago - total_pedido
            self.logger.registrar(f"[DINHEIRO] Pagamento aceito. Troco: {self.troco:.2f}.")

        else:
            self.logger.registrar(f"[DINHEIRO] Cliente pagará com valor exato. Sem troco.")
