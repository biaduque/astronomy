__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"

'''
Este programa simula a plotagem de uma estrela com manchas, através de parâmetros como raio, intensidade, escurecimento 
de limbo, etc.
As bibliotecas importadas são: 
math
matplotlib
numpy
verify:função criada para validar entradas, por exemplo numeros nao float/int ou negativos
'''


import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from verify import Validar
import random


class estrela:
    '''
    A classe estrela recebe como objeto o raio, intensidade maxima, coeficientes de escurecimento de limbo.
    A estrela é formata em uma matriz de tamanho defeault 856.
    São objetos pertencentes a classe os parâmetros passados à mancha, como: raio, intensidade, longitude e latitude 
    em relação à estrela. 
    ************ PARÂMETROS DA ESTRELA***************
    :parâmetro raio: O raio da estrela
    :parâmetro intensidadeMaxima: Intensidade do centro da estrela
    :parâmetro coeficienteHum: Coeficiente de escurecimento de limbo 
    :parâmetro coeficienteDois: Coeficiete de escurecimento de limbo
    :parâmetro tamanhoMatriz: Tamanho da matriz em que será construída a estrela 
    :parâmetro estrela: Estrela construida com os coeficientes de escurecimento de limbo
    '''
   

    def __init__(self,raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz):
        
        self.raio=raio
        self.intensidadeMaxima=intensidadeMaxima
        self.coeficienteHum=coeficienteHum
        self.coeficienteDois=coeficienteDois
        self.tamanhoMatriz=tamanhoMatriz
        #self.colors = ["gray","pink","hot"]
        error=0
        self.estrela = [[ 0.0 for i in range(self.tamanhoMatriz)] for j in range(self.tamanhoMatriz)]

        for j in range(len(self.estrela)):
            for i in range(len(self.estrela[j])):
                distanciaCentro = math.sqrt(pow(i-self.tamanhoMatriz/2,2) + pow(j-self.tamanhoMatriz/2,2))
                if distanciaCentro <= self.raio:
                    cosTheta = cosTheta = math.sqrt(1-pow(distanciaCentro/self.raio,2))
                    self.estrela[i][j] = int(self.intensidadeMaxima * (1 - self.coeficienteHum *(1 - cosTheta) - self.coeficienteDois * (pow(1 - cosTheta, 2))))
    
        self.error=error
        self.Nx = self.tamanhoMatriz
        self.Ny = self.tamanhoMatriz
        #self.color = random.choice(self.colors)
        self.color = "hot"
        #Plotar(self.tamanhoMatriz,self.estrela)
    
    #######  inserir manchas


    def manchas(self,r,intensidadeMancha,lat,longt):
        '''
        Função onde é criada a(s) mancha(s) da estrela. Todos os parâmetros 
        são relacionados ao tamanho da estrela, podendo o usuário escolher valores 
        ou selecionar a opção default.
        *********INICIO DOS PARÂMETROS DA MANCHA*******
        :parâmetro raioMancha: Raio da mancha em relação ao raio da estrela 
        :parâmetro intensidadeMancha: Intensidade da mancha em funcao da intensidade maxima da estrela
        :parâmetro latitudeMancha: Coordenada de latitude da mancha em relação à estrela
        :parâmetro longitudeMancha: Coordenada de longitude da mancha em relação à estrela 
        
        '''
        # Parametros da mancha
        # #r=0.05 (teste)
        # intensidadeMancha=0.5 (teste)
        # coordenadas da mancha em graus
        #teste latitude=-30
        #teste longitude=20

        self.raioMancha = self.raio * r  # raio em funcao do raio da estrela em pixels
        self.intensidadeMancha = intensidadeMancha # intensidade da mancha em funcao da intensidade maxima da estrela

        #coordenadas de posicionamento da mancha em graus


        degreeToRadian = np.pi/180. #A read-only variable containing the floating-point value used to convert degrees to radians.
        self.latitudeMancha  = lat * degreeToRadian 
        self.longitudeMancha =  longt * degreeToRadian

        #posicao da mancha em pixels em relacao ao centro da estrela
        ys=self.raio*np.sin(self.latitudeMancha)  
        xs=self.raio*np.cos(self.latitudeMancha)*np.sin(self.longitudeMancha)
        anguloHelio=np.arccos(np.cos(self.latitudeMancha)*np.cos(self.longitudeMancha))

        
        # efeito de projecao pela mancha estar a um anguloHeliocentrico do centro da estrela - elipcidade
        yy = ys + self.Ny/2 # posicao em pixel com relacao à origem da matriz
        xx = xs + self.Nx/2 # posicao em pixel com relacao à origem da matriz

        kk = np.arange(self.Ny * self.Nx)
        vx = kk-self.Nx*np.int64(1.*kk/self.Nx) - xx
        vy = kk/self.Ny - yy

        # angulo de rotacao da mancha
        anguloRot=np.abs(np.arctan(ys/xs))    # em radianos
        if self.latitudeMancha*self.longitudeMancha > 0: anguloRot=-anguloRot

        ii, = np.where((((vx*np.cos(anguloRot)-vy*np.sin(anguloRot))/np.cos(anguloHelio))**2+(vx*np.sin(anguloRot)+vy*np.cos(anguloRot))**2) < self.raioMancha**2)
        
        spot = np.zeros(self.Ny * self.Nx) + 1
                
        spot[ii]=self.intensidadeMancha
        spot = spot.reshape([self.Ny, self.Nx])
    
        self.estrela= self.estrela * spot
        plt.axis([0,self.Nx,0,self.Ny])
                
        #self.estrelaManchada= estrelaManchada
        
        #Plotar(self.tamanhoMatriz,self.estrela)
        error=0
        self.error=error
        return self.estrela #retorna a decisão: se há manchas ou não

    #inserção de flares
    def faculas(self,estrela,count): 
        
         #recebe como parâmetro a estrela atualizada
        '''
        Função onde são criadas as fáculas da estrela. Todos os parâmetros 
        são relacionados ao tamanhdo da estrela, podendo o usuário escolher valores 
        ou selecionar a opção default.
        ---Parametros ainda nao definidos
        *********INICIO DOS PARÂMETROS FÁCULA*******
        :parâmetro 
        :parâmetro 
        :parâmetro 
        :parâmetro
        
        '''
        error=0
        self.error=error
        #vai sobrescrever a estrela que ele está criando, sendo ela a estrela ou a estrelaManchada.
        self.estrela=estrela
        return self.estrela #retorna a decisão: se há fácula ou não 
    
    def flares(self,estrela,count): #recebe como parâmetro a estrela atualizada
        '''
        Função onde são criadas os flares da estrela. Todos os parâmetros 
        são relacionados ao tamanhdo da estrela, podendo o usuário escolher valores 
        ou selecionar a opção default.
        ---Parametros ainda nao definidos
        *********INICIO DOS PARÂMETROS FLARES*******
        :parâmetro 
        :parâmetro 
        :parâmetro 
        :parâmetro
        
        '''

       
        error=0
        self.error=error
        #vai sobrescrever a estrela que ele está criando, sendo ela a estrela ou a estrelaManchada.
        self.estrela=estrela
        return self.estrela #retorna a decisão: se há flare ou não 


    def getNx(self):
        '''
        Retorna parâmetro Nx, necessário para o Eclipse.
        '''
        return self.Nx
    def getNy(self):
        '''
        Retorna parâmetro Ny, necessário para o Eclipse.
        '''
        return self.Ny

    def getRaioStar(self):
        '''
        Retorna o raio da estrela, necessário para o programa Eclipse, visto que o raio do planeta se dá em 
        relação ao raio da estrela.
        '''
        return self.raio
    def getEstrela(self):
        '''
        Retorna a estrela, plotada sem as manchas, necessário caso o usuário escolha a plotagem sem manchas.
        '''
        return self.estrela
    def getError(self):
        '''
        Retorna valor de erro. Se não houverem erros, a variável assumirá 0. Se houverem erros, o programa manterá
        o valor origem da variável (que é -1).
        '''
        return self.error

    def Plotar(self,tamanhoMatriz,estrela):
        Nx = tamanhoMatriz
        Ny = tamanhoMatriz
        plt.axis([0,Nx,0,Ny])
        plt.imshow(estrela,self.color)
        plt.show()