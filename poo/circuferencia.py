class Circulo:
    def __init__(self,raio):
        self.raio = raio

    def area(self):
        return 3.14 * self.raio ** 2
def circuferencia(raio):
    return 2 * 3.14 * raio
circ = Circulo(3)
print(circ.area())