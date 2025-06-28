# Módulo para processamento de pagamentos em dinheiro.

from pedido.pedido import Pedido
from pagamentos.base import Pagamento, StatusPagamento
from infra.logger import Logger
from infra.mensageria import Mensageria
from pagamentos.base import PagamentoException

class ValidacaoDinheiroException(PagamentoException):
    """Erro relacionado ao pagamento em dinheiro."""
    pass

class Dinheiro(Pagamento):
    def __init__(self, pedido: Pedido, valor_pago: float, logger: Logger, mensageria: Mensageria):
        """Inicializa pagamento em dinheiro e valida valor pago."""
        super().__init__(pedido, logger, mensageria)
        
        if not isinstance(valor_pago, (int, float)) or valor_pago < 0:
            raise ValidacaoDinheiroException("Valor pago deve ser um número positivo ou zero.")
        
        self.valor_pago = valor_pago
        self.troco = 0.0

    def _get_tipo(self) -> str:
        """Retorna o tipo de pagamento como 'DINHEIRO'."""
        return "DINHEIRO"
    
    def _get_status_sucesso(self) -> StatusPagamento:
        """Define o status de sucesso como aguardando pagamento na entrega."""
        return StatusPagamento.AGUARDANDO_PAGAMENTO
    
    def _realizar_cobranca(self):
        """Verifica se o valor pago é suficiente e calcula o troco, se houver."""
        self.logger.registrar(f"[DINHEIRO] Verificando valor para troco.")
        total_pedido = self.pedido.calcular_total()

        if self.valor_pago < total_pedido:
            raise ValidacaoDinheiroException(
                f"Valor pago ({self.valor_pago}) é menor que o total do pedido ({total_pedido})."
            )
        
        if self.valor_pago > total_pedido:
            self.troco = self.valor_pago - total_pedido
            self.logger.registrar(f"[DINHEIRO] Pagamento aceito. Troco: R${self.troco:.2f}.")
        else:
            self.logger.registrar(f"[DINHEIRO] Pagamento em dinheiro com valor exato, sem troco.")