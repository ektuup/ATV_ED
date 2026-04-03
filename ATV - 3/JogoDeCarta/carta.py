class Carta:
    def __init__(self, numero, naipe):
        try: 
            self.naipe = str(naipe)
        except ValueError:
            print('naipe deve ser uma string')
        self.num = numero

    def __str__(self):
        simb = ""
        if self.num == 1:
            simb = 'A'
        elif self.num == 11:
            simb = 'J'
        elif self.num == 12:
            simb = 'Q'
        elif self.num == 13:
            simb = 'K'
        else:
            simb = self.num
        return f"[{simb}{self.naipe}]"
    
    def __lt__(self, carta2): 
        if self.num != carta2.num:
            return self.num < carta2.num
        return self.naipe < carta2.naipe
    ##sobrecarregado para usar o .sort() automatico. a prioridade é ordenar por numero, se nao, por naipe lexicograficamente
