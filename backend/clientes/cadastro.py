# Cadastro de clientes com validação básica e tratamento de erros.

from clientes.endereco import Endereco
from clientes.clientes import Cliente

def validar_texto_com_letra(valor: str, campo: str) -> str:
    """
    Valida se a string `valor` contém pelo menos uma letra e
    tem no mínimo 2 caracteres não vazios.
    """
    if not any(c.isalpha() for c in valor) or len(valor.strip()) < 2:
        raise ValueError(f"{campo} inválido. Deve conter ao menos uma letra e ter pelo menos 2 caracteres.")
    return valor

def obter_input_validado(mensagem: str, validador, campo: str):
    """
    Solicita entrada do usuário repetidamente até que o valor
    informado seja validado pela função `validador`.
    """
    while True:
        try:
            valor = input(mensagem)
            return validador(valor, campo)
        except ValueError as e:
            print(e)

def obter_telefone():
    """
    Solicita telefone do usuário, validando que seja composto
    apenas por números e tenha entre 8 e 11 dígitos.
    """
    while True:
        telefone = input("Telefone (8-11 dígitos, somente números): ")
        if not telefone.isdigit():
            print("Telefone deve conter apenas números.")
            continue
        if not (8 <= len(telefone) <= 11):
            print("Telefone deve ter entre 8 e 11 dígitos.")
            continue
        return telefone

def obter_numero():
    """
    Solicita um número inteiro do usuário, validando a entrada.
    """
    while True:
        numero = input("Número: ")
        if numero.isdigit():
            return int(numero)
        print("Número deve ser um número inteiro.")

def obter_cep():
    """
    Solicita o CEP do usuário, validando que tenha exatamente
    8 dígitos numéricos.
    """
    while True:
        cep = input("CEP (8 dígitos numéricos): ")
        if cep.isdigit() and len(cep) == 8:
            return cep
        print("CEP inválido. Deve conter exatamente 8 números.")

def cadastrar_cliente() -> Cliente:
    """
    Realiza o cadastro de um cliente, solicitando dados pessoais
    e endereço, validando as entradas com as funções acima.
    """
    try:
        print("=== Cadastro de Cliente ===")

        nome = obter_input_validado("Nome: ", validar_texto_com_letra, "Nome")
        
        # Validação simples do email: precisa conter '@' e '.'
        email = input("Email: ")
        while "@" not in email or "." not in email:
            print("Email inválido. Digite um email válido.")
            email = input("Email: ")

        telefone = obter_telefone()

        print("=== Endereço ===")
        rua = obter_input_validado("Rua: ", validar_texto_com_letra, "Rua")
        bairro = obter_input_validado("Bairro: ", validar_texto_com_letra, "Bairro")
        cidade = obter_input_validado("Cidade: ", validar_texto_com_letra, "Cidade")
        numero = obter_numero()
        cep = obter_cep()
        complemento = input("Complemento (opcional): ")

        endereco = Endereco(rua, numero, bairro, cidade, cep, complemento)
        cliente = Cliente(nome, email, telefone, endereco)
        return cliente

    except Exception as e:
        print(f"[Erro] Falha no cadastro: {e}")
        return None
