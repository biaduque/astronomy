__author__ = "Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"


import numpy as np
from matplotlib import pyplot
from eclipse_nv1 import Eclipse
from star_nv1 import estrela
from verify import Validar,calSemiEixo,calculaLat

'''
main programmed for professionals and students familiar with the area
--- star ---
radius parameter :: radius of the planet in days
parameter MaximumMaximity :: intensity of the star to be plotted
parameter matrix size :: size in pixels of the star matrix
parameter rayStar :: ray of the star in relation to the ray of the sun
parameter coefficientHum :: dimming coefficient of limbus 1 (u1)
parameter coefficientTwo :: limbo dimming coefficient 2 (u2)
star_ object :: is the star object where the star matrix is ​​stored according to the parameters. Class function calls
star are made through it.
star parameter :: variable that receives the star object

--- planet ---
parameter period :: planet's orbit period in days
parameter anguloInclinacao :: angle of inclination of the planet in degrees
semieixoorbital parameter :: planet's orbital semi-axis
parameter semiEixoRaioStar :: conversion of the orbital semi-axis in relation to the star radius
parameter radarPlanetaRstar :: conversion of the radius of the planet in relation to the radius of Jupiter to in relation to the radius of the star


---  spot ---
latsugerida parameter :: suggested latitude for the spot
parameter fa :: vector with the area of ​​each spot
fi parameter :: vector with the intensity of each spot
parameter li :: vector with the length of each spot
parameter quantity :: variable that stores the amount of stains
parameter r :: radius of the spot in relation to the radius of the star
parameter intensityMancha :: intensity of the stain in relation to the intensity of the star
lat :: spot latitude parameter
longt parameter :: spot length
parameter rayMancha :: real radius of the spot
parameter area :: spot area

--- eclipse ---
eclipse parameter :: variable that holds the object of the eclipse class that generates the light curve. Class function calls
Eclipse () are done through it.
parameter tempoTransito :: transit time of the planet
light curve parameter :: light curve matrix that will be plotted as a graph
parameter tempoHora :: transit time in matrix hours
'''

raio= 373. #default (pixel)
intensidadeMaxima=240 #default
tamanhoMatriz = 856 #default
raioStar=1.05 #radius of the star in relation to the ray of the sun
raioStar=raioStar*696340 #multiplying by the solar ray in Km
coeficienteHum=0.405
coeficienteDois=0.262


#star
estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)

Nx= estrela_.getNx() #Nx and Ny needed for plotting the eclipse
Ny= estrela_.getNy()
raioEstrelaPixel = estrela_.getRaioStar()
estrela= estrela_.getEstrela() #returns the star objects

dtor = np.pi/180.  
periodo =  1.4857108  #in days
anguloInclinacao =  87.2  #degree

dec=int(input(" Do you want to calculate the planet's Orbital semi-axis using the 3rd KEPLER LAW? 1. Yes 2.No|"))
if dec==1:
    mass=0. #put the star's mass in relation to the sun's mass
    semieixoorbital = calSemiEixo(mass,periodo)
    semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
    #transform in km to do in relation to the radius of the star
else:
    semiEixoRaioStar = Validar('Semi-axis (in AU:)')
    semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
    #multiplying by AU (transforming into Km) and converting in relation to the radius of the star

raioPlanetaRstar = 1.312 #in relation to the jupiter radius
raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplying by the radius of Jupiter in km

#suggested latitude for the spot
latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
print("The suggested latitude for the spot to influence the star's light curve is:", latsugerida)

count=0
quantidade=1 #amount of stains desired
#create quantity-size vectors to place the stain parameters
fa = [0.]*quantidade #array area spots
fi = [0.]*quantidade #array intensity spots
li = [0.]*quantidade #array longitude patches



while count!=quantidade: #the loop will rotate the amount of stains selected by the user
    print('\033[1;35m\n\n══════════════════ Spots Parameters ',count+1,'═══════════════════\n\n\033[m')
    r = Validar('Enter the radius of the spot as a function of the radius of the star in pixels:')
                
    intensidadeMancha= float(input('Enter the intensity of the spot as a function of the maximum intensity of the star:'))
    fi[count]=intensidadeMancha
    lat=float(input('Spot latitude:'))
    longt=float(input('Spot longitude:'))
    li[count]=longt

    raioMancha= r*raioStar
    area = np.pi *(raioMancha**2)
    fa[count]= area

    estrela=estrela_.manchas(r,intensidadeMancha,lat,longt) #updates the star object
    count+=1

#array print of intensity, longitude and area of the spot for testing
print(fi)
print(li)
print(fa)


#to plot the star
#you don't want to plot the star, comment lines below
estrela = estrela_.getEstrela()
estrela_.Plotar(tamanhoMatriz,estrela)


#eclipse

eclipse= Eclipse(Nx,Ny,raioEstrelaPixel,estrela) 
eclipse.criarEclipse(periodo, semiEixoRaioStar, anguloInclinacao, raioPlanetaRstar)


print ("Total Time (Transit):",eclipse.getTempoTransito()) 
tempoTransito=eclipse.getTempoTransito()
curvaLuz=eclipse.getCurvaLuz()
tempoHoras=eclipse.getTempoHoras()

#Plot of light curve
pyplot.plot(tempoHoras,curvaLuz)
pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
pyplot.show()



           