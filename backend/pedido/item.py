# Módulo que define um item com nome e preço.

class Item:
    def __init__(self, nome: str, preco: float):
        """Inicializa um item com nome e preço."""
        self.nome = nome
        self.preco = preco