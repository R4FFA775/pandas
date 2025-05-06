class livros:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
    def relatorio(self):
        return f'O livro {self.titulo} foi escrito por {self.autor} em {self.ano}.'

livro1 = livros('Dom Casmurro', 'Machado de Assis', 1899)
livro2 = livros('O Senhor dos Anéis', 'J.R.R. Tolkien', 1954)
livro3 = livros('1984', 'George Orwell', 1949)


class bilioteca:
    def __init__(self):
        self.livros = []
    
    def adicionar_livro(self, livro):
        self.livros.append(livro)
    
    def listar_livros(self):
        for livro in self.livros:
            print(livro.relatorio())
    
    def remover_livro(self, livro):
        if livro in self.livros:
            self.livros.remove(livro)
        else:
            print("Livro não encontrado na biblioteca.")

livro1 = livros('Dom Casmurro', 'Machado de Assis', 1899)
livro2 = livros('O Senhor dos Anéis', 'J.R.R. Tolkien', 1954)
livro3 = livros('1984', 'George Orwell', 1949)

bib = bilioteca()
bib.adicionar_livro(livro1)
bib.adicionar_livro(livro2)
bib.adicionar_livro(livro3)

print("Livros na biblioteca:")
bib.listar_livros()

print("\nRemovendo '1984' da biblioteca:")
bib.remover_livro(livro3)
print("\nLivros na biblioteca após remoção:")
bib.listar_livros()
