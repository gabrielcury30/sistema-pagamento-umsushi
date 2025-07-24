# Módulo base para processamento e controle de pagamentos.

from abc import ABC, abstractmethod
from enum import Enum
from infra.logger import Logger
from infra.notificacao_service import NotificacaoService

# --- ENUMS ---
class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    RECUSADO = "Recusado"
    AGUARDANDO_PAGAMENTO = "Aguardar Pagamento na Entrega"

class TipoCartao(Enum):
    CREDITO = "Crédito"
    DEBITO = "Débito"

class PagamentoException(Exception):
    """Erro ocorrido durante o processamento de pagamento."""
    pass

# --- Classe abstrata Pagamento ---
class Pagamento(ABC):
    def __init__(self, pedido, logger: Logger, notificacao: NotificacaoService):
        """Inicializa o pagamento associando ao pedido, logger e sistema de notificações."""
        self.pedido = pedido
        self.logger = logger
        self.notificacao = notificacao
        self.status = StatusPagamento.PENDENTE
        pedido.definir_pagamento(self)

    def processar_pagamento(self):
        """Orquestra o fluxo de processamento do pagamento, tratando exceções e registrando resultados."""
        try:
            self._registrar_inicio()
            self._realizar_cobranca()
            self.status = self._get_status_sucesso()
            self._registrar_status()
            self._notificar_cliente()

        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[{self._get_tipo()}] Erro no pagamento: {e}", nivel="ERROR")

        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[{self._get_tipo()}] Recibo gerado:\n{recibo}")
            return self.status

    # --- Métodos auxiliares privados ---
    def _registrar_inicio(self):
        """Registra no log o início do processamento do pagamento."""
        self.logger.registrar(f"[{self._get_tipo()}] Iniciando pagamento para pedido {self.pedido.id}")

    def _registrar_status(self):
        """Registra no log o status final do pagamento."""
        self.logger.registrar(f"[{self._get_tipo()}] Status definido como: {self.status.value}")

    def _notificar_cliente(self):
        """Envia notificação ao cliente com o status do pagamento."""
        self.notificacao.enviar_notificacao(
            f"Olá {self.pedido.cliente.nome}, o status do seu pagamento via {self._get_tipo()} é: {self.status.value}\n"
        )

    @abstractmethod
    def _get_tipo(self) -> str:
        """Retorna o tipo de pagamento (ex: 'Crédito', 'Débito')."""
        pass

    @abstractmethod
    def _realizar_cobranca(self):
        """Executa a lógica específica para realizar a cobrança."""
        pass

    @abstractmethod
    def _get_status_sucesso(self) -> StatusPagamento:
        """Define o status considerado como sucesso para o pagamento."""
        pass