__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"

'''
Programa que simula o eclipse e a curva de luz de um planeta ao transitar 
sua host star.
Nesse programa é calculada a curva de luz da estrela em relação aos parâmetros do planeta adicionados
pelo usuário.
***Bibliotecas importadas***
numpy:
matplotlib:
estrela: arquivo de programa onde são calculados os parâmetros da estrela, dado os inputs do usuário (raio, intensidade,etc)
verify:função criada para validar entradas, por exemplo numeros nao float/int ou negativos
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
from estrela_nv1 import estrela
from verify import Validar

class Eclipse:
    '''
    Criação da classe eclipse, que retornará a curva de luz do trânsito do planeta ao redor da estrela


    ****parâmetros atribuidos ao planeta****
    :parâmetro periodo: período de rotação do planeta
    :parâmetro SemiEixoRaioStar: semi eixo do planeta em relação ao raio da estrela
    :parâmetro anguloInclinacao: angulo de inclinação do planeta
    :parâmetro raioPlanetaRstar: raio do planeta
    '''
    def __init__(self,Nx,Ny,raioEstrelaPixel,estrelaManchada):

        self.Nx = Nx
        self.Ny = Ny
        self.raioEstrelaPixel = raioEstrelaPixel
        self.estrelaManchada = estrelaManchada


    def criarEclipse(self, periodo, semiEixoRaioStar, anguloInclinacao, raioPlanetaRstar):
        self.periodo = periodo
        self.semiEixoRaioStar = semiEixoRaioStar
        self.anguloInclinacao = anguloInclinacao
        self.raioPlanetaRstar = raioPlanetaRstar

        dtor = np.pi/180.
        '''Inicio do calculo do TEMPO TOTAL de trânsito através dos parâmetros passados ao planeta.'''
        #default
        anguloObliquidade = 0.
        anguloRot = 0.
        #default
        semiEixoPixel = self.semiEixoRaioStar * self.raioEstrelaPixel
        raioPlanetaPixel = self.raioPlanetaRstar * self.raioEstrelaPixel

        # latitude of projected transit, for zero obliquity
        latitudeTransito = -np.arcsin(self.semiEixoRaioStar*np.cos(anguloInclinacao*dtor))/dtor # latitude Sul (arbitraria)
        # duracao do transito em horas
        duracaoTransito=2 * (90.-np.arccos((np.cos(latitudeTransito*dtor))/self.semiEixoRaioStar)/dtor)*self.periodo/360*24. 
        tempoTotal = 3 * duracaoTransito

        x=int(input("Intervalo de tempo=1. Deseja alterar? 1. SIM | 2. NÃO:"))
        if x ==1:
            intervaloTempo=float(input('Digite o intervalo de tempo em minutos:'))
        elif x==2:
            intervaloTempo = 1.   # em minutos

        self.tempoTotal= tempoTotal


        '''
        Inicio do calculo do tempo em Horas e da curva de Luz na matriz
        :parâmetro nn: calculo do numero de pontos na curva de luz
        :parâmetro tamanhoMatriz: recebe a estrela manchada para depois plotar o planeta
        :parâmetro tempoHoras: calcula o tempo do transito em horas, transformando-o em objeto da classe Eclipse
        :parâmetro curvaLuz: calcula a curva de luz do transito do planeta ao eclipsar a estrela, também se torna 
        objeto de Eclipse       
        '''
        
        # calculo do numero de pontos na curva de luz
        nn=np.fix(tempoTotal*60./intervaloTempo)

        # OUTPUT
        tamanhoMatriz= self.Nx #Nx ou Ny

        tempoHoras = (np.arange(tamanhoMatriz)-tamanhoMatriz/2)*intervaloTempo/60.   # em horas
        self.tempoHoras= tempoHoras
        curvaLuz = [ 1.0 for i in range(tamanhoMatriz)]
        self.curvaLuz=curvaLuz


        '''Parâmetros de órbita
        :parâmetro dteta: intervalo angular entre pontos da orbita
        :parâmetro tetaPos: angulos das posicaos do planeta na órbita
        :parâmetro xplaneta: x na matriz que projetará o planeta
        :parâmetro yplanetas: t na matriz que projetará o planeta
        '''
        dteta = 360*intervaloTempo/self.periodo/24./60   # intervalo angular entre pontos da orbita (em graus)

        # angulos das posicaos do planeta na órbita
        tetaPos = ((np.arange(tamanhoMatriz) - tamanhoMatriz/2)*dteta+270.)*dtor    # em radianos

        # orbita projetada do planeta
        xplaneta = semiEixoPixel*np.cos(tetaPos) + tamanhoMatriz/2
        yplaneta = semiEixoPixel*np.sin(tetaPos)*np.cos(anguloInclinacao*dtor) + tamanhoMatriz/2

        if(anguloInclinacao > 90.): 
            yplaneta = -semiEixoPixel*np.sin(tetaPos)*np.cos(anguloInclinacao*dtor) + tamanhoMatriz/2

        pp, = np.where((xplaneta >= 0) & (xplaneta < tamanhoMatriz) & (yplaneta >= 0) & (yplaneta < tamanhoMatriz))    # only points within the matrix
        xplan = xplaneta[pp]
        yplan = yplaneta[pp]
        ''''
        Curva de Luz e normalização da intensidade
        '''
        # maximo da curva de luz, usado na normalizacao da intensidade
        maxCurvaLuz = np.sum(self.estrelaManchada) 

        

        '''
        Criação da matriz para plotagem:
        '''
        for i in range(0,len(pp)):

                        plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. ##matriz de n por n
                        x0=xplan[i]
                        y0=yplan[i]

                        kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                        ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                    
                        plan[ii]=0.
                        plan = plan.reshape([tamanhoMatriz,tamanhoMatriz])
                        
                        curvaLuz[pp[i]]=np.sum(self.estrelaManchada*plan,dtype=float)/maxCurvaLuz

                        if(i == len(pp)/2):
                            plt.axis([0,self.Nx,0,self.Ny])
                            plt.imshow(len(self.estrelaManchada)*plan,cmap="gray")
                            plt.show()




        error=0
        self.error=error

    '''Chamada dos objetos atribuídos à classe Eclipse.'''
    def getTempoTransito(self):
        '''Retorna o parâmetro tempoTotal, representando o tempo de trânsito do planeta em sua host star.'''
        return self.tempoTotal
    def getTempoHoras(self):
        '''Retorna o parâmetro tempoHoras, representando o tempo de trânsito do planeta em sua host star em Horas.'''
        return self.tempoHoras
    def getCurvaLuz(self):
        '''Retorna o parâmetro curvaLuz, representando a curva de luz da estrela que possui um planeta a orbitar nela.'''
        return self.curvaLuz
    def getError(self):
        '''
        Retorna o valor de erro, ocorrendo ou não algum. Se não houver erro, recebe 0. Se houver, a variável terá
        seu valor de inicio (que é -1)
        '''
        return self.error
    
    

