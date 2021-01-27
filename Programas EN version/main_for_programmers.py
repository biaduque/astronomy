import numpy as np
from matplotlib import pyplot
from star_nv1 import estrela
from eclipse_nv1 import Eclipse
from verify import Validar,calSemiEixo,calculaLat

'''
main created for professionals and students familiar with the area
--- star ---
raio parameter:: star's radius in pixel
intensidadeMaxima parameter:: plotted star's intensity
tamanhoMatriz parameter:: star's matrix size in pixel
raioStar parameter:: star's radius in relation to sun's radius
coeficienteHum parameter:: limb darkening coefficient (u1)
coeficienteDois parameter:: limb darkening coefficient (u2)
estrela_ object :: it's the object star where it's stored the star's matrix according to the parameters. Estrela class's function calls
are made through this object.
estrela parameter :: variable that receives the star object
--- planet ---
periodo parameter:: planet's orbit period in days
anguloInclinacao parameter:: planet's tilt angle in degrees
semieixoorbital parameter:: planet's orbital semi axis
semiEixoRaioStar parameter:: planet's orbital semi axis conversion in relation to the star's radius
raioPlanetaRstar parameter:: planet's radius conversion in relation to Jupiter's radius, which is in relation to the star's radius
---  spot --- 
latsugerida parameter:: suggested latitude for the spot
fa parameter:: vector with the area of each spot
fi parameter:: vector with the intensity of each spot
li parameter:: vector with the longitude of each spot
quantidade parameter:: variable that stores the amount of spots
r parameter:: spot's radius in relation to the star's radius
intensidadeMancha parameter:: spot's intensity in relation to the star's intensity
lat parameter:: spot's latitude
longt parameter:: spot's longitude
raioMancha parameter:: spot's radius
area parameter:: spot's area
--- eclipse ---
eclipse parameter:: variable that stores the eclipse class's object that generates the light curve. Eclipse class's function calls
are made through this object.
tempoTransito parameter:: planet's transit time
curvaLuz parameter:: light curve's matrix that will be plotted in graph form
tempoHoras parameter:: transit time in hours
'''

raio= 373. #default (pixel)
intensidadeMaxima=240 #default
tamanhoMatriz = 856 #default
raioStar=0.117 #star's radius in relation to the sun's radius
raioStar=raioStar*696340 #multiplying by the sun's radius in km
coeficienteHum=0.65
coeficienteDois=0.28


#creates the star
estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)

Nx= estrela_.getNx() #Nx and Ny are needed for plotting the eclipse
Ny= estrela_.getNy()
dtor = np.pi/180.  

periodo = 6.099 # in days
anguloInclinacao = 89.86  # in degrees

dec=int(input("Do you want to calculate the planet's Orbital semi-axis using KEPLER'S 3RD LAW? 1.Yes 2.No |"))
if dec==1:
    mass=0. #put here the star's mass value in relation to the sun's mass
    semieixoorbital = calSemiEixo(mass,periodo)
    semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
    #converting to km to calculate in relation to the star's radius
else:
    semiEixoRaioStar = Validar('Semi axis (in AU:)')
    # in Rstar units
    semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
    #multiplying by AU (converting to km) and converting in relation to the star's radius


raioPlanetaRstar = 0.0819 #in relation to Jupiter's radius
raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplying by jupiter's radius in km

latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
print("The suggested latitude for the spot to influence the star's light curve is:", latsugerida)

#spots
count = 0
quantidade = 0 #desired amount of spots. If you want to increase it, change this variable's value
#create
#create quantity size vectors to put the spot's parameters
fa = [0.]*quantidade #spot's area vector
fi = [0.]*quantidade #spot's intensity vector
li = [0.]*quantidade #spot's longitude vector

while count!=quantidade: #the loop will run the amount of spots selected by the user
    print("\033[1;35m\n\n══════════════════ Spot ",count+1,"'s parameters ═══════════════════\n\n\033[m")
    r = Validar('Enter the radius of the spot in relation to the radius of the star: ')
                
    intensidadeMancha= float(input('Enter the intensity of the spot in relation to the maximum intensity of the star:'))
    fi[count]=intensidadeMancha
    lat=float(input("Spot's latitude:"))
    longt=float(input("Spot's longitude:"))
    li[count]=longt

    raioMancha= r*raioStar
    area = np.pi *(raioMancha**2)
    fa[count]= area

    estrela=estrela_.manchas(r,intensidadeMancha,lat,longt) #gets the choice if there'll be spots or not
    count+=1

#prints the spot's intensity, longitude and area vectors for testing
print("Intensidades:",fi)
print("Longitudes:",li)
print("Areas:",fa)

estrela = estrela_.getEstrela()
#for plotting the star
#in case you don't want to plot the star, transform the 2 lines below in comments
if (quantidade>0): #if spots are added, plot
    estrela_.Plotar(tamanhoMatriz,estrela)

#creating moons
lua = False #if you don't want any moons, change this variable's value to False
eclipse= Eclipse(Nx,Ny,raio,estrela)
estrela_.Plotar(tamanhoMatriz,estrela)
eclipse.geraTempoHoras()
tempoHoras=eclipse.getTempoHoras()
#instantiating MOON
rmoon = 0.5 #in relation to the Earth's radius
rmoon = rmoon *6371 #multiplying by Earth's radius in km
mass = 0.001 #in relation to the Earth's mass
mass = mass * (5.972*(10**24))
massPlaneta = 0.002 #in relation to the Jupiter's radius
massPlaneta = massPlaneta * (1.898 *(10**27)) #convert to grams because of the G constant
G = (6.674184*(10**(-11)))
perLua = 0.1 #in days
distancia=((((perLua*24.*3600./2./np.pi)**2)*G*(massPlaneta+mass))**(1./3))/raioStar
distancia = distancia/100
moon = eclipse.criarLua(rmoon,mass,raio,raioStar,tempoHoras,anguloInclinacao,periodo,distancia)
estrela = estrela_.getEstrela()



#eclipse
eclipse.criarEclipse(semiEixoRaioStar, raioPlanetaRstar,periodo,anguloInclinacao,lua)


print ("Total Time (Transit):",eclipse.getTempoTransito()) 
tempoTransito=eclipse.getTempoTransito()
curvaLuz=eclipse.getCurvaLuz()
tempoHoras=eclipse.getTempoHoras()

#Light curve's plotting
pyplot.plot(tempoHoras,curvaLuz)
pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
pyplot.show()
