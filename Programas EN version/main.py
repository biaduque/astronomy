__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"



import numpy as np
from matplotlib import pyplot
from star_nv1 import estrela
from eclipse_nv1 import Eclipse
from verify import Validar,calSemiEixo,calculaLat


############ CREATION OF THE STAR #############


'''
In the main, the star and eclipse functions are called.
First the star is created, while the user adds the parameters he wants
such as stains, flares, faculas, etc.
After completing this step, the user must add parameters of the planet
in relation to the star so that its characteristic light curve is plotted.

imports
verify: function created to validate entries, for example non-float / int or negative numbers
star: Star class that has stains, faculas and flares as objects
eclipse: eclipse class that receives a star and calculates its light curve
'''

print('''\033[1;36m
╔═════════════»»»   Example Star  «««════════════╗
║-PIXEL RADIUS: 373                              ║      
║-INTENSIDADE DO CENTRO DA ESTRELA: 240          ║
║  LIMBO DARKING COEFFICIENT                     ║
║-u1: 0.5                                        ║
║-u2:0.3                                         ║
╚════════════════════════════════════════════════╝\033[m\n\n''')
#default
raio = 373.# star radius in pixels
intensidadeMaxima=240.#star center intensity (or maximum intensity)

#star creation step
error=-1 #error = -1 for the program to repeat the step in case an error occurs
#as long as the error is -1, the while will run, that is, the user will have to redo the process if there is an error
while error==-1:
    try:
        x=int(input('Choose an option!\n1. Plot star example |2. Add parameters to the star:'))
        if x==1:
            raioStar=1.
        # limbo dimming coefficients
            coeficienteHum = 0.5
            coeficienteDois = 0.3
        elif x==2:
            raioStar= Validar("Star radius (in relation to the sun's ray):")
            raioStar=raioStar*696340 #multiplying by the solar ray in Km
            coeficienteHum = float(input('Limbo Darking Coefficient (u1):'))
            coeficienteDois = float(input('Limbo Darking Coefficient (u2):'))

        x=int(input('Matrix size set to 856, do you want to change it? 1.Yes 2.No:'))
        if x== 1:
            tamanhoMatriz=int(input('Enter the Matrix size:'))
        elif x==2:
            tamanhoMatriz = 856


        # Construction of the star with limbo darkening
        # Creation of the star object inside a star.
        estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)
        error=estrela_.getError() # if you pass all steps, error = 0 and exit the loop
        estrela=estrela_.getEstrela()
        estrela._Plotar(tamanhoMatriz,estrela)
    except Exception as erro:
         print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m') #retorna o tipo de erro


##################### STARTING ECLIPSE ##########################

#planet, traffic, curve
print('''\033[1;33m
        ╔══════════════════════════»»» EXAMPLE ECLIPSE «««══════════════════════════════╗
        ║- PERIOD: 10 (in days)                                                         ║           
        ║- SEMI AXIS (in relation to the radius of the star): 15                      	║
        ║- INCLINATION ANGLE (in degrees):88                                           	║
        ║- PLANET RADIUS (in relation to the radius of the star):0.1                   	║
        ╚═══════════════════════════════════════════════════════════════════════════════╝\033[m'''
        )
dtor = np.pi/180.  
aux= True
while aux == True: 
    try:
        x=int(input('1.Example Eclipe. 2.Change the parameters:')) #choice of how to pass the eclipse parameters
        aux= False
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')
                
if x==1:
#default entries
    periodo = 10.  # in days
    semiEixoRaioStar = 15   #in Rstar units
    anguloInclinacao = 88.  # in degrees
    raioPlanetaRstar = 0.1   #in Rstar units     
            
elif x==2:
    aux= True
    while aux == True:
        try:
            periodo = Validar("Period (in days):")
            anguloInclinacao = float(input('Inclination Angle (in degrees):')) 
            raioPlanetaRstar = Validar('Planet Radius (in relation to the Júpiter radius:)')
            raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplying by the radius of jupiter in km

            dec=int(input("Do you want to calculate the planet's Orbital semi-axis (a) using the 3rd KEPLER LAW? 1. Yes 2.No |"))
            if dec==1:
                mass= Validar("Enter the mass of the star in relation to the mass of the sun (MassSun):")
                semieixoorbital = calSemiEixo(periodo,mass) #calculating with 3rd Kepler Law
                semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
                #turns to km to do in relation to the radius of the star
            else:
                semiEixoRaioStar = Validar('Semi-axis (in AU:)')
                semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
                #multiplying by AU (transforming into Km) and converting in relation to the radius of the star
            
            while semiEixoRaioStar*np.cos(anguloInclinacao*dtor) >= 1: 
                print('Planet does not eclipse star (change inclination angle)')
                anguloInclinacao = float(input('Inclination Angle:')) 
            
            aux= False
        
        except Exception as erro:
            print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')
                

#STAR SPOT
error=-1
while error==-1:
    try:
        escolha= Validar('\033[1;35mDo you want to add spots on your star? 1. Yes 2. No |\033[m')  #defines the choice, whether there will be stain or not.
        if escolha==1:
            latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
            print("The suggested latitude for the spot to influence the star's light curve is:", latsugerida)
            quantidade= Validar('\033[1;35mEnter the number of spots to add:\033[m')
            quantidade=int(quantidade)
            count=0
            #create quantity size vectors to place the stain parameters
            fa = [0.]*quantidade #spots area vector
            fi = [0.]*quantidade #vector intensity spots
            li = [0.]*quantidade #longitude spota vector
            while count!=quantidade: #the loop will rotate the amount of spots selected by the user
                print('\033[1;35m\n\n══════════════════ Spot Parameters',count+1,'═══════════════════\n\n\033[m')
                r = Validar('Enter the radius of the spot as a function of the radius of the star: ')
                
                intensidadeMancha= Validar('Enter the intensity of the spot as a function of the maximum intensity of the star:')
                fi[count]=intensidadeMancha
                lat=float(input('Spot latitude:'))

                longt=float(input('Spot length:'))
                li[count]=longt

                raioMancha= r*raioStar
                area = np.pi *(raioMancha**2)
                fa[count] = area

                estrela=estrela_.manchas(r,intensidadeMancha,lat,longt) #receives the sspots parameters
                #stores what is stored in the star object to overwrite
                error=estrela_.getError()
                count+=1
            print(fi)
            print(li)
            print(fa)
        else:
            estrela = estrela_.getEstrela()  # stores what is stored in the star object to overwrite
            error=0    
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')

estrela=estrela_.getEstrela()
estrela._Plotar(tamanhoMatriz,estrela)

# Faculas in production
error=-1
while error==-1:
    try:
        escolha= Validar('\033[1;92mDo you want to add Fáculas to your star? 1. Yes 2. No|')
        # var escolha defines the choice, whether facula or not.
        if escolha==1:
            quantidade= Validar('Choice not yet programmed')
            count=0
            while count!=quantidade:
                print('*****Parâmetros da fácula ',count+1,'.*****\033[m')
                estrela = estrela_.faculas(estrela,count) #facula receives the star now updated
                error = estrela_.getError()
                count+=1
        else:
            estrela = estrela_.getEstrela()  # stores what is stored in the star object to overwrite
            error=0    
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')

#STAR FLARES in production
error=-1
while error==-1:
    try:
        #flare parameters 
        escolha = Validar('Do you want to add flares to your star? 1. Yes 2. No |')
        
        #var escolha defines the choice, whether there will be flares or not.
        if escolha==1:
            quantidade= Validar('Change not yet programmed')
            count=0
            while count!=quantidade:
                print('***** Flare Parameters ',count+1,'.*****\033[m')
                estrela = estrela_.getEstrela() #flare receives the star now updated
                error = estrela_.getError()
                count+=1
        else:
            estrela = estrela_.getEstrela() #flare receives the star now updated
            error=0    
    except Exception as erro:
        print(f'The value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')
#CALL OF NECESSARY VARIABLES FOR CALCULATING THE LIGHT CURVE
Nx= estrela_.getNx() #Nx and Ny needed for plotting the eclipse
Ny= estrela_.getNy()
raioEstrelaPixel = estrela_.getRaioStar()
estrelaManchada= estrela_.getEstrela()#actually returns the spotless star to plot at the end
# assignment of variables given by the parameters to be plotted.



error=-1 #handling errors in eclipse
eclipse= Eclipse(Nx,Ny,raioEstrelaPixel,estrelaManchada) 
while error==-1:
    try:
        eclipse.criarEclipse(periodo, semiEixoRaioStar, anguloInclinacao, raioPlanetaRstar)
        error=eclipse.getError()
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please type again. The type of problem encountered was{erro.__class__}\n\n\033[m')

#PRINTED COMMENTS BELOW FOR TESTING ONLY

print ("Total Time (Transit):",eclipse.getTempoTransito()) 
tempoTransito=eclipse.getTempoTransito() #returns transit time

#print("Curva Luz:",eclipse.getCurvaLuz())

curvaLuz=eclipse.getCurvaLuz() #returns light curve (matrix)

#print("Tempo Horas:",eclipse.getTempoHoras())

tempoHoras=eclipse.getTempoHoras() #returns transit time in hours

#Plot of light curve 
pyplot.plot(tempoHoras,curvaLuz)
pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
pyplot.show()
