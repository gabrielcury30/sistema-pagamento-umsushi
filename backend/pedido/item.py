# Módulo que define um item com nome e preço.

class Item:
    def __init__(self, nome: str, preco: float):
        """Inicializa um item com nome e preço e verifica se o valor é não negativo"""
        if not isinstance(preco, (int, float)) or preco < 0:
            raise ValueError(f"O preço do item '{nome}' deve ser um número não negativo")
        
        self.nome = nome
        self.preco = preco