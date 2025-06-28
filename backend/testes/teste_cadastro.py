# Teste para cadastrar clientes e endereços.

from clientes.cadastro import cadastrar_cliente

if __name__ == "__main__":
    cliente = cadastrar_cliente()

    print("\n=== Cliente Cadastrado ===")
    print(f"Nome: {cliente.nome}")
    print(f"Email: {cliente.email}")
    print(f"Telefone: {cliente.telefone}")
    print("Endereço:")
    print(f"  Rua: {cliente.endereco.rua}")
    print(f"  Número: {cliente.endereco.numero}")
    print(f"  Bairro: {cliente.endereco.bairro}")
    print(f"  Cidade: {cliente.endereco.cidade}")
    print(f"  CEP: {cliente.endereco.cep}")
    print(f"  Complemento: {cliente.endereco.complemento}")

