# Construir cadastramento de endereco e regiao de um cliente
class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str, cep: str, complemento: str = ""):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.complemento = complemento