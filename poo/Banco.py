class ContaBancaria:
    def __init__(self, saldo):
        self.saldo = saldo
        self.conta = 2000

    def sacar(self, valor):
            if valor > self.saldo:
                return "Saldo insuficiente"
            else:
                self.saldo -= valor
                return f"Você sacou {valor}. Seu saldo atual é {self.saldo}."
            
    def depositar(self, valor):
        self.saldo += valor
        return f"Você depositou {valor}. Seu saldo atual é {self.saldo}."
 
conta = ContaBancaria(5000)
print(conta.sacar(2000))
print(conta.depositar(1000))
print(conta.sacar(5000))
#