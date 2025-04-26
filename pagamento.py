from dataclasses import dataclass

@dataclass
class itemMenu:
    nome: str
    preco: float

menu = [ 
    itemMenu("ovo de salmão fresco", 75.90),
    itemMenu("ovo de salmão maçaricado", 75.90), 
    itemMenu("hot balls - queijo", 22.99)
    ]



class Carrinho:
    def __init__(self, usuarioId: str):
        self.usuarioId = usuarioId
        self.pedidos = []

    def adicionar_Item(self, item):
        self.pedidos.append(item)
    
    def remover_Item(self, item):
        if item in self.pedidos:
            self.pedidos.remove(item)

    def total_Pedido(self):
         return sum(item.preco for item in self.pedidos)

   
            
class Checkout:
    def __init__(self, carrinho:Carrinho, metodo: str):
        self.carrinho = carrinho
        self.metodo = metodo

    def pagar(self):
        total = self.carrinho.total_Pedido()
        print("Pedido total de:", total, "para", self.carrinho.usuarioId)

        if(self.metodo == "Cartão"):
            print("Insira o numero do seu cartão")
            self.cartao = input()
        elif(self.metodo == "Pix"): 
            print("Código de barras para pagar com pix: ||l|l|l|||||ll|l|l|ll|l||ll|")



carrinho1 = Carrinho("Usuario João")
carrinho1.adicionar_Item(menu[0])
carrinho1.adicionar_Item(menu[2])

checkout1 = Checkout(carrinho1, "Cartão")
checkout1.pagar()
