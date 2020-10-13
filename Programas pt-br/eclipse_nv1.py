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
    def __init__(self,Nx,Ny,raioEstrelaPixel,estrelaManchada,periodo,anguloInclinacao):

        self.Nx = Nx
        self.Ny = Ny
        self.raioEstrelaPixel = raioEstrelaPixel
        self.estrelaManchada = estrelaManchada
        self.periodo = periodo
        self.anguloInclinacao = anguloInclinacao

    def geraTempoHoras(self):

        x=int(input("Intervalo de tempo=1. Deseja alterar? 1. SIM | 2. NÃO:"))
        if x ==1:
            self.intervaloTempo=float(input('Digite o intervalo de tempo em minutos:'))
        elif x==2:
            self.intervaloTempo = 1.   # em minutos


        self.tamanhoMatriz= self.Nx #Nx ou Ny
        tempoHoras = (np.arange(self.tamanhoMatriz)-self.tamanhoMatriz/2)*self.intervaloTempo/60.   # em horas
        self.tempoHoras= tempoHoras


    def criarLua(self, radius, mass, albedo, distance, raioPlanetaPixel, raioStar,tempoHoras):
        moon = Moon(radius, mass, albedo, distance, self.raioEstrelaPixel, self.anguloInclinacao ,self.periodo, raioPlanetaPixel, self.tempoHoras)
        tempoHoras = self.tempoHoras
        moon.moonOrbit(raioStar)
        Rmoon = moon.getRmoon()
        self.Rmoon = Rmoon
        self.xm = moon.getxm()
        self.ym = moon.getym()
        self.Rmoon = Rmoon #em pixel 
        return moon
        


    def criarEclipse(self,semiEixoRaioStar, raioPlanetaRstar,lua):
        intervaloTempo = self.intervaloTempo
        tamanhoMatriz = self.tamanhoMatriz
        self.semiEixoRaioStar = semiEixoRaioStar
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
        latitudeTransito = -np.arcsin(self.semiEixoRaioStar*np.cos(self.anguloInclinacao*dtor))/dtor # latitude Sul (arbitraria)
        # duracao do transito em horas
        duracaoTransito=2 * (90.-np.arccos((np.cos(latitudeTransito*dtor))/self.semiEixoRaioStar)/dtor)*self.periodo/360*24. 
        tempoTotal = 3 * duracaoTransito
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
        curvaLuz = [ 1.0 for i in range(tamanhoMatriz)]
        self.curvaLuz=curvaLuz


        '''Parâmetros de órbita
        :parâmetro dteta: intervalo angular entre pontos da orbita
        :parâmetro tetaPos: angulos das posicaos do planeta na órbita
        :parâmetro xplaneta: x na matriz que projetará o planeta
        :parâmetro yplaneta: t na matriz que projetará o planeta
        '''
        dteta = 360*intervaloTempo/self.periodo/24./60   # intervalo angular entre pontos da orbita (em graus)

        # angulos das posicaos do planeta na órbita
        tetaPos = ((np.arange(tamanhoMatriz) - tamanhoMatriz/2)*dteta+270.)*dtor    # em radianos

        # orbita projetada do planeta
        xplaneta = semiEixoPixel*np.cos(tetaPos) + tamanhoMatriz/2
        yplaneta = semiEixoPixel*np.sin(tetaPos)*np.cos(self.anguloInclinacao*dtor) + tamanhoMatriz/2       



        if(self.anguloInclinacao > 90.): 
            yplaneta = -semiEixoPixel*np.sin(tetaPos)*np.cos(self.anguloInclinacao*dtor) + tamanhoMatriz/2

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

                        if (lua == True): 
                            #fazer a subtracao de xm e ym 
                            xm=x0-self.xm[i]         
                            ym=y0-self.ym[i]   

                        kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                        ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                    
                        plan[ii]=0.


                        ### adicionando luas ###

                        if (lua == True): #criou luas 
                            ll = np.where((kk/tamanhoMatriz-ym)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-xm)**2 <= self.Rmoon**2)
                            plan[ll]=0.

                        #####      
                            
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
    

    ############ adição de luas teste ###########
class Orbit (object):
    def __init__(self, semiaxis, period, inclinationAngle, obliquityAngle, eccentricity):
        self.semiaxis = semiaxis #(in Rstar)
        self.period = period #(in days), assumed circular orbit
        self.inclinationAngle = np.radians(inclinationAngle) #(in rad)
        self.obliquityAngle = obliquityAngle
        self.eccentricity = eccentricity
        
        
    def returndt(self): #intervalo entre os pontos
        return 2 #ou 20 testar   


class Moon ():
    
    #pm = 0.0751017821823 #moon period
    #rm = 0.0288431223213 # moon radius
    #dm = 4.10784266075 # moon distance
    tm0 = 1.15612181491 # moon first transit time
    #kind = 'big-fst_'
    
    pos = np.random.choice([-1, 1])
    
    
    def __init__(self, radius, mass, albedo, distance, raioEstrelaPixel, anguloInclinacao ,periodo, raioPlanetaPixel,tempoHoras):
        self.radius = radius
        self.mass = mass
        self.albedo = albedo
        self.distance = distance
        self.raioEstrelaPixel = raioEstrelaPixel
        self.anguloInclinacao = anguloInclinacao
        self.periodo = periodo
        self.raioPlanetaPixel = raioPlanetaPixel
        self.tempoHoras = tempoHoras
        
        
    # moon orbit in equatorial plane of planet
    def moonOrbit(self, raioStar):
        self.distance = self.distance * self.pos    
        #raio da lua em relacao ao raio da estrela 
        self.Rmoon = self.radius * raioStar
        self.RmoonPixel = self.Rmoon * self.raioEstrelaPixel
        
        dmoon = self.distance * self.raioPlanetaPixel
        theta_m0 = self.tm0
        
        theta_m = 2*np.pi * self.tempoHoras / (self.periodo*24.) - theta_m0
        self.xm = dmoon * np.cos(theta_m)
        self.ym = dmoon * np.sin(theta_m) * np.cos(self.anguloInclinacao) 
        
        pair = []
        pair.append(self.xm)
        pair.append(self.ym)
        
        return pair
    
    def getRmoon(self):
        return self.RmoonPixel


    def dMoon(self):
        return self.distance * self.raioPlanetaPixel
    
    def rMoon(self):
        return self.radius * self.raioPlanetaPixel

    def getxm(self):
        return self.xm

    def getym(self):
        return self.ym