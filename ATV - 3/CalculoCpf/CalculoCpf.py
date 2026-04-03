import os

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.cpf = None

    def calculaDigito(self, lista_cpf):
            sum = 0
            for i in range(len(lista_cpf)):
                sum += lista_cpf[i] * (2 + i)
            resto = sum % 11
            if resto <= 1:
                return 0
            else:
                return 11 - resto

    def cpfAnalise(self):
        print(f"Olá, {self.nome}!")
        while True:
            limpatela()
            self.cpf = input("Digite o CPF a ser analisado:\n(Apenas os 11 dígitos, sem pontuação)\n")
            try:
                int(self.cpf)
                if len(self.cpf) != 11:
                    raise TypeError
                break
            except:
                print("Erro!!!\nDigite o CPF a ser verificado com apenas onze números e nada mais.\n")
        
        int_cpf = int(self.cpf)
        lista_cpf = []

        p_digitofornecido = int_cpf % 100
        s_digitofornecido = p_digitofornecido % 10
        p_digitofornecido = p_digitofornecido // 10

        int_cpf = int_cpf // 100

        for i in range(9):
            lista_cpf.append(int_cpf % 10)
            int_cpf = int_cpf // 10

        p_digito = self.calculaDigito(lista_cpf)

        lista_cpf.reverse()
        lista_cpf.append(p_digito)
        lista_cpf.reverse()

        s_digito = self.calculaDigito(lista_cpf)

        lista_cpf.reverse()
        lista_cpf.append(s_digito)

        print()
        if p_digito == p_digitofornecido and s_digito == s_digitofornecido:
            print("CPF válido.\n")
        else:
            print("CPF inválido.")
            print(f"CPF válido deveria ser: ", end="")
            for i in range(11):
                if i == 3 or i == 6:
                    print(".", end="")
                elif i == 9:
                    print("-", end="")
                print(lista_cpf[i], end="")
            print()
        print()

def limpatela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    limpatela()
    print("---------------------------------")
    print("Boas vindas ao calculador de CPF!")
    print("---------------------------------")
    print()
    
    menuUsuario()
    
    while True:
        print("Deseja consultar CPF de novo usuário?")
        try:
            op = int(input("1 - Sim\n2 - Não\n"))
            limpatela()
            match op:
                case 1:
                    menuUsuario()
                case 2:
                    print("Até logo!\nFim do programa...")
                    break
                case _:
                    raise Error
        except:
            print("Erro!\nPor favor, digite um digito válido.")

def menuUsuario():
    usuario = Usuario(input("Como devemos te chamar? "))
    limpatela()
    usuario.cpfAnalise()

if __name__ == "__main__":
    menu()
