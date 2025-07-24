# Implementa a classe Cliente associada a um endereço.

from clientes.endereco import Endereco

class Cliente:
    def __init__(self, nome: str, email: str, telefone: str, endereco: Endereco):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco