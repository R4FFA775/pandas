import csv
from datetime import datetime, timedelta


class Livro:
    def __init__(self, titulo, autor, ano, categoria, isbn, disponivel=True):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.categoria = categoria
        self.isbn = isbn
        self.disponivel = disponivel

    def validar_isbn(self):
        if len(self.isbn) == 13 and self.isbn.isdigit():
            return True
        return False

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            return True
        return False

    def devolver(self):
        self.disponivel = True
        return True

    def detalhes(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} - {self.autor} ({self.ano}) | ISBN: {self.isbn} | Categoria: {self.categoria} | Status: {status}"


class Usuario:
    ID_COUNTER = 1  # Contador automático de ID

    def __init__(self, nome):
        self.nome = nome
        self.id = Usuario.ID_COUNTER
        Usuario.ID_COUNTER += 1
        self.__livros_emprestados = {}  # {livro: data_emprestimo}
        self.__limite = 3
        self.atrasos = 0

    def pegar_emprestado(self, livro):
        if len(self.__livros_emprestados) >= self.__limite:
            print(f"{self.nome} atingiu o limite de empréstimos.")
            return False
        if livro.emprestar():
            self.__livros_emprestados[livro] = datetime.now()
            return True
        else:
            print(f"Livro '{livro.titulo}' não está disponível.")
            return False

    def devolver_livro(self, livro):
        for l in list(self.__livros_emprestados.keys()):
            if l.isbn == livro.isbn:
                livro.devolver()
                data_emprestimo = self.__livros_emprestados.pop(l)
                dias = (datetime.now() - data_emprestimo).days
                if dias > 14:
                    self.atrasos += 1
                    print(f"{self.nome} devolveu com atraso de {dias - 14} dias.")
                return True
        return False

    def tem_atrasos(self):
        for livro, data in self.__livros_emprestados.items():
            if (datetime.now() - data).days > 14:
                return True
        return False

    def bloqueado(self):
        return self.atrasos > 3

    def __str__(self):
        return f"{self.nome} (ID: {self.id})"


class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.carregar_dados()

    def cadastrar_livro(self, livro):
        if livro.validar_isbn():
            self.livros.append(livro)
            return True
        print(f"ISBN inválido para o livro {livro.titulo}")
        return False

    def cadastrar_usuario(self, usuario):
        if any(u.nome == usuario.nome for u in self.usuarios):
            print("Usuário já cadastrado.")
            return False
        self.usuarios.append(usuario)
        return True

    def buscar_livro(self, termo):
        resultados = []
        for livro in self.livros:
            if (termo.lower() in livro.titulo.lower() or
                termo.lower() in livro.autor.lower() or
                termo == livro.isbn):
                resultados.append(livro)
        return resultados

    def listar_livros(self):
        for livro in self.livros:
            print(livro.detalhes())

    def salvar_dados(self):
        # Salvar livros
        with open('livros.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['titulo', 'autor', 'ano', 'categoria', 'isbn', 'disponivel'])
            for livro in self.livros:
                writer.writerow([
                    livro.titulo,
                    livro.autor,
                    livro.ano,
                    livro.categoria,
                    livro.isbn,
                    str(livro.disponivel)
                ])

        # Salvar usuários
        with open('usuarios.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['nome', 'id', 'atrasos'])
            for usuario in self.usuarios:
                writer.writerow([
                    usuario.nome,
                    usuario.id,
                    usuario.atrasos
                ])

    def carregar_dados(self):
        try:
            # Carregar livros
            with open('livros.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    livro = Livro(
                        row['titulo'],
                        row['autor'],
                        int(row['ano']),
                        row['categoria'],
                        row['isbn'],
                        row['disponivel'].strip().lower() == 'true'
                    )
                    self.livros.append(livro)

            # Carregar usuários
            with open('usuarios.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    usuario = Usuario(row['nome'])
                    usuario.id = int(row['id'])
                    usuario.atrasos = int(row['atrasos'])
                    self.usuarios.append(usuario)

            # Atualizar contador de ID
            if self.usuarios:
                Usuario.ID_COUNTER = max(u.id for u in self.usuarios) + 1

        except FileNotFoundError:
            print("Arquivos de dados não encontrados. Iniciando biblioteca vazia.")


def limpar_tela():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    print("\n=== SISTEMA DE BIBLIOTECA ===")
    print("1. Cadastrar novo livro")
    print("2. Cadastrar novo usuário")
    print("3. Emprestar livro")
    print("4. Devolver livro")
    print("5. Buscar livro")
    print("6. Listar todos os livros")
    print("7. Listar usuários")
    print("0. Sair")
    return input("\nEscolha uma opção: ")


def main():
    biblioteca = Biblioteca()
    while True:
        limpar_tela()
        opcao = menu()

        if opcao == "1":
            print("\n=== Cadastrar Novo Livro ===")
            titulo = input("Título: ")
            autor = input("Autor: ")
            try:
                ano = int(input("Ano: "))
            except ValueError:
                print("Ano inválido!")
                continue
            categoria = input("Categoria: ")
            isbn = input("ISBN (13 dígitos): ")
            if len(isbn) != 13 or not isbn.isdigit():
                print("ISBN inválido!")
                continue
            livro = Livro(titulo, autor, ano, categoria, isbn)
            biblioteca.cadastrar_livro(livro)
            print("Livro cadastrado com sucesso!")

        elif opcao == "2":
            print("\n=== Cadastrar Novo Usuário ===")
            nome = input("Nome do usuário: ")
            usuario = Usuario(nome)
            if biblioteca.cadastrar_usuario(usuario):
                print("Usuário cadastrado com sucesso!")

        elif opcao == "3":
            print("\n=== Emprestar Livro ===")
            termo = input("Digite o título ou ISBN do livro: ")
            resultados = biblioteca.buscar_livro(termo)
            if resultados:
                print("\nLivros encontrados:")
                for i, livro in enumerate(resultados):
                    print(f"{i+1}. {livro.detalhes()}")
                try:
                    escolha = int(input("\nEscolha o número do livro (0 para cancelar): ")) - 1
                    if escolha == -1:
                        continue
                    elif 0 <= escolha < len(resultados):
                        id_usuario = int(input("Digite o ID do usuário: "))
                        usuario = next((u for u in biblioteca.usuarios if u.id == id_usuario), None)
                        if usuario:
                            if usuario.pegar_emprestado(resultados[escolha]):
                                print("Livro emprestado com sucesso!")
                        else:
                            print("Usuário não encontrado!")
                except ValueError:
                    print("Opção inválida!")
            else:
                print("Nenhum livro encontrado.")

        elif opcao == "4":
            print("\n=== Devolver Livro ===")
            try:
                id_usuario = int(input("Digite o ID do usuário: "))
                usuario = next((u for u in biblioteca.usuarios if u.id == id_usuario), None)
                if usuario:
                    termo = input("Digite o título ou ISBN do livro: ")
                    resultados = biblioteca.buscar_livro(termo)
                    if resultados:
                        for livro in resultados:
                            if usuario.devolver_livro(livro):
                                print("Livro devolvido com sucesso!")
                                break
                        else:
                            print("Livro não encontrado ou não está emprestado para este usuário!")
                    else:
                        print("Livro não encontrado.")
                else:
                    print("Usuário não encontrado!")
            except ValueError:
                print("ID inválido.")

        elif opcao == "5":
            print("\n=== Buscar Livro ===")
            termo = input("Digite o termo de busca: ")
            resultados = biblioteca.buscar_livro(termo)
            if resultados:
                print("\nLivros encontrados:")
                for livro in resultados:
                    print(livro.detalhes())
            else:
                print("Nenhum livro encontrado.")

        elif opcao == "6":
            print("\n=== Lista de Todos os Livros ===")
            biblioteca.listar_livros()

        elif opcao == "7":
            print("\n=== Lista de Usuários ===")
            for usuario in biblioteca.usuarios:
                print(usuario)

        elif opcao == "0":
            print("\nSalvando dados...")
            biblioteca.salvar_dados()
            print("Dados salvos com sucesso!")
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()