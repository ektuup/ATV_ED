def gcd(a, b):
    if b > a:
        a, b = b, a
    while b != 0:
        r = a % b
        a = b
        b = r
    return a if a > 0 else -a

class fraction:
    def __init__(self, numer, denom):
        if denom == 0:
            raise ValueError("Erro: o denominador não pode ser 0")
        mdc = gcd(numer, denom)
        self.num = numer // mdc
        self.den = denom // mdc

        if(self.den < 0):
            self.den *= -1
            self.num *= -1

    def __str__(self):
        return f"{self.num}/{self.den}"
    
    def __add__(self, f2):
        sum_num = self.num * f2.den + f2.num * self.den
        sum_den = self.den * f2.den
        return fraction(sum_num, sum_den)

    def __sub__(self, f2):
        sub_num = self.num * f2.den - f2.num * self.den
        sub_den = self.den * f2.den
        return fraction(sub_num, sub_den)
    
    def __mul__(self, f2):
        mul_num = self.num * f2.num
        mul_den = self.den * f2.den
        return fraction(mul_num, mul_den)
    
    def __truediv__(self, f2):
        if f2.num == 0:
            raise ValueError("Erro: o Denominador nao pode ser 0")
        div_num = self.num * f2.den
        div_den = self.den * f2.num
        return fraction(div_num, div_den)

    def __eq__(self, f2):
        return self.num == f2.num and self.den == f2.den

    def __ne__(self, f2):
        return self.num != f2.num or self.den != f2.den

    def __gt__(self, f2):
        return self.num/self.den > f2.num/f2.den
    
    def __ge__(self, f2):
        return self.num/self.den >= f2.num/f2.den
    
    def __lt__(self, f2):
        return  self.num/self.den < f2.num/f2.den
    
    def __le__(self, f2):
        return self.num/self.den <= f2.num/f2.den

    def getNum(self):
        return self.num

    def getDen(self):
        return self.den

    def read(msg):
        while True:
            entrada = input(msg)
            try:
                partes = entrada.split("/")
                num = int(partes[0])
                den = int(partes[1])

                return fraction(num, den)
            except ValueError:
                print('Erro: o numerador e o denominador de uma fração são números inteiros')
            except IndexError:
                print('Erro: o numerador e o denominador de uma fração são separados por uma barra (/)')
            except ZeroDivisionError:
                print('Erro: o denominador não pode ser zero')