# Módulo para validação e processamento de pagamentos via PIX.

import re
import random
import requests
from pedido.pedido import Pedido
from pagamentos.base import Pagamento, StatusPagamento, PagamentoException
from infra.logger import Logger
from infra.notificacao_service import NotificacaoService

class ValidacaoPixException(PagamentoException):
    """Erro de validação da chave PIX."""
    pass

class Pix(Pagamento):
    def __init__(self, pedido: Pedido, chave_pix: str, logger: Logger, notificacao: NotificacaoService):
        """Inicializa pagamento via PIX validando a chave informada."""
        super().__init__(pedido, logger, notificacao)
        self.chave_pix = chave_pix
        self.codigo_transacao = None
        self._validar_chave()

    def _validar_chave(self):
        """
        Valida a chave PIX conforme formatos suportados:
        email, CPF/CNPJ (11 dígitos) ou chave aleatória (32 caracteres hexadecimais).
        """
        padrao = r"[^@]+@[^@]+\.[^@]+|\d{11}|[0-9A-Fa-f]{32}"
        if not re.fullmatch(padrao, self.chave_pix):
            raise ValidacaoPixException(f"Chave PIX inválida: {self.chave_pix}")

    def _gerar_qr_code(self) -> str:
        """Gera uma string simulando o QR Code para o pagamento PIX."""
        total_centavos = int(self.pedido.calcular_total() * 100)
        return f"PIX://{self.chave_pix}/{total_centavos}-{random.randint(0,9999)}"

    def _get_tipo(self) -> str:
        """Retorna o tipo do pagamento como 'PIX'."""
        return "PIX"
    
    def _get_status_sucesso(self) -> StatusPagamento:
        """Define o status de sucesso como aprovado para PIX."""
        return StatusPagamento.APROVADO
    
    def _realizar_cobranca(self):
        """
        Realiza a cobrança via PIX, validando chave, simulando
        geração do QR code e comunicação com operadora externa.
        """
        try:
            self.logger.registrar(f"[PIX] Validando chave PIX: {self.chave_pix}")
            # Validação extra
            self._validar_chave()

            self.codigo_transacao = self._gerar_qr_code()
            self.logger.registrar(f"[PIX] Código de transação gerado: {self.codigo_transacao}")

            self.logger.registrar("[PIX] Enviando requisição à operadora PIX...")
            resp = requests.get("https://yesno.wtf/api", timeout=5)
            resp.raise_for_status()
            data = resp.json()

            if data.get("answer") == "no":
                raise PagamentoException("Pagamento recusado pela operadora do PIX.")

            self.logger.registrar("[PIX] Pagamento aprovado pela operadora.")

        except requests.exceptions.RequestException as e:
            self.logger.registrar(f"[PIX] Erro na comunicação com a operadora: {e}", nivel="ERROR")
            raise PagamentoException(f"Falha na comunicação com a operadora PIX: {e}") from e

        except ValidacaoPixException as e:
            self.logger.registrar(f"[PIX] Chave PIX inválida: {e}", nivel="ERROR")
            raise

        except PagamentoException:
            raise

        except Exception as e:
            self.logger.registrar(f"[PIX] Erro inesperado no pagamento: {e}", nivel="ERROR")
            raise PagamentoException(f"Erro inesperado no pagamento PIX: {e}") from e