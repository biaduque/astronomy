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
import math
import matplotlib.pyplot as plt
from matplotlib import pyplot
from star_nv1 import estrela
from verify import Validar, ValidarEscolha
#from keplerAux import keplerfunc  # auxiliary library in case of kepler library malfunction
import matplotlib.animation as animation
import kepler # library to calculate the eccentric orbits (pip install kepler)
import os

class Eclipse:

   
    def __init__(self,Nx,Ny,raioEstrelaPixel,estrelaManchada):
        

        '''
        :Nx and Ny parameters: star's matrix's size 
        :raioEstrelaPixel parameter: star's radius in pixel 
        :estrelaManchada parameter: STAR object is used as estrelaManchada after spots are inserted
        '''
        self.Nx = Nx
        self.Ny = Ny
        self.raioEstrelaPixel = raioEstrelaPixel
        self.estrelaManchada = estrelaManchada
        
        # OUTPUT
        curvaLuz =[ 1.0 for i in range(self.Nx)]
        self.curvaLuz = curvaLuz

    def geraTempoHoras(self):
        '''
        Function called in Main to calculate the transit's time in hours
        '''
        x=ValidarEscolha("Time period=1. Do you want to change it? 1. YES | 2. NO:")
        if x ==1:
            self.intervaloTempo=Validar('Enter the Time period in minutes:')
        elif x==2:
            self.intervaloTempo = 1.   # in minutes


        self.tamanhoMatriz= self.Nx #Nx or Ny
        tempoHoras = (np.arange(self.tamanhoMatriz)-self.tamanhoMatriz/2)*self.intervaloTempo/60.   # in hours
        self.tempoHoras= tempoHoras

    # from the moment when the moon is instanced in main, these objects become class' objects with a self object.
    def criarLua(self, raioM, massM, raioPlanetaPixel, raioStar,tempoHoras,anguloInclinacao,periodo,distancia):
        moon = Moon(raioM, massM, self.raioEstrelaPixel,anguloInclinacao ,periodo, raioPlanetaPixel, self.tempoHoras,distancia)
        moon.moonOrbit(raioStar)
        Rmoon = moon.getRmoon()

        #data collect, which is necessary to plot the eclipse
        self.xxm = moon.getxm()
        self.yym = moon.getym()
        self.Rmoon = Rmoon #in pixel 
        self.massM = massM
        self.tamanhoMatriz= self.Nx
        #collecting moon's data
        self.ppMoon = moon.getppMoon(self.tamanhoMatriz)
        self.xl = moon.getxl()
        self.yl = moon.getyl()
        return moon
        


    def criarEclipse(self,semiEixoRaioStar, raioPlanetaRstar,periodo,anguloInclinacao,lua,ecc,anom):

        '''
        Creation of eclipse class, which will return the transit's light curve of the planet surrounding the star


        **** parameters assigned to the planet ****
        :periodo parameter: planet's rotation period
        :SemiEixoRaioStar parameter: planet's semi axis in relation to star's radius
        :anguloInclinacao parameter: planet's tilt angle
        :raioPlanetaRstar parameter: planet's radius in relation to star's radius
        :lua parameter: moon that orbits the planet (True or False)
        :ecc parameter: eccentricity of the planet's orbit
        :anom parameter: anomaly of the planet's orbit
        '''


        intervaloTempo = self.intervaloTempo
        tamanhoMatriz = self.tamanhoMatriz
        self.semiEixoRaioStar = semiEixoRaioStar
        self.raioPlanetaRstar = raioPlanetaRstar
        self.periodo = periodo
        self.anguloInclinacao = anguloInclinacao

        dtor = np.pi/180.
        semiEixoPixel = self.semiEixoRaioStar * self.raioEstrelaPixel

        '''Starting the calculation of the ENTIRE transit time using parameters assigned to the planet.'''

        #ecc = 0. #default
        #anom = 0.  #default

        #calculating the obliquity

        '''
        Orbit parameters
        :xplaneta parameter: x in the matrix that projects the planet
        :yplaneta parameter: y in the matrix that projects the planet
        '''

        nk=2*np.pi/(self.periodo*24)    # in hours^(-1)
        Tp=self.periodo*anom/360.*24. # pericenter's time (in hours)
        m = nk*(self.tempoHoras-Tp)     # in radians
        
        # calculating the eccentric anomaly in radians
        eccanom = kepler.solve(m,ecc)  # attached subroutine
        xs=semiEixoPixel*(np.cos(eccanom)-ecc)
        ys=semiEixoPixel*(math.sqrt(1-(ecc**2))*np.sin(eccanom))

        ang=anom*dtor-(np.pi/2)
        xp=xs*np.cos(ang)-ys*np.sin(ang)
        yp=xs*np.sin(ang)+ys*np.cos(ang)

        ie, = np.where(self.tempoHoras == min(abs(self.tempoHoras)))

        xplaneta=xp-xp[ie[0]]
        yplaneta=yp*np.cos(self.anguloInclinacao*dtor)
        
        pp, = np.where((abs(xplaneta) < 1.2 * tamanhoMatriz/2) & (abs(yplaneta) < tamanhoMatriz/2)) #rearranges the vector with only the necessary points to analyze the light curve
        xplan = xplaneta[pp] + tamanhoMatriz/2
        yplan = yplaneta[pp] + tamanhoMatriz/2

        raioPlanetaPixel = self.raioPlanetaRstar * self.raioEstrelaPixel

       

        '''
        Start of the calculation of the time (in hours) and light curve in the matrix
        :nn parameter: number of points in the light curve
        :tamanhoMatriz parameter: gets the spotted star to then plot the planet
        :tempoHoras parameter: calculates the transit time in hours, transforming it in an object of the Eclipse class
        :curvaLuz parameter: calculates the light curve of the planet's transit when eclipsing the star, and also becomes
        an object of the Eclipse 
        '''
        latitudeTransito = -np.arcsin(self.semiEixoRaioStar*np.cos(self.anguloInclinacao*dtor))/dtor # south latitude (arbitrary)
        # transit duration in hours
        duracaoTransito=2 * (90.-np.arccos((np.cos(latitudeTransito*dtor))/self.semiEixoRaioStar)/dtor)*self.periodo/360*24. 
        tempoTotal = 3 * duracaoTransito
        self.tempoTotal= tempoTotal

        
        # calculation of the number of points in the light curve
        nn=np.fix(tempoTotal*60./intervaloTempo)

        #selects the largest orbit so that the light curve gets plotted correctly (full observation of the light curve)
        if(lua == True):
            if (len(pp)>len(self.ppMoon)):
                rangeloop = pp
            else: 
                rangeloop = self.ppMoon
                xplan = xplaneta[self.ppMoon] + tamanhoMatriz/2 #xplan and yplan change in case there is the addition of moons 
                yplan = yplaneta[self.ppMoon] + tamanhoMatriz/2
        else:
            rangeloop = pp


        ''''
        Light curve and normalization of intensity
        '''
        # maximum of the light curve, used in normalizing the intensity
        maxCurvaLuz = np.sum(self.estrelaManchada)

        '''
        Creating the matrix for the plotting:
        '''
        #creating variables to plot the animation
        fig, (ax1, ax2) = plt.subplots(2,1)
        ims = [] 
        j = 0 #auxiliary variable used to plot the animation
        plota = True #FLAG variable that indicates when to store the image of the PLOT


        print("\nPlease wait while the transit's animation is being generated.\n")
        #Start of the loops for plotting and calculation of the transit
        if (lua == False):
            for i in range(0,len(rangeloop)):

                            plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. ##n-by-n matrix
                            x0 = xplan[i] 
                            y0 = yplan[i]
                                
                            kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                            ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                        
                            plan[ii]=0.
                            plan = plan.reshape(self.tamanhoMatriz, self.tamanhoMatriz) #position added to the matrix
                            self.curvaLuz[rangeloop[i]]=np.sum(self.estrelaManchada*plan,dtype=float)/maxCurvaLuz
                            
                            if(plota and self.curvaLuz[rangeloop[i]] != 1 and j<200):
                                plt.axis([0,self.Nx,0,self.Ny])
                                im = ax1.imshow(self.estrelaManchada*plan,cmap="hot", animated = True)
                                ims.append([im]) #stores the points of the graph in the animation (as an image)
                                j+=1 
                            plota = not(plota) #auxiliary variable that selects the best gap between images for the plotting
        else:
            for i in range(0,len(rangeloop)):

                            plan = np.zeros(tamanhoMatriz*tamanhoMatriz)+1. ##n-by-n matrix
                            x0 = xplan[i] 
                            y0 = yplan[i]
                                
                            kk=np.arange(tamanhoMatriz*tamanhoMatriz)

                            ii = np.where((kk/tamanhoMatriz-y0)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-x0)**2 <= raioPlanetaPixel**2)
                        
                            plan[ii]=0.

                            ### adding the moons ###
                            xm = x0-self.xxm[i]         
                            ym = y0-self.yym[i]   
                            ll = np.where((kk/tamanhoMatriz-ym)**2+(kk-tamanhoMatriz*np.fix(kk/tamanhoMatriz)-xm)**2 <= self.Rmoon**2)
                            plan[ll]=0.

                            #####      
                            plan = plan.reshape(self.tamanhoMatriz, self.tamanhoMatriz) #position added to the matrix
                            self.curvaLuz[rangeloop[i]]=np.sum(self.estrelaManchada*plan,dtype=float)/maxCurvaLuz

                            if(plota and self.curvaLuz[rangeloop[i]] != 1 and j<200):
                                plt.axis([0,self.Nx,0,self.Ny])
                                im = ax1.imshow(self.estrelaManchada*plan,cmap="hot", animated = True)
                                ims.append([im]) #stores the points of the graph in the animation (as an image)
                                j+=1
                            plota = not(plota) #auxiliary variable that selects the best gap between images for the plotting

        ax2.plot(self.tempoHoras,self.curvaLuz)
        ax2.axis([-self.tempoTotal/2,self.tempoTotal/2,min(self.curvaLuz)-0.001,1.001])
        ani =animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=0.1)
        plt.show()
        #ani.save('animacao_transito.gif',writer="PillowWriter") #saves the generated gif in the file's roots for user use

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
    def setEstrela(self,estrela):
        '''
        With this function, it is possible to hand the updated star to the forming eclipse, in case there is the addition of new spots.
        '''
        self.estrelaManchada = estrela

    
############ adding moons ###########

class Moon:
    '''
    Moon Class, created according to the addition of planets.
    '''
    pos = np.random.choice([-1, 1])

    def __init__(self, raioM, massM, raioEstrelaPixel, anguloInclinacao ,periodoM, raioPlanetaPixel,tempoHoras,distancia):

        '''
        :raioM parameter:: moon's radius in Earth's radius units
        :massM parameter:: moon's mass in Earth's mass units
        :anguloInclinação parameter:: planet's tilt angle in degrees
        :period parameter:: period of the moon's orbit in days
        :raioPlanetaPixel parameter:: planet's radius in pixel
        :tempoHoras parameter:: planet's transit time in hours
        :distancia parameter:: moon-planet distance in km
        '''
        
        tm0 = 0 # moon first transit time
        self.raioM = raioM
        self.massM = massM
        self.raioEstrelaPixel = raioEstrelaPixel
        self.anguloInclinacao = anguloInclinacao #in degrees
        self.periodo = periodoM #in days
        self.tm0 = tm0 #default
        self.raioPlanetaPixel = raioPlanetaPixel
        self.tempoHoras = tempoHoras
        self.distancia = distancia
        
        
    # moon orbit in equatorial plane of planet
    def moonOrbit(self, raioStar):
        '''
        Function that calculates the moon's orbit, only requiring to use the star's radius as raioStar in km
        '''
        self.Rmoon = self.raioM / raioStar #moon's radius in relation to star's radius
        self.RmoonPixel = self.Rmoon * self.raioEstrelaPixel #moon's radius calculated in pixel
        
        self.dmoon = self.distancia * self.raioEstrelaPixel #calculation of the distance in pixel
        
        self.theta_m = 2*np.pi * self.tempoHoras / (self.periodo*24.) - self.tm0
        self.xm = self.dmoon * np.cos(self.theta_m)
        self.ym = self.dmoon * np.sin(self.theta_m) * np.cos(self.anguloInclinacao) 

    def getppMoon(self,tamanhoMatriz):
        #calculating the moon's projected orbit
        dtor = np.pi/180.
        xlua = self.xm + tamanhoMatriz/2
        ylua = self.ym + tamanhoMatriz/2
        if(self.anguloInclinacao > 90.): 
            ylua = -self.dmoon*np.sin(self.theta_m)*np.cos(self.anguloInclinacao*dtor) + tamanhoMatriz/2

        #moon's projected orbit
        ppMoon, = np.where((xlua >= 0) & (xlua < tamanhoMatriz) & (ylua >= 0) & (ylua < tamanhoMatriz)) 
        self.xl = xlua[ppMoon]
        self.yl = ylua[ppMoon]
        return ppMoon   
    
    def getxl(self):
        return self.xl
    def getyl(self):
        return self.yl

    def getRmoon(self):
        return self.RmoonPixel

    def dMoon(self):
        return self.distancia * self.raioPlanetaPixel

    def getxm(self):
        return self.xm

    def getym(self):
        return self.ym