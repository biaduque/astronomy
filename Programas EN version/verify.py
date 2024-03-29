import numpy as np
def Validar(msg):
    '''function created to validate entries, for example non-float / int or negative numbers'''
    valor=0
    while True:
        n=float(input(msg))
        if  n>=0:
            valor= n
            return valor
        else:
            print("\033[0;31mError! Type a valid entry.\033[m")

def ValidarEscolha(msg):
    '''function created to validate choices (1 or 2)'''
    valor=0
    while True:
        n=int(input(msg))
        if  (n==1) or (n==2):
            valor= n
            return valor
        else:
            print("\033[0;31mError! Type a valid entry.\033[m")

def calSemiEixo(periodo,mass):
    '''
    function that calculates the planet's semi-axis according to the period through Kepler's 3rd law
    parameters:
    periodo :: planet's period in days
    G :: universal gravitational constant
    Pi :: pi's value
    periodos :: converted period converted to seconds
    mass :: mass of the star in relation to the mass of the sun
    massestrela :: star's mass conversion
    a :: orbital semiaxis returned
    '''
    print(
    ''' 
                                 KEPLER'S 3rd LAW
    \033[1;35m------------------------------------------------------------------------------
    períodos**2= ((4*(pi))**2/G*(massaestrela+massaplaneta))*(semieixoorbital***3)
    G=9,806 65 m/s²,
    Pi=3.14159265359
    -------------------------------------------------------------------------------
    \033[m''')
    G= (6.674184*(10**(-11))) #universal gravitation constant 
    periodos=periodo*86400 #transforming the period that is given in days into seconds
    massestrela = mass * (1.989*(10**30))
    a=(((periodos**2)*G*massestrela)/(4*(np.pi**2)))**(1/3)
    print("a=",a)
    return a

def calculaLat(semiEixoRaioStar,anguloInclinacao):
    '''Function that calculates latitude so that the spot is influential in the light curve'''
    dtor=np.pi/180
    lat = - np.arcsin(semiEixoRaioStar*np.cos(anguloInclinacao*dtor))/dtor
    return lat