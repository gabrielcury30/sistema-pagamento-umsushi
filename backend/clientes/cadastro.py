# Cadastro de clientes com validação básica e tratamento de erros.

import requests
import re
from clientes.endereco import Endereco
from clientes.clientes import Cliente

def validar_texto_com_letra(valor: str, campo: str) -> str:
    """
    Valida se a string valor contém pelo menos uma letra e
    tem no mínimo 2 caracteres não vazios.
    """
    if not any(c.isalpha() for c in valor) or len(valor.strip()) < 2:
        raise ValueError(f"{campo} inválido. Deve conter ao menos uma letra e ter pelo menos 2 caracteres.")
    return valor

def obter_input_validado(mensagem: str, validador, campo: str):
    """
    Solicita entrada do usuário repetidamente até que o valor
    informado seja validado pela função validador.
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



def buscar_endereco_por_cep(cep: str) -> dict:
    """
    Faz um request para a API ViaCEP e retorna um dicionário com as chaves:
    'logradouro', 'bairro' e 'localidade'.
    Se o CEP não existir ou der erro, lança ValueError.
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if data.get("erro"):
        raise ValueError("CEP não encontrado.")
    return {
        "rua": data["logradouro"],
        "bairro": data["bairro"],
        "cidade": data["localidade"],
    }



def obter_cep_e_autocompletar() -> dict:
    """
    Solicita CEP do usuário, validando que tenha exatamente
    8 dígitos numéricos, busca na API e retorna
    os dados de endereço (rua, bairro, cidade).
    """
    while True:
        cep = input("CEP (8 dígitos numéricos): ")
        if not (cep.isdigit() and len(cep) == 8):
            print("CEP inválido. Deve conter exatamente 8 números.")
            continue

        try:
            endereco_api = buscar_endereco_por_cep(cep)
            print(
                f"Encontrado: {endereco_api['rua']}, "
                f"{endereco_api['bairro']} - {endereco_api['cidade']}"
            )
            return {"cep": cep, **endereco_api}
        except (requests.RequestException, ValueError) as e:
            print(f"Não foi possível buscar o CEP: {e}")


def validar_email(email: str) -> str:
    """Valida o formato do email usando regex simples."""
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Email inválido. Deve estar no formato nome@dominio.com")
    return email


def cadastrar_cliente() -> Cliente:
    """
    Realiza o cadastro de um cliente, solicitando dados pessoais
    e endereço, validando as entradas com as funções acima.
    """
    try:
        print("=== Cadastro de Cliente ===")

        nome = obter_input_validado("Nome: ", validar_texto_com_letra, "Nome")
        
        email = obter_input_validado("Email: ", validar_email, "Email")

        telefone = obter_telefone()

        print("=== Endereço ===")
        dadosEndereco = obter_cep_e_autocompletar()
        numero = obter_numero()
        complemento = input("Complemento (opcional): ")
        endereco = Endereco(rua=dadosEndereco["rua"], numero=numero, bairro=dadosEndereco["bairro"], cidade=dadosEndereco["cidade"], cep=dadosEndereco["cep"], complemento=complemento)
        cliente = Cliente(nome, email, telefone, endereco)
        return cliente

    except Exception as e:
        print(f"[Erro] Falha no cadastro: {e}")
        return None