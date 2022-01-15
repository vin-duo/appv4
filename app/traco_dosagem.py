
class Ensaio():
    
    #Atribuir valores default nas variaveis do __init__ conforme sugestoes do Americo.
    def __init__(self,m=5, cp=13.56, alfa=0, alfaantigo=0, agua=0, umidade=0, pesobrita=0, arredondamento=3):
        self.m = m
        self.cp = cp
        self.alfa = alfa/100 #para dar em (%)
        self.agua = agua
        self.umidade = umidade
        self.pesobrita = pesobrita
        self.alfaantigo = alfaantigo/100
        self.arredondamento = arredondamento

    def massas_unitarias(self):
        cimento_unitario = 1
        areia_unitario= round(self.alfa*(1+self.m)-1, self.arredondamento)
        pedra_unitario = round(self.m-areia_unitario, self.arredondamento)
        return(cimento_unitario, areia_unitario, pedra_unitario)

    def massas_iniciais(self):
        a = self.alfa*(1+self.m)-1
        p = self.m-a
        massa_cimento = round(self.pesobrita/p, self.arredondamento)
        massa_areia = round(self.pesobrita*a/p, self.arredondamento)
        massa_pedra = round(self.pesobrita, self.arredondamento)
        return(massa_cimento, massa_areia, massa_pedra)

    def massas_iniciais_antigas(self):
        if self.alfaantigo == 0:
            return(0,0)
        else:
            a = self.alfaantigo*(1+self.m)-1
            p = self.m-a
            massa_cimento = round(self.pesobrita/p, self.arredondamento)
            massa_areia = round(self.pesobrita*a/p, self.arredondamento)
            massa_pedra = round(self.pesobrita, self.arredondamento)
            return(massa_cimento, massa_areia, massa_pedra)

    def quantidades_adicionar(self):
        if self.alfaantigo == 0:
            return(0,0)
        else:
            massa_antiga = self.massas_iniciais_antigas()
            massa_nova = self.massas_iniciais()
            adicionar_cimento = round(massa_nova[0] - massa_antiga[0], self.arredondamento)
            adicionar_areia = round(massa_nova[1] - massa_antiga[1], self.arredondamento)
            return(adicionar_cimento, adicionar_areia)

    def umidade_agregado(self):
        fator_umidade = self.umidade/100
        areia_seca = self.massas_iniciais()[1]
        areia_umida = round(areia_seca/(1-fator_umidade), self.arredondamento)
        massa_de_agua = round(areia_umida - areia_seca, self.arredondamento)
        return(areia_umida, massa_de_agua)

    def agua_cimento(self):
        cimento = self.massas_iniciais()[0]
        ac = self.agua/cimento
        return(ac)

