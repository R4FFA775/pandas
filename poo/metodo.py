
class Produto:
 def __init__(self, nome, preco):
  self.nome = nome
  self.preco = preco
 def aplicar_desconto(self, percentual):
  self.preco *= (1 - percentual / 100)
  produto = Produto("Notebook", 5000)
  produto.aplicar_desconto(10)
  print(produto.preco)
  