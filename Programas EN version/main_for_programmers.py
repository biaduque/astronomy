import numpy as np
from matplotlib import pyplot
from eclipse_nv1 import Eclipse
from star_nv1 import estrela
from verify import Validar,calSemiEixo,calculaLat

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



           