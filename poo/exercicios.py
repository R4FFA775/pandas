class Cachorro:
    def __init__ (self, nome, raca):
        self.nome = nome
        self.raca = raca

    def relatorio(self):
        return f'O cachorro {self.nome} é da raça {self.raca}.'
    
cachorro1 = Cachorro('Rex', 'Labrador')
print(cachorro1.relatorio())  
    
