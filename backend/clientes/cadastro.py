from clientes.endereco import Endereco
from clientes.clientes import Cliente

def cadastrar_cliente():
    print("=== Cadastro de Cliente ===")
    
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone: ")

    print("=== Endereço ===")
    
    rua = input("Rua: ")
    numero = int(input("Número: "))
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    cep = input("CEP: ")
    complemento = input("Complemento: ")

    endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
    cliente = Cliente(nome, email, telefone, endereco)

    return cliente