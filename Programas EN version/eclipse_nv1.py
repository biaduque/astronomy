__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"

'''
Program that simulates the eclipse and light curve of a planet as it transits
host star.
In this program, a star light curve is calculated in relation to the parameters of the planet added 
by the user.
*** Imported libraries ***
numpy:
matplotlib:
star: program file where's star parameters are calculated, given user data (radius, intensity, etc.)
check: function created to validate entries, for example, non-floating numbers / int or negative numbers
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
from star_nv1 import estrela
from verify import Validar

class Eclipse:
    '''
  Creation of the eclipse class, which will return the traffic light curve of the planet "surrounding the star


     **** parameters assigned to the planet ****
     : periodo parameter: planet's rotation period
     : SemiEixoRaioStar parameter: planet's semi axis  in relation to the star's radius
     : anguloInclination parameter: planet's tilt angle
     : raioPlanetaRstar parameter: planet's radius
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
        '''Calculation's start of the ENTIRE transit TIME using parameters assigned to the planet.'''
        #default
        anguloObliquidade = 0.
        anguloRot = 0.
        #default
        semiEixoPixel = self.semiEixoRaioStar * self.raioEstrelaPixel
        raioPlanetaPixel = self.raioPlanetaRstar * self.raioEstrelaPixel

        # latitude of projected transit, for zero obliquity
        latitudeTransito = -np.arcsin(self.semiEixoRaioStar*np.cos(anguloInclinacao*dtor))/dtor # latitude Sul (arbitraria)
        # transit time in hours
        duracaoTransito=2 * (90.-np.arccos((np.cos(latitudeTransito*dtor))/self.semiEixoRaioStar)/dtor)*self.periodo/360*24. 
        tempoTotal = 3 * duracaoTransito

        x=int(input("Time period = 1. Do you want to change? 1. YES | 2. NO:"))
        if x ==1:
            intervaloTempo=float(input('Enter the time interval in minutes:'))
        elif x==2:
            intervaloTempo = 1.   #in minutes

        self.tempoTotal= tempoTotal


        '''
        Start of the time calculation in Hours and the Light curve in the matrix
         :nn  parameter: calculation's number of dots on the light curve
         :tamanhoMatrix parameter: receives the spotted star and then plot the planet
         :tempoHoras parameter: calculates transit time in hours, transforming it into an Eclipse class object
         : parameter curveLight: calculates the light curve of the planet's transit when eclipsing the star. It also becomes
         an Eclipse object     
        '''
        
        # calculation of the number of dots on the light curve
        nn=np.fix(tempoTotal*60./intervaloTempo)

        # OUTPUT
        tamanhoMatriz= self.Nx #Nx or Ny

        tempoHoras = (np.arange(tamanhoMatriz)-tamanhoMatriz/2)*intervaloTempo/60.   # in hours
        self.tempoHoras= tempoHoras
        curvaLuz = [ 1.0 for i in range(tamanhoMatriz)]
        self.curvaLuz=curvaLuz


        '''
        Orbit parameters
         : dteta parameter: angular interval between points of the orbit
         : tetaPos parameter: angles of the planet's positions in orbit
         : xplaneta parameter: x in the matrix that projects the planet
         : yplaneta parameter: t in the matrix that projects the planet
        '''
        dteta = 360*intervaloTempo/self.periodo/24./60   # angular range between orbiting points (in degrees)

        # angles of planet positions in orbit
        tetaPos = ((np.arange(tamanhoMatriz) - tamanhoMatriz/2)*dteta+270.)*dtor    #in radians

        #"planet's projected orbit
        xplaneta = semiEixoPixel*np.cos(tetaPos) + tamanhoMatriz/2
        yplaneta = semiEixoPixel*np.sin(tetaPos)*np.cos(anguloInclinacao*dtor) + tamanhoMatriz/2

        if(anguloInclinacao > 90.): 
            yplaneta = -semiEixoPixel*np.sin(tetaPos)*np.cos(anguloInclinacao*dtor) + tamanhoMatriz/2

        pp, = np.where((xplaneta >= 0) & (xplaneta < tamanhoMatriz) & (yplaneta >= 0) & (yplaneta < tamanhoMatriz))    # only points within the matrix
        xplan = xplaneta[pp]
        yplan = yplaneta[pp]
        ''''
        Light curve and intensity normalization
        '''
        #light curve's maximum, used to normalize the intensity
        maxCurvaLuz = np.sum(self.estrelaManchada) 

        

        '''
        Creation of the matrix for plotting:
        '''
        for i in range(0,len(pp)):

                        plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. #n-by-n matrix
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

    '''Calling and returning objects assigned to the Eclipse class'''
    def getTempoTransito(self):
        '''Returns "tempoTotal" parameter, representing the transit time of the planet on its host star.'''
        return self.tempoTotal
    def getTempoHoras(self):
        '''Returns "tempoHoras" parameter, representing the planet's transit time on its host star in Hours.'''
        return self.tempoHoras
    def getCurvaLuz(self):
        '''Returns "curvaLuz" parameter, representing the light curve of the star that has a planet orbiting it.'''
        return self.curvaLuz
    def getError(self):
        '''
        Returns the error value, whether or not any errors occurred. If there is no error, it is assigned 0. If any errors occu, 
        the variable will have its starting value (which is -1)
        '''
        return self.error
    
    

