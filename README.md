# sistema-pagamento-umsushi

Este repositório contém o desenvolvimento do Sistema de Pagamento para o cliente real UM Sushi, como parte do projeto final da disciplina MATA55 - Programação Orientada a Objetos (2025.1).

## Índice

- [Atividade 1](#atividade-1)
- [Estrutura de Classes](#estrutura-de-classes)

## Atividade 1

Adiciona classes para cuidar do sistema de pagamento:

- **Cliente**: Representa um cliente no sistema. Contém informações pessoais como nome, e-mail, telefone e endereço.
- **Endereco**: Contém os detalhes do endereço de um cliente, como rua, número, bairro, cidade, CEP e complemento.
- **Item**: Representa um item no cardápio de pedidos. Contém informações sobre o nome e o preço do item.
- **Pedido (Mock)**: Representa um pedido feito por um cliente. Armazena o cliente, os itens do pedido, o total do pedido e a data em que foi realizado. Também possui métodos para calcular o total e gerar um recibo.
- **Pagamento (Abstrato)**: Classe abstrata que define a estrutura básica para processar pagamentos. Contém o pedido relacionado e o status do pagamento, com um método abstrato para processar o pagamento.
- **PIX (Herda de Pagamento)**: Representa o pagamento via PIX. Herdada da classe Pagamento, ela adiciona a chave PIX para realizar o pagamento.
- **Cartao (Herda de Pagamento)**: Representa o pagamento via cartão. Herdada da classe Pagamento, ela inclui informações como número do cartão, CVV, validade e tipo de cartão (crédito ou débito).



## Estrutura de Classes

```plaintext
Módulo: Clientes
    Classe: Cliente  
    └── nome: str  
    └── email: str  
    └── telefone: str  
    └── endereco: Endereco  

    Classe: Endereco  
    └── rua: str  
    └── numero: int  
    └── bairro: str  
    └── cidade: str  
    └── cep: str  
    └── complemento: str  


Módulo: Pedidos
    Classe: Item  
    └── nome: str  
    └── preco: float  

    Classe: Pedido (Mock)  
    └── cliente: Cliente  
    └── itens: List[Item]  
    └── total: float  
    └── data_pedido: datetime  
    ├── calcular_total(): float  
    └── gerar_recibo(): str  

Módulo: Pagamentos
    Classe Abstrata: Pagamento  
    └── pedido: Pedido  
    └── status: enum  
    └── processar_pagamento()  

    Classe: PIX (Herda de Pagamento)  
    └── chave_pix: str  
    └── processar_pagamento()  

    Classe: Cartao (Herda de Pagamento)  
    └── numero: str  
    └── cvv: str  
    └── validade: str  
    └── tipo: enum  
    └── processar_pagamento()  
```

---
