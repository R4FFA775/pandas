class Calculadora: 
    def __init__(self, valor1, valor2):
        self.valor1 = valor1
        self.valor2 = valor2
#funções das operações
    def somar(self):
        return self.valor1 + self.valor2

    def subtrair(self):
        return self.valor1 - self.valor2

    def multiplicar(self):
        return self.valor1 * self.valor2

    def dividir(self):
        if self.valor2 != 0:
            return self.valor1 / self.valor2
        else:
            return "Divisão por zero não é permitida"
        
    
sorted
calculadora = Calculadora(10, 5)
    
print("Soma:", calculadora.somar())  
print("Subtração:", calculadora.subtrair()) 
print("Multiplicação:", calculadora.multiplicar()) 
print("Divisão:", calculadora.dividir())  