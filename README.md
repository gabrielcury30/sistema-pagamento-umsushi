# sistema-pagamento-umsushi

Este repositório contém o desenvolvimento do Sistema de Pagamento para o cliente real UM Sushi, como parte do projeto final da disciplina MATA55 - Programação Orientada a Objetos (2025.1).

## Índice

- [Atividade 1](#atividade-1)
- [Estrutura de Classes](#estrutura-de-classes)

## Atividade 1

Adiciona três classes simples para cuidar do sistema de pagamento:

- **itemMenu**: estrutura básica dos itens disponíveis no menu do restaurante (nome e preço).
- **Carrinho**: cuida da lógica de adicionar e remover itens do menu para o carrinho de compras do usuário.
- **Checkout**: recebe o carrinho de compras do usuário e o método utilizado para pagamento; cuida da lógica de pagamento.

## Estrutura de Classes

```plaintext
itemMenu
└── nome: str
└── preco: float

Carrinho
├── adicionar_Item(item: itemMenu)
├── remover_Item(item: itemMenu)
├── total_Pedido() -> float

Checkout
├── pagar()
└── métodos de pagamento: Cartão, Pix
```

---
