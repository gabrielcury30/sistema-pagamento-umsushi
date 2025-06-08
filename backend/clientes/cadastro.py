from clientes.endereco import Endereco
from clientes.clientes import Cliente

def validar_texto_com_letra(valor: str, campo: str) -> str:
    """
    Garante que o valor contenha ao menos uma letra e tenha pelo menos 2 caracteres.
    """
    while not any(c.isalpha() for c in valor) or len(valor.strip()) < 2:
        print(f"{campo} inválido. Deve conter ao menos uma letra e ter pelo menos 2 caracteres.")
        valor = input(f"{campo}: ")
    return valor

def cadastrar_cliente():
    print("=== Cadastro de Cliente ===")

    # Nome
    nome = input("Nome: ")
    while nome.isdigit() or len(nome.strip()) < 2:
        print("Nome inválido. Deve conter letras e ter pelo menos 2 caracteres.")
        nome = input("Nome: ")

    # Email
    email = input("Email: ")
    while "@" not in email or "." not in email:
        print("Email inválido. Digite um email válido.")
        email = input("Email: ")

    # Telefone: somente números, entre 8 e 11 dígitos
    while True:
        telefone = input("Telefone (8-11 dígitos, somente números): ")
        try:
            _ = int(telefone)
            if len(telefone) < 8 or len(telefone) > 11:
                print("Telefone deve ter entre 8 e 11 dígitos.")
                continue
            break
        except ValueError:
            print("Telefone deve conter apenas números.")

    print("=== Endereço ===")

    # Rua, Bairro e Cidade (valida texto com letra)
    rua    = validar_texto_com_letra(input("Rua: "), "Rua")
    bairro = validar_texto_com_letra(input("Bairro: "), "Bairro")
    cidade = validar_texto_com_letra(input("Cidade: "), "Cidade")

    # Número do endereço
    while True:
        numero_str = input("Número: ")
        try:
            numero = int(numero_str)
            break
        except ValueError:
            print("Número deve ser um número inteiro.")

    # CEP (8 dígitos numéricos)
    while True:
        cep = input("CEP (8 dígitos numéricos): ")
        if cep.isdigit() and len(cep) == 8:
            break
        else:
            print("CEP inválido. Deve conter exatamente 8 números.")

    complemento = input("Complemento (opcional): ")

    endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
    cliente = Cliente(nome, email, telefone, endereco)
    return cliente