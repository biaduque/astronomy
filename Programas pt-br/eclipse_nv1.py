<<<<<<< HEAD
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
import matplotlib.animation as animation


import os


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
        
        # OUTPUT
        curvaLuz =[ 1.0 for i in range(self.Nx)]
        self.curvaLuz = curvaLuz

    def geraTempoHoras(self):

        x=int(input("Intervalo de tempo=1. Deseja alterar? 1. SIM | 2. NÃO:"))
        if x ==1:
            self.intervaloTempo=float(input('Digite o intervalo de tempo em minutos:'))
        elif x==2:
            self.intervaloTempo = 1.   # em minutos


        self.tamanhoMatriz= self.Nx #Nx ou Ny
        tempoHoras = (np.arange(self.tamanhoMatriz)-self.tamanhoMatriz/2)*self.intervaloTempo/60.   # em horas
        self.tempoHoras= tempoHoras

    #a partir do momento em que a lua é instanciada na main, esses objetos se tornam objetos da classe com self.
    def criarLua(self, radius, mass, raioPlanetaPixel, raioStar,tempoHoras,anguloInclinacao,periodo,distancia):
        moon = Moon(radius, mass, self.raioEstrelaPixel,anguloInclinacao ,periodo, raioPlanetaPixel, self.tempoHoras,distancia)
        tempoHoras = self.tempoHoras
        moon.moonOrbit(raioStar)
        Rmoon = moon.getRmoon()

        #coleta de dados necessarias para a plotagem do eclipse
        self.xxm = moon.getxm()
        self.yym = moon.getym()
        self.Rmoon = Rmoon #em pixel 
        self.mass = mass
        self.tamanhoMatriz= self.Nx
        self.ppMoon = moon.getppMoon(self.tamanhoMatriz)
        self.xl = moon.getxl()
        self.yl = moon.getyl()
        return moon
        


    def criarEclipse(self,semiEixoRaioStar, raioPlanetaRstar,periodo,anguloInclinacao,lua):

        intervaloTempo = self.intervaloTempo
        tamanhoMatriz = self.tamanhoMatriz
        self.semiEixoRaioStar = semiEixoRaioStar
        self.raioPlanetaRstar = raioPlanetaRstar
        self.periodo = periodo
        self.anguloInclinacao = anguloInclinacao

        dtor = np.pi/180.
        '''Inicio do calculo do TEMPO TOTAL de trânsito através dos parâmetros passados ao planeta.'''
        anguloObliquidade = 0. #default
        anguloRot = 0.  #default
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


        #seleciona a maior orbita para que a curva de luz seja plotada de maneira correta (observando ela inteira)
        if(lua == True):
            if (len(pp)>len(self.ppMoon)):
                rangeloop = pp
            else: 
                rangeloop = self.ppMoon
                xplan = xplaneta[self.ppMoon]
                yplan = yplaneta[self.ppMoon]
        else:
            rangeloop = pp

        ''''
        Curva de Luz e normalização da intensidade
        '''
        # maximo da curva de luz, usado na normalizacao da intensidade
        maxCurvaLuz = np.sum(self.estrelaManchada) 

        '''
        Criação da matriz para plotagem:
        '''
        #criacao de variaveis para plotagem da animacao 
        fig = plt.figure()
        ims = []
        j = 0 #variavel auxiliar utilizada para plotagem da animacao 
        plota = True #variavel FLAG que indica quando armazenar a imagem do PLOT 
        print("\nAguarde um momento, a animacao do trânsito está sendo gerada.\n")
        for i in range(0,len(rangeloop)):

                        plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. ##matriz de n por n
                        x0 = xplan[i] 
                        y0 = yplan[i]
                            
                        kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                        ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                    
                        plan[ii]=0.

                        ### adicionando luas ###
                        if (lua == True): #criou luas 
                            xm = x0-self.xxm[i]         
                            ym = y0-self.yym[i]   
                            ll = np.where((kk/tamanhoMatriz-ym)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-xm)**2 <= self.Rmoon**2)
                            plan[ll]=0.

                        #####      
                        plan = plan.reshape(self.tamanhoMatriz, self.tamanhoMatriz) #posicao adicionada na matriz
                        self.curvaLuz[rangeloop[i]]=np.sum(self.estrelaManchada*plan,dtype=float)/maxCurvaLuz

                        if(plota and self.curvaLuz[rangeloop[i]] != 1 and j<200):
                            plt.axis([0,self.Nx,0,self.Ny])
                            im = plt.imshow(self.estrelaManchada*plan,cmap="gray", animated = True)
                            ims.append([im]) #armazena na animação os pontos do grafico (em imagem)
                            j+=1
                        plota = not(plota) #variavel auxiliar que seleciona o intervalo correto para plotagem
        
        ani =animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000)
        plt.show()
        #ani.save('animacao_transito.gif',writer="PillowWriter") #salva o gif gerado na raiz do arquivo, para utilizacao do usuario

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
    def setEstrela(self,estrela):
        self.estrelaManchada = estrela

    

    ############ adição de luas ###########
class Orbit (object):
    def __init__(self, semiaxis, period, inclinationAngle, obliquityAngle, eccentricity):
        self.semiaxis = semiaxis #(in Rstar)
        self.period = period #(in days), assumed circular orbit
        self.inclinationAngle = np.radians(inclinationAngle) #(in rad)
        self.obliquityAngle = obliquityAngle
        self.eccentricity = eccentricity
        
        
    def returndt(self): #intervalo entre os pontos
        return 2 #ou 20 testar   


class Moon:
    
    pos = np.random.choice([-1, 1])

    def __init__(self, radius, mass, raioEstrelaPixel, anguloInclinacao ,periodo, raioPlanetaPixel,tempoHoras,distancia):
        
        tm0 = 0 # moon first transit time
        self.radius = radius
        self.mass = mass
        self.raioEstrelaPixel = raioEstrelaPixel
        self.anguloInclinacao = anguloInclinacao
        self.periodo = periodo
        self.tm0 = tm0 #default
        self.raioPlanetaPixel = raioPlanetaPixel
        self.tempoHoras = tempoHoras
        self.distancia = distancia
        
        
    # moon orbit in equatorial plane of planet
    def moonOrbit(self, raioStar):
        #raio da lua em relacao ao raio da estrela 
        self.Rmoon = self.radius / raioStar
        self.RmoonPixel = self.Rmoon * self.raioEstrelaPixel
        
        self.dmoon = self.distancia * self.raioEstrelaPixel
        
        self.theta_m = 2*np.pi * self.tempoHoras / (self.periodo*24.) - self.tm0
        self.xm = self.dmoon * np.cos(self.theta_m)
        self.ym = self.dmoon * np.sin(self.theta_m) * np.cos(self.anguloInclinacao) 
        
        #pair = []
        ##pair.append(self.xm)
        ##pair.append(self.ym)
        #return pair
    
    def getRmoon(self):
        return self.RmoonPixel

    def dMoon(self):
        return self.distancia * self.raioPlanetaPixel

    def getxm(self):
        return self.xm

    def getym(self):
        return self.ym

    def getppMoon(self,tamanhoMatriz):
        #calculando a orbita projetada da lua
        dtor = np.pi/180.
        xlua = self.xm + tamanhoMatriz/2
        ylua = self.ym + tamanhoMatriz/2
        if(self.anguloInclinacao > 90.): 
            ylua = -self.dmoon*np.sin(self.theta_m)*np.cos(self.anguloInclinacao*dtor) + tamanhoMatriz/2

        #orbita projetada da Lua
        ppMoon, = np.where((xlua >= 0) & (xlua < tamanhoMatriz) & (ylua >= 0) & (ylua < tamanhoMatriz)) 
        self.xl = xlua[ppMoon]
        self.yl = ylua[ppMoon]
        return ppMoon   
    
    def getxl(self):
        return self.xl
    def getyl(self):
=======
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
import matplotlib.animation as animation


import os


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
        
        # OUTPUT
        curvaLuz =[ 1.0 for i in range(self.Nx)]
        self.curvaLuz = curvaLuz

    def geraTempoHoras(self):

        x=int(input("Intervalo de tempo=1. Deseja alterar? 1. SIM | 2. NÃO:"))
        if x ==1:
            self.intervaloTempo=float(input('Digite o intervalo de tempo em minutos:'))
        elif x==2:
            self.intervaloTempo = 1.   # em minutos


        self.tamanhoMatriz= self.Nx #Nx ou Ny
        tempoHoras = (np.arange(self.tamanhoMatriz)-self.tamanhoMatriz/2)*self.intervaloTempo/60.   # em horas
        self.tempoHoras= tempoHoras

    #a partir do momento em que a lua é instanciada na main, esses objetos se tornam objetos da classe com self.
    def criarLua(self, radius, mass, raioPlanetaPixel, raioStar,tempoHoras,anguloInclinacao,periodo,distancia):
        moon = Moon(radius, mass, self.raioEstrelaPixel,anguloInclinacao ,periodo, raioPlanetaPixel, self.tempoHoras,distancia)
        tempoHoras = self.tempoHoras
        moon.moonOrbit(raioStar)
        Rmoon = moon.getRmoon()

        #coleta de dados necessarias para a plotagem do eclipse
        self.xxm = moon.getxm()
        self.yym = moon.getym()
        self.Rmoon = Rmoon #em pixel 
        self.mass = mass
        self.tamanhoMatriz= self.Nx
        self.ppMoon = moon.getppMoon(self.tamanhoMatriz)
        self.xl = moon.getxl()
        self.yl = moon.getyl()
        return moon
        


    def criarEclipse(self,semiEixoRaioStar, raioPlanetaRstar,periodo,anguloInclinacao,lua):

        intervaloTempo = self.intervaloTempo
        tamanhoMatriz = self.tamanhoMatriz
        self.semiEixoRaioStar = semiEixoRaioStar
        self.raioPlanetaRstar = raioPlanetaRstar
        self.periodo = periodo
        self.anguloInclinacao = anguloInclinacao

        dtor = np.pi/180.
        '''Inicio do calculo do TEMPO TOTAL de trânsito através dos parâmetros passados ao planeta.'''
        anguloObliquidade = 0. #default
        anguloRot = 0.  #default
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


        #seleciona a maior orbita para que a curva de luz seja plotada de maneira correta (observando ela inteira)
        if(lua == True):
            if (len(pp)>len(self.ppMoon)):
                rangeloop = pp
            else: 
                rangeloop = self.ppMoon
                xplan = xplaneta[self.ppMoon]
                yplan = yplaneta[self.ppMoon]
        else:
            rangeloop = pp

        ''''
        Curva de Luz e normalização da intensidade
        '''
        # maximo da curva de luz, usado na normalizacao da intensidade
        maxCurvaLuz = np.sum(self.estrelaManchada) 

        '''
        Criação da matriz para plotagem:
        '''
        #criacao de variaveis para plotagem da animacao 
        fig = plt.figure()
        ims = []
        j = 0 #variavel auxiliar utilizada para plotagem da animacao 
        plota = True #variavel FLAG que indica quando armazenar a imagem do PLOT 
        print("\nAguarde um momento, a animacao do trânsito está sendo gerada.\n")
        for i in range(0,len(rangeloop)):

                        plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. ##matriz de n por n
                        x0 = xplan[i] 
                        y0 = yplan[i]
                            
                        kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                        ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                    
                        plan[ii]=0.

                        ### adicionando luas ###
                        if (lua == True): #criou luas 
                            xm = x0-self.xxm[i]         
                            ym = y0-self.yym[i]   
                            ll = np.where((kk/tamanhoMatriz-ym)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-xm)**2 <= self.Rmoon**2)
                            plan[ll]=0.

                        #####      
                        plan = plan.reshape(self.tamanhoMatriz, self.tamanhoMatriz) #posicao adicionada na matriz
                        self.curvaLuz[rangeloop[i]]=np.sum(self.estrelaManchada*plan,dtype=float)/maxCurvaLuz

                        if(plota and self.curvaLuz[rangeloop[i]] != 1 and j<200):
                            plt.axis([0,self.Nx,0,self.Ny])
                            im = plt.imshow(self.estrelaManchada*plan,cmap="gray", animated = True)
                            ims.append([im]) #armazena na animação os pontos do grafico (em imagem)
                            j+=1
                        plota = not(plota) #variavel auxiliar que seleciona o intervalo correto para plotagem
        
        ani =animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000)
        plt.show()
        #ani.save('animacao_transito.gif',writer="PillowWriter") #salva o gif gerado na raiz do arquivo, para utilizacao do usuario

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
    def setEstrela(self,estrela):
        self.estrelaManchada = estrela

    

    ############ adição de luas ###########
class Orbit (object):
    def __init__(self, semiaxis, period, inclinationAngle, obliquityAngle, eccentricity):
        self.semiaxis = semiaxis #(in Rstar)
        self.period = period #(in days), assumed circular orbit
        self.inclinationAngle = np.radians(inclinationAngle) #(in rad)
        self.obliquityAngle = obliquityAngle
        self.eccentricity = eccentricity
        
        
    def returndt(self): #intervalo entre os pontos
        return 2 #ou 20 testar   


class Moon:
    
    pos = np.random.choice([-1, 1])

    def __init__(self, radius, mass, raioEstrelaPixel, anguloInclinacao ,periodo, raioPlanetaPixel,tempoHoras,distancia):
        
        tm0 = 0 # moon first transit time
        self.radius = radius
        self.mass = mass
        self.raioEstrelaPixel = raioEstrelaPixel
        self.anguloInclinacao = anguloInclinacao
        self.periodo = periodo
        self.tm0 = tm0 #default
        self.raioPlanetaPixel = raioPlanetaPixel
        self.tempoHoras = tempoHoras
        self.distancia = distancia
        
        
    # moon orbit in equatorial plane of planet
    def moonOrbit(self, raioStar):
        #raio da lua em relacao ao raio da estrela 
        self.Rmoon = self.radius / raioStar
        self.RmoonPixel = self.Rmoon * self.raioEstrelaPixel
        
        self.dmoon = self.distancia * self.raioEstrelaPixel
        
        self.theta_m = 2*np.pi * self.tempoHoras / (self.periodo*24.) - self.tm0
        self.xm = self.dmoon * np.cos(self.theta_m)
        self.ym = self.dmoon * np.sin(self.theta_m) * np.cos(self.anguloInclinacao) 
        
        #pair = []
        ##pair.append(self.xm)
        ##pair.append(self.ym)
        #return pair
    
    def getRmoon(self):
        return self.RmoonPixel

    def dMoon(self):
        return self.distancia * self.raioPlanetaPixel

    def getxm(self):
        return self.xm

    def getym(self):
        return self.ym

    def getppMoon(self,tamanhoMatriz):
        #calculando a orbita projetada da lua
        dtor = np.pi/180.
        xlua = self.xm + tamanhoMatriz/2
        ylua = self.ym + tamanhoMatriz/2
        if(self.anguloInclinacao > 90.): 
            ylua = -self.dmoon*np.sin(self.theta_m)*np.cos(self.anguloInclinacao*dtor) + tamanhoMatriz/2

        #orbita projetada da Lua
        ppMoon, = np.where((xlua >= 0) & (xlua < tamanhoMatriz) & (ylua >= 0) & (ylua < tamanhoMatriz)) 
        self.xl = xlua[ppMoon]
        self.yl = ylua[ppMoon]
        return ppMoon   
    
    def getxl(self):
        return self.xl
    def getyl(self):
>>>>>>> 3b7c4e723644f9d17e150534deda176eb47ed175
        return self.yl