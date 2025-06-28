from clientes.endereco import Endereco
from clientes.clientes import Cliente

def criar_cliente_teste(
    nome="Teste Nome",
    email="teste@email.com",
    telefone="999999999",
    rua="Rua Teste",
    numero=123,
    bairro="Bairro Teste",
    cidade="Cidade Teste",
    cep="12345678",
    complemento=""
) -> Cliente:
    endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
    cliente = Cliente(nome, email, telefone, endereco)
    return cliente


if __name__ == "__main__":
    cliente = criar_cliente_teste(nome="Ana Paula", email="ana.paula@teste.com")
    print(f"Cliente criado: {cliente.nome}, {cliente.email}, {cliente.telefone}")
    print(f"Endereço: {cliente.endereco.rua}, {cliente.endereco.numero}, {cliente.endereco.bairro}, {cliente.endereco.cidade}")