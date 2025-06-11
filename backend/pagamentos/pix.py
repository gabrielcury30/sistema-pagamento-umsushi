from pedido.pedido import Pedido
from pagamentos.base import Pagamento, StatusPagamento, Logger, Mensageria

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
        total_centavos = int(self.pedido.calcular_total() * 100)
        return f"PIX://{self.chave_pix}/{total_centavos}-{random.randint(0,9999)}"

    def _get_tipo(self) -> str:
        return "PIX"
    
    def _get_status_sucesso(self) -> StatusPagamento:
        return StatusPagamento.APROVADO
    
    def _realizar_cobranca(self):
        self._validar_chave()
        self.codigo_transacao = self._gerar_qr_code()
        
        resp = requests.get("https://yesno.wtf/api", timeout=5)
        resp.raise_for_status()  
        data = resp.json()

        if data.get("answer") == "no":
            raise RuntimeError("Recusa pela operadora do PIX") 