__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"

'''
This program simulates the plotting of a star with spots, using parameters such as radius, intensity, limb darkening, etc.
'''


import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from verify import Validar



class estrela:
    '''
    The star class receives as its object the radius, maximum intensity, limb darkening coefficients.
    The star is formed in a matrix of defeault size 856.
    Objects belonging to the class are the parameters passed to the spot, such as: radius, intensity, longitude and latitude
    in relation to the star.
    ************ STAR PARAMETERS ***************
    : raio parameter: The radius of the star
    : intensidadeMaxima parameter: Intensity of the center of the star
    : coeficienteHum parameter: Limbo dimming coefficient
    : coeficienteDois parameter: Limbo dimming coefficient
    : amanhoMatriz parameter: Size of the matrix in which the star will be built
    : estrela parameter: Star built with limbo dimming coefficients
    '''
   

    def __init__(self,raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz):
        
        self.raio=raio
        self.intensidadeMaxima=intensidadeMaxima
        self.coeficienteHum=coeficienteHum
        self.coeficienteDois=coeficienteDois
        self.tamanhoMatriz=tamanhoMatriz
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
        self.color = "hot"
    
    #insert spots



    def manchas(self,r,intensidadeMancha,lat,longt):
        '''
        Function where the star spot (s) is created. All parameters
        are related to the size of the star, with the user being able to enter values
        or select the default option.
        ********* START OF SPOT PARAMETERS *******
        : raioMancha parameter: Radius of the spot in relation to the radius of the star
        : intensicadeMancha parameter: Stain intensity as a function of maximum star intensity
        : latitudeMancha : Spot's latitude coordinate in relation to the star
        : latitudeMancha parameter: Spot's latitude coordinate in relation to the star
        : longitudeMancha parameter: Spot's longitude coordinate in relation to the star
        
        '''
        #Spots parameters for testing
        #r = 0.05 (test)
        #intensidadeMancha = 0.5 (test) spot's intensity 
        # spot coordinates in degrees
        #test latitude = -30
        #test longitude = 20

        self.raioMancha = self.raio * r # in relation to the star's radius in pixels
        self.intensidadeMancha = intensidadeMancha # spot intensity as a function of maximum star intensity

        

        #spot's position coordinates in degrees
        degreeToRadian = np.pi/180. #A read-only variable containing the floating-point value used to convert degrees to radians.
        self.latitudeMancha  = lat * degreeToRadian 
        self.longitudeMancha =  longt * degreeToRadian

        #position of the spot in pixels in relation to the center of the star
        ys=self.raio*np.sin(self.latitudeMancha)  
        xs=self.raio*np.cos(self.latitudeMancha)*np.sin(self.longitudeMancha)
        anguloHelio=np.arccos(np.cos(self.latitudeMancha)*np.cos(self.longitudeMancha))

                
        # projection effect by the spot being at an heliocentricAngle from the center of the star - ellipticity
        yy = ys + self.Ny/2 # pixel position in relation to the matrix origin
        xx = xs + self.Nx/2 # pixel position in relation to the matrix origin

        kk = np.arange(self.Ny * self.Nx)
        vx = kk-self.Nx*np.int64(1.*kk/self.Nx) - xx
        vy = kk/self.Ny - yy

       # spot's rotation angle
        anguloRot=np.abs(np.arctan(ys/xs))    #in radians
        if self.latitudeMancha*self.longitudeMancha > 0: anguloRot=-anguloRot

        ii, = np.where((((vx*np.cos(anguloRot)-vy*np.sin(anguloRot))/np.cos(anguloHelio))**2+(vx*np.sin(anguloRot)+vy*np.cos(anguloRot))**2) < self.raioMancha**2)
        
        spot = np.zeros(self.Ny * self.Nx) + 1
                
        spot[ii]=self.intensidadeMancha
        spot = spot.reshape([self.Ny, self.Nx])
    
        self.estrela= self.estrela * spot
        plt.axis([0,self.Nx,0,self.Ny])
                
        #self.estrelaManchada= estrelaManchada
        error=0
        self.error=error
        return self.estrela #returns the spotted star

    def faculas(self,estrela,count): 
        
         #receive the updated star as a parameter
        '''
        Function where the star's faculas are created. All parameters
        are related to the size of the star, with the user being able to enter values
        or select the default option.
        --- Parameters not yet defined
        ********* START OF FACULA PARAMETERS*******
        :parameter
        :parameter
        :parameter
        :parameter
        
        '''
        error=0
        self.error=error
        #will overwrite the star he is creating, whether it is the star or the spotted star
        self.estrela=estrela
        return self.estrela #returns the spotted star
    
    def flares(self,estrela,count): #receives the updated star as a parameter
        '''
        Function where the star's flares are created. All parameters
        are related to the size of the star, with the user being able to enter values
        or select the default option.
        --- Parameters not yet defined
        ********* START OF FLARES PARAMETERS *******
        :parameter
        :parameter
        :parameter
        :parameter
        
        '''

       
        error=0
        self.error=error
        #will overwrite the star he is creating, whether it is the star or the spotted star.
        self.estrela=estrela
        return self.estrela #returns the spotted star


    def getNx(self):
        '''
        Returns parameter Nx, needed for Eclipse.
        '''
        return self.Nx
    def getNy(self):
        '''
        Returns parameter Ny, needed for Eclipse.
        '''
        return self.Ny

    def getRaioStar(self):
        '''
        Returns the radius of the star, necessary for the Eclipse program, since the radius of the planet is given in
        relation to the star's radius.
        '''
        return self.raio
    def getEstrela(self):
        '''
        Returns the star, plotted without the spots, necessary if the user chooses the plot without spots.
        '''
        return self.estrela
    def getError(self):
        '''
        Returns error value. If there are no errors, the variable's value will become 0. If there are errors, the program will keep
        the source value of the variable (which is -1).
        '''
        return self.error
    def Plotar(self,tamanhoMatriz,estrela):
        Nx = tamanhoMatriz
        Ny = tamanhoMatriz
        plt.axis([0,Nx,0,Ny])
        plt.imshow(estrela,self.color)
        plt.show()