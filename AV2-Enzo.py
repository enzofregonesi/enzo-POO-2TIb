import math
from datetime import date


class Produto:
    def __init__(self, nome, preco):
        self.set_nome(nome)
        self.set_preco(preco)

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome do produto deve ser um texto.")
        if not nome.strip():
            raise ValueError("O nome do produto não pode ficar vazio.")
        self.__nome = nome.strip()

    def get_preco(self):
        return self.__preco

    def set_preco(self, preco):
        if isinstance(preco, bool) or not isinstance(preco, (int, float)):
            raise TypeError("O preço deve ser um número.")
        if not math.isfinite(preco) or preco < 0:
            raise ValueError("O preço deve ser um número não negativo e finito.")
        self.__preco = float(preco)

    def consultar_preco(self):
        return self.get_preco()


class ItemPedido:
    def __init__(self, quantidade, preco_unitario):
        self.set_quantidade(quantidade)
        self.set_preco_unitario(preco_unitario)

    def get_quantidade(self):
        return self.__quantidade

    def set_quantidade(self, quantidade):
        if isinstance(quantidade, bool) or not isinstance(quantidade, int):
            raise TypeError("A quantidade deve ser um número inteiro.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self.__quantidade = quantidade

    def get_preco_unitario(self):
        return self.__preco_unitario

    def set_preco_unitario(self, preco_unitario):
        if isinstance(preco_unitario, bool) or not isinstance(preco_unitario, (int, float)):
            raise TypeError("O preço unitário deve ser um número.")
        if not math.isfinite(preco_unitario) or preco_unitario < 0:
            raise ValueError("O preço unitário deve ser não negativo e finito.")
        self.__preco_unitario = float(preco_unitario)

    def calcular_subtotal(self):
        return self.get_quantidade() * self.get_preco_unitario()


class Pedido:
    def __init__(self, numero, data_pedido):
        self.set_numero(numero)
        self.set_data(data_pedido)
        self.__itens = []
        self.__finalizado = False

    def get_numero(self):
        return self.__numero

    def set_numero(self, numero):
        if isinstance(numero, bool) or not isinstance(numero, (int, str)):
            raise TypeError("O número do pedido deve ser um inteiro ou texto.")
        if isinstance(numero, int) and numero <= 0:
            raise ValueError("O número do pedido deve ser maior que zero.")
        if isinstance(numero, str) and not numero.strip():
            raise ValueError("O número do pedido não pode ficar vazio.")
        self.__numero = numero.strip() if isinstance(numero, str) else numero

    def get_data(self):
        return self.__data

    def set_data(self, data_pedido):
        if not isinstance(data_pedido, (date, str)):
            raise TypeError("A data do pedido deve ser uma data ou texto.")
        if isinstance(data_pedido, str) and not data_pedido.strip():
            raise ValueError("A data do pedido não pode ficar vazia.")
        self.__data = data_pedido

    def get_itens(self):
        return tuple(self.__itens)

    def adicionar_item(self, item):
        if self.__finalizado:
            raise ValueError("Não é possível alterar um pedido finalizado.")
        if not isinstance(item, ItemPedido):
            raise TypeError("O pedido aceita apenas itens do tipo ItemPedido.")
        self.__itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.__itens)

    def finalizar(self):
        if not self.__itens:
            raise ValueError("Não é possível finalizar um pedido sem itens.")
        self.__finalizado = True
        return self.calcular_total()

    def esta_finalizado(self):
        return self.__finalizado


class Cliente:
    def __init__(self, nome, email):
        self.set_nome(nome)
        self.set_email(email)
        self.__pedidos = []

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome do cliente deve ser um texto.")
        if not nome.strip():
            raise ValueError("O nome do cliente não pode ficar vazio.")
        self.__nome = nome.strip()

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if not isinstance(email, str):
            raise TypeError("O e-mail deve ser um texto.")
        email = email.strip()
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValueError("Informe um e-mail válido.")
        self.__email = email

    def get_pedidos(self):
        return tuple(self.__pedidos)

    def cadastrar(self):
        return True

    def realizar_pedido(self, pedido):
        if not isinstance(pedido, Pedido):
            raise TypeError("O cliente só pode realizar pedidos do tipo Pedido.")
        self.__pedidos.append(pedido)
        return pedido


class Carrinho:
    def __init__(self):
        self.__itens = []

    def get_itens(self):
        return tuple(self.__itens)

    def adicionar_item(self, produto):
        if not isinstance(produto, Produto):
            raise TypeError("O carrinho aceita apenas produtos do tipo Produto.")
        self.__itens.append(produto)


# ==============================================================================
# TESTE DE VALIDAÇÃO DO PROJETO FINAL
# ==============================================================================
if __name__ == "__main__":
    print("=== TESTANDO O MODELO DO SUPERMERCADO ===")

    arroz = Produto("Arroz 5 kg", 29.90)
    leite = Produto("Leite 1 L", 5.49)
    cliente = Cliente("Ana Silva", "ana@email.com")

    carrinho = Carrinho()
    carrinho.adicionar_item(arroz)
    carrinho.adicionar_item(leite)
    print(f"Produtos no carrinho: {len(carrinho.get_itens())}")
    print(f"Preço do {arroz.get_nome()}: R$ {arroz.consultar_preco():.2f}")

    pedido = Pedido(1, date.today())
    pedido.adicionar_item(ItemPedido(2, arroz.consultar_preco()))
    pedido.adicionar_item(ItemPedido(3, leite.consultar_preco()))
    cliente.realizar_pedido(pedido)
    total = pedido.finalizar()

    print(f"Cliente: {cliente.get_nome()} ({cliente.get_email()})")
    print(f"Pedidos do cliente: {len(cliente.get_pedidos())}")
    print(f"Total do pedido: R$ {total:.2f}")

    print("\n--- Teste: tentativa de cadastrar quantidade inválida ---")
    try:
        ItemPedido(0, arroz.consultar_preco())
    except ValueError as erro:
        print(f"Item não criado: {erro}")
