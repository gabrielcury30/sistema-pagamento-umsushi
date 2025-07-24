# Módulo de serviço responsável por orquestrar o processamento de pagamentos.

from pagamentos.base import PagamentoException
from services.payment_factory import PagamentoFactory
from pedido.pedido import Pedido
from pagamentos.base import StatusPagamento
from infra.logger import Logger
from infra.notificacao_service import NotificacaoService

class PagamentoService:
    """
    Serviço que encapsula a lógica de processamento de pagamentos,
    incluindo criação do pagamento, logging e notificação.
    """
    def __init__(self):
        self.logger = Logger()
        self.notificacao = NotificacaoService()
        self.factory = PagamentoFactory()

    def processar_pagamento(self, pedido: Pedido, metodo: str, dados_pagamento: dict):
        """
        Processa o pagamento de um pedido usando o método especificado,
        tratando exceções e registrando o status final.
        """
        self.logger.registrar(f"--- SERVIÇO DE PAGAMENTO INICIADO PARA MÉTODO {metodo} ---")

        if not isinstance(dados_pagamento, dict):
            raise ValueError("`dados_pagamento` deve ser um dicionário.")

        try:
            pagamento_obj = self.factory.criar(
                metodo=metodo,
                pedido=pedido,
                dados_pagamento=dados_pagamento,
                logger=self.logger,
                notificacao=self.notificacao
            )

            resultado = pagamento_obj.processar_pagamento()

            self.logger.registrar(f"--- SERVIÇO DE PAGAMENTO FINALIZADO COM STATUS: {resultado.name} ---")
            return resultado

        except PagamentoException as pe:
            self.logger.registrar(f"[ERRO] Falha no pagamento: {pe}", nivel="ERROR")
            self.notificacao.enviar_notificacao(f"Erro no pagamento: {pe}")
            pedido.status_pagamento = StatusPagamento.RECUSADO
            return StatusPagamento.RECUSADO

        except ValueError as ve:
            self.logger.registrar(f"[ERRO] Dados inválidos para o método '{metodo}': {ve}", nivel="ERROR")
            self.notificacao.enviar_notificacao(f"Erro nos dados do pagamento: {ve}")
            pedido.status_pagamento = StatusPagamento.RECUSADO
            return StatusPagamento.RECUSADO

        except Exception as e:
            self.logger.registrar(f"[ERRO] Erro inesperado ao processar pagamento: {e}", nivel="ERROR")
            self.notificacao.enviar_notificacao("Erro inesperado ao processar o pagamento. Tente novamente.")
            pedido.status_pagamento = StatusPagamento.RECUSADO
            return StatusPagamento.RECUSADO