# pagamentos/pix.py
from pagamentos.base import Pagamento, StatusPagamento, Pedido, Logger, Mensageria 
import re, random, requests

class Pix(Pagamento):
    def __init__(self, pedido, chave_pix, logger, mensageria):
        super().__init__(pedido, logger, mensageria)
        self.chave_pix = chave_pix
        self.codigo_transacao = None

    def _validar_chave(self):
        padrao = r"[^@]+@[^@]+\.[^@]+|\d{11}|[0-9A-Fa-f]{32}"
        if not re.fullmatch(padrao, self.chave_pix):
            raise ValueError(f"Chave PIX inválida: {self.chave_pix}")

    def _gerar_qr_code(self):
        total_centavos = int(self.pedido.total * 100)
        return f"PIX://{self.chave_pix}/{total_centavos}-{random.randint(0,9999)}"

    def processar_pagamento(self):
        try:
            self.logger.registrar(f"[PIX] Iniciando pagamento {self.pedido.id}")
            self._validar_chave()
            self.codigo_transacao = self._gerar_qr_code()

            resp = requests.get("https://yesno.wtf/api", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if data.get("answer") == "yes":
                self.status = StatusPagamento.APROVADO
                self.logger.registrar(f"[PIX] Aprovado: {self.codigo_transacao}")
                self.mensageria.enviar_notificacao(
                    f"Olá {self.pedido.cliente.nome}, QR: {self.codigo_transacao}"
                )
            else:
                raise RuntimeError("Transação PIX recusada pela API")
        except Exception as e:
            self.status = StatusPagamento.RECUSADO
            self.logger.registrar(f"[PIX] Erro: {e}", nivel="ERROR")
        finally:
            self.pedido.status_pagamento = self.status
            recibo = self.pedido.gerar_recibo()
            self.logger.registrar(f"[PIX] Recibo:\n{recibo}")
            return self.codigo_transacao
