
from logging_util import registrar_evento
class Pix(Pagamento):
    def processar_pagamento(self):
        if not self.pedido.pedidos:
            registrar_evento("Erro: O carrinho está vazio!", nivel=logging.ERROR)
            return

        self.status = StatusPagamento.PROCESSANDO
        registrar_evento(f"Pagamento via PIX iniciado para {self.pedido.usuario_id}. Total: R$ {self.pedido.total_pedido():.2f}")
        
        # Simulação de transação
        try:
            self.codigo_transacao = f"PIX-{random.randint(100000, 999999)}"
            registrar_evento(f"Código de transação gerado: {self.codigo_transacao}")

            if random.random() < 0.9:
                self.status = StatusPagamento.PAGO
                registrar_evento(f"Pagamento PIX para {self.pedido.usuario_id} APROVADO.")
            else:
                self.status = StatusPagamento.FALHA
                raise PagamentoPixFalhou("Falha na simulação do pagamento PIX")
        
        except PagamentoPixFalhou as e:
            registrar_evento(f"Erro no pagamento PIX: {e}", nivel=logging.ERROR)
        finally:
            registrar_evento(f"Status do pagamento PIX: {self.status.value}")
