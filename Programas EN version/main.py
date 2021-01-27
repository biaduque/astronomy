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
║-INTENSITY OF THE STAR'S CENTER: 240            ║
║ LIMB DARKENING COEFFICIENT                     ║
║-u1: 0.5                                        ║
║-u2: 0.3                                        ║
╚════════════════════════════════════════════════╝\033[m\n\n''')

#default
#star's radius in pixel
raio = 373.
#intensity of the star's center (or maximum intensity)
intensidadeMaxima=240.
#starting data collection of the star parameters
error=-1
while error==-1:
    try:
        x=int(input('Choose an option!\n1. Plot example star |2. Add parameters to the star:'))
        if x==1:
            raioStar=1.
        #limb darkening coefficients
            coeficienteHum = 0.5
            coeficienteDois = 0.3
        elif x==2:
            raioStar= Validar("Star's radius (in relation to the sun's radius):")
            raioStar=raioStar*696340 #multiplying by the sun's radius in km
            coeficienteHum = float(input('Limb darkening coefficient (u1):'))
            coeficienteDois = float(input('Limb darkening coefficient (u2):'))

        #creating an if for recommended settings
        x=int(input("Matrix's size set to 856. Do you want to change it? 1.Yes 2.No :"))
        if x== 1:
            tamanhoMatriz=int(input("Enter the matrix's size:"))
        elif x==2:
            tamanhoMatriz = 856
        # Construction of the star with limb darkening
        # Creation of the star object inside the star.
        error=0 #if it passes all steps, error=0 and exits the loop
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m') #returns the error's type


error=-1 #error handling
#STAR
while error==-1: #while error is still -1, the while will still run, meaning that the user will have to redo the process if it still have an error
    #if it goes through all inputs without errors, the function will return 0, and thus it will exit the loop and proceed to the next step
    try:
        estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)
        estrela = estrela_.getEstrela()
        estrela_.Plotar(tamanhoMatriz,estrela)
        error=estrela_.getError() #if there is no error, it will receive 0, which will make it exit the loop
    except Exception as erro:
        print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m') #returns the error's type

#CALLING NECESSARY VARIABLES TO CALCULATE THE LIGHT CURVE
Nx= estrela_.getNx() #Nx and Ny are needed for plotting the eclipse
Ny= estrela_.getNy()
raioEstrelaPixel = estrela_.getRaioStar()
estrelaManchada = estrela_.getEstrela() #returns the spotless star for plotting later
#variables assignment given by the parameters so that they can be plotted


#instantiating the ECLIPSE
eclipse= Eclipse(Nx,Ny,raioEstrelaPixel,estrelaManchada) #instantiate the Eclipse

##################### Main that allows the creation of more than one planet, each one with their own moon #####################
def criandoPlanetas(estrela_,planetas,qtd):

    '''
    Function used to the addition of more than one planet that orbits the star. This function
    runs inside a while according to the amount of planets needed by the user
    parameter_ :: star object
    planetas parameter :: amount of planets to be added
    qtd parameter :: initial variable = 0 that gets incremented each loop interaction (used as auxiliary for verifications
                     inside the function)
    '''

    ##################### STARTING THE ECLIPSE ##########################

    #planet,transit,light curve
    print('''\033[1;33m
            ╔══════════════════════════»»» EXAMPLE ECLIPSE «««══════════════════════════════╗
            ║- PERIOD: 10 (in days)                                                         ║           
            ║- SEMI AXIS (in relation to the radius of the star): 15                       	║
            ║- TILT ANGLE (in degrees): 88                                              	║
            ║- PLANET'S RADIUS (in relation to the star's radius): 0.1                     	║
            ╚═══════════════════════════════════════════════════════════════════════════════╝\033[m'''
            )
    dtor = np.pi/180.  
    aux= True
    while aux == True: 
        try:
            x=int(input('1.Example Eclipse. 2.Change the parameters:')) #choice of how to pass the eclipse parameters
            aux= False
        except Exception as erro:
            print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m')
                    
    if x==1:
    #default entries
        periodo = 10.  # in days
        semiEixoRaioStar = 15   # in Rstar units
        anguloInclinacao = 88.  # in degrees
        raioPlanetaRstar = 0.1   # in Rstar units
                
    elif x==2:
        aux= True
        while aux == True:
            try:
                periodo = Validar("Period:")
                anguloInclinacao = float(input('Tilt angle:')) 
                raioPlanetaRstar = Validar("Planet's radius (in relation to Jupiter's radius):")
                raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplying by jupiter's radius in km
                anom = float(input("Enter the Anomaly: (Default = 0)"))
                ecc = float(input("Enter the Eccentricity: (Default = 0)"))

                dec=int(input("Do you want to calculate the planet's Orbital semi-axis using KEPLER'S 3RD LAW? 1.Yes 2.No |"))
                if dec==1:
                    mass= Validar("Enter the mass of the star in relation to the mass of the sun (MassSun):")
                    semieixoorbital = calSemiEixo(periodo,mass)
                    print("Result = ", semieixoorbital)
                    semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
                    #turns in km to calculate in relation to the star's radius
                else:
                    semiEixoRaioStar = Validar('Semi axis (in AU:)')
                    # in Rstar units
                    semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
                    #multiplying by AU (turning into Km) and converting in relation to the star's radius
                
                while semiEixoRaioStar*np.cos(anguloInclinacao*dtor) >= 1: 
                    print('Planet does not eclipse the star. Please, change the tilt angle.')
                    anguloInclinacao = float(input('Tilt angle:')) 
                
                aux= False
            
            except Exception as erro:
                print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m')
                    

    #STAR'S SPOT
    error=-1
    while error==-1:
        try:
            escolha= Validar('\033[1;35mDo you want to add spots on your star? 1. Yes 2. No |\033[m')  #defines if there will be spots on the star
            if escolha==1:
                latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
                print("The suggested latitude for the spot to influence the star's light curve is:", latsugerida)
                quantidade= Validar('\033[1;35mEnter the number of spots to add:\033[m')
                quantidade=int(quantidade)
                count=0
                #create quantity size vectors to put the spot's parameters
                fa = [0.]*quantidade #spot's area vector
                fi = [0.]*quantidade #spot's intensity vector
                li = [0.]*quantidade #spot's longitude vector
                while count!=quantidade: #the loop will run the amount of spots selected by the user
                    print("\033[1;35m\n\n══════════════════ Spot ",count+1,"'s parameters ═══════════════════\n\n\033[m")
                    r = Validar('Enter the radius of the spot in relation to the radius of the star: ')
                    
                    intensidadeMancha= Validar('Enter the intensity of the spot in relation to the maximum intensity of the star:')
                    fi[count]=intensidadeMancha
                    lat=float(input("Spot's latitude:"))

                    longt=float(input("Spot's longitude:"))
                    li[count]=longt

                    raioMancha= r*raioStar
                    area = np.pi *(raioMancha**2)
                    fa[count] = area

                    estrela=estrela_.manchas(r,intensidadeMancha,lat,longt) #gets the choice if there'll be spots or not
                    error=estrela_.getError()
                    count+=1
                print("Intensities:",fi)
                print("Longitudes:",li)
                print("Areas:",fa)
                estrela = estrela_.getEstrela()
                eclipse.setEstrela(estrela) #Passing the star to the eclipse
            else:
                estrela = estrela_.getEstrela()  # stores what is saved in the star object to overwrite
                error=0    
        except Exception as erro:
            print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m')


    estrela_.Plotar(tamanhoMatriz,estrela)
    eclipse.geraTempoHoras()
    tempoHoras=eclipse.getTempoHoras() #generates the Eclipse's time (in hours)

    ##################### STARTING THE MOON ##########################

    error=-1 #error handling
    lua = False
    while error==-1:
        try:
            escolha= Validar('\033[1;35mDo you want to add moons to this Planet? 1. Yes 2. No |\033[m')  #defines if there will be moons around this planet
            if escolha==1:
                lua = True
                quantidade= Validar('\033[1;35mEnter the number of MOONS to add:\033[m')
                quantidade=int(quantidade)
                count=0
                while count!=quantidade: #the loop will run the amount of moons selected by the user
                    print("\033[1;35m\n\n══════════════════ MOON ",count+1,"'s parameters ═══════════════════\n\n\033[m")
                    # radius, mass,distance, raioPlanetaPixel, raioStar,tempoHoras
                    rmoon = Validar('Enter the radius of the moon in relation to the radius of the Earth: ')
                    rmoon = rmoon *6371 #multiplying by Earth's radius in km
                    mass = Validar("Enter the moon's mass (in Earth's mass units): ")  
                    mass = mass * (5.972*(10**24))
                    massPlaneta = Validar("Enter the Planet's mass (in Jupiter's mass units): ") #must be converted to kg
                    massPlaneta = massPlaneta * (1.898 *(10**27)) #turn into grams because of the gravitational constant
                    G = (6.674184*(10**(-11)))
                    perLua = Validar("Enter the moon's orbit period:") #in days
                    distancia=((((perLua*24.*3600./2./np.pi)**2)*G*(massPlaneta+mass))**(1./3))/raioStar
                    distancia = distancia/100

                    #x1000**(1/3)/10ˆ5 for the conversion because of the G parameter
                    print("Distance = ",distancia)
                    print("rmoon = ",rmoon/raioStar)
                    raioPlanetaPixel = (raioPlanetaRstar)*(raioEstrelaPixel)
                    #instantiating moon
                    moon = eclipse.criarLua(rmoon,mass,raioPlanetaPixel,raioStar,tempoHoras,anguloInclinacao,periodo,distancia)
                    estrela = estrela_.getEstrela()
                    count+=1
                break      
            else:
                estrela = estrela_.getEstrela()
                error=0    
        except Exception as erro:
            print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m')

    error = -1
    #starts the calculation of the eclipse with planets, moons, spots and whatever the user added
    while error==-1:
        try:
            eclipse.criarEclipse(semiEixoRaioStar, raioPlanetaRstar,periodo,anguloInclinacao,lua,ecc,anom)
            error=eclipse.getError()
        except Exception as erro:
            print(f'\033[0;31mThe value entered is invalid. Please enter the value again. The type of problem encountered was{erro.__class__}\n\n\033[m')

    #Do you want to print the light curve now? add option
    decisao = Validar("Do you want to print the light curve now? 1.YES | 2.NO: ")
    if (decisao==2 and qtd!=planetas-1):
        print("\033[1;33mThe next planet can be added :) \033[m")
    else:
        print ("Total Time (Transit):",eclipse.getTempoTransito()) 
        tempoTransito=eclipse.getTempoTransito()
        #print("Light Curve:",eclipse.getCurvaLuz())
        curvaLuz=eclipse.getCurvaLuz()
        #Plotting of the light curve alone
        pyplot.plot(tempoHoras,curvaLuz)
        pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
        pyplot.show()

#############################################################################################################
#create graph's object
#pass this object to the main
planetas = Validar("Enter the amount of desired planets: ")
qtd = 0
while (qtd!= planetas):
    criandoPlanetas(estrela_,planetas,qtd)
    qtd+=1 
#plots the orbit of the added planets
