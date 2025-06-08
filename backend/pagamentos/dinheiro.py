from pedido.pedido import Pedido
from pagamentos.base import Pagamento, StatusPagamento, Logger, Mensageria
import re, random

class Dinheiro(Pagamento):
    def __init__(self, pedido: Pedido, valor_pago: float, logger: Logger, mensageria: Mensageria):
        super().__init__(pedido, logger, mensageria)
        self.valor_pago = valor_pago
        self.troco = 0.0
        self.status = StatusPagamento.AGUARDANDO_PAGAMENTO
        self.pedido.status_pagamento = self.status

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[DINHEIRO] Processando pagamento para o pedido {self.pedido.id}")

            total_pedido = self.pedido.calcular_total()

            if self.valor_pago < total_pedido:
                raise ValueError(f"Valor insuficiente. Pago: R${self.valor_pago:.2f}, Total: R${total_pedido:.2f}")

            self.status = StatusPagamento.APROVADO
            self.troco = self.valor_pago - total_pedido

            self.logger.registrar(f"[DINHEIRO] Pagamento aprovado. Troco: R${self.troco:.2f}")
            self.mensageria.enviar_notificacao(
                f"Pagamento em dinheiro confirmado para {self.pedido.cliente.nome}. Troco: R${self.troco:.2f}"
            )

        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[DINHEIRO] Erro no pagamento: {e}", nivel="ERROR")

        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[DINHEIRO] Recibo:\n{recibo}")
            return self.status