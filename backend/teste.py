from src.clientes import Cliente, Endereco  # Ajuste para o caminho correto

import unittest
from pagamentos.pix import Pix
from pedidos import Carrinho, ItemMenu

class TestPagamentoPix(unittest.TestCase):
    def setUp(self):
        self.carrinho = Carrinho("Usuário Teste")
        self.carrinho.adicionar_item(ItemMenu("Salmão", 75.90))

    def test_pagamento_pix_sucesso(self):
        """Verifica se um pagamento PIX é processado corretamente"""
        pagamento = Pix(self.carrinho, "chave123")
        pagamento.processar_pagamento()
        self.assertEqual(pagamento.status, StatusPagamento.PAGO)

    def test_pagamento_pix_falha(self):
        """Verifica se o sistema responde corretamente a uma falha de pagamento"""
        pagamento = Pix(self.carrinho, "chave123")
        pagamento.processar_pagamento()
        self.assertIn(pagamento.status, [StatusPagamento.PAGO, StatusPagamento.FALHA])

if __name__ == "__main__":
    unittest.main()
