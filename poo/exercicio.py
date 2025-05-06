class Pessoa:
    def __init__(self, nome, idade):
        self.idade = idade
        self.nome = nome

    def apresentar(self):
        return f'Olá, meu nome é {self.nome} e tenho {self.idade} anos.'
pessoa1 = Pessoa('João', 30)
print(pessoa1.apresentar())


sorted# class Carro:
