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
IntensidadeMaxima parameter :: intensity of the star to be plotted
tamanhoMatriz parameter :: size in pixels of the star's matrix
raioStar parameter:: star's radius in relation to the sun's radius
coeficienteHum parameter:: first limb darkening coefficient (u1)
coeficienteDois parameter:: second limb darkening coefficient (u2) (u2)
estrela_ object :: it's the star the star's object where the star matrix is ​​stored according to the parameters. Star class's functions's calls
are made through it.
estrela parameter :: variable that receives the star object

--- planet ---
periodo parameter   :: planet's orbit period in days
anguloInclinacao parameter  :: angle of inclination of the planet in degrees
semieixoorbital parameter :: planet's orbital semi-axis
semiEixoRaioStar parameter  :: conversion of the orbital semi-axis in relation to the star's radius
raioPlanetaRstar parameter :: conversion of the radius of Jupiter divided by the radius of the star


---  spot ---
latsugerida parameter :: suggested latitude for the spot
fa parameter  :: vector with the area of ​​each spot
fi parameter :: vector with the intensity of each spot
li parameter:: vector with the longitude of each spot
quantidade parameter :: variable that stores the amount of spots
r parameter:: radius of the spot in relation to the radius of the star
intensidadeMancha parameter :: spot's intensity in relation to the intensity of the star
lat parameter :: spot's latitude 
longt parameter :: spot's longitude
raioMancha parameter:: real radius of the spot
area parameter :: spot's area

--- eclipse ---
eclipse parameter :: variable that holds the object of the eclipse class that generates the light curve. Eclipse class's function's calls
are done through it.
tempoTransito parameter :: transit time of the planet
curvaLuz parameter :: light curve's matrix that will be plotted as a graph
parameter tempoHora :: transit time in matrix hours
'''

raio= 373. #default (pixel)
intensidadeMaxima=240 #default
tamanhoMatriz = 856 #default
raioStar=1.05 #radius of the star in relation to the radius of the sun
raioStar=raioStar*696340 #multiplying by the solar radius in Km
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

dec=int(input(" Do you want to calculate the planet's Orbital semi-axis using the KEPLER'S 3rd LAW? 1. Yes 2.No|"))
if dec==1:
    mass=0. #put the star's mass in relation to the sun's mass
    semieixoorbital = calSemiEixo(mass,periodo)
    semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
    #transform in km to do in relation to the radius of the star
else:
    semiEixoRaioStar = Validar('Semi-axis (in AU:)')
    semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
    #multiplying by AU (transforming into Km) and converting in relation to the radius of the star

raioPlanetaRstar = 1.312 #in relation to the jupiter's radius
raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplying by the radius of Jupiter in km

#suggested latitude for the spot
latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
print("The suggested latitude for the spot to influence the star's light curve is:", latsugerida)

count=0
quantidade=1 #amount of spots desired
#create quantity-size arrays to place the spot's parameters
fa = [0.]*quantidade #area spots array
fi = [0.]*quantidade #intensity spots array
li = [0.]*quantidade #longitude spots array



while count!=quantidade: #the loop will run the amount of spots selected by the user
    print('\033[1;35m\n\n══════════════════ Spots Parameters ',count+1,'═══════════════════\n\n\033[m')
    r = Validar('Enter the radius of the spot as a function of the radius of the star in pixels:')
                
    intensidadeMancha= float(input('Enter the intensity of the spot as a function of the maximum intensity of the star:'))
    fi[count]=intensidadeMancha
    lat=float(input("Spot's latitude:"))
    longt=float(input("Spot's longitude:"))
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
#if you don't want to plot the star, transform the next two lines in comments
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



           