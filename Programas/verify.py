def Validar(msg):
    '''função criada para validar entradas, por exemplo numeros nao float/int ou negativos'''
    valor=0
    while True:
        n=float(input(msg))
        if  n>0:
            valor= n
            return valor
        else:
            print("\033[0;31mErro! Digite uma entrada válida\033[m")

def calSemiEixo(periodo):
    print(
    ''' 
                                 3a LEI DE KEPLER
    \033[1;35m------------------------------------------------------------------------------
    períodos**2= ((4*(pi))**2/G*(massaestrela+massaplaneta))*(semieixoorbital***3)
    G=9,806 65 m/s²,
    Pi=3.14159265359
    -------------------------------------------------------------------------------
    A seguir, digite a massa da estrela em Kg para que a 3a Lei de Kepler seja apli-
    cada e entao, o Semi Eixo orbital seja calculado.
    \033[m''')
    G= (6.674184*(10**-11)) #constante gravitacao universal
    Pi=3.14159265359 
    periodos=periodo*86400 #transformando o periodo que é dado em dias em segundos
    mass= float(input("Digite a massa da estrela em unidades de MassSun:"))
    massestrela = mass * (1.989*(10**30))
    a=(((periodos**2)*(G*massestrela))/(4*(Pi**2)))**1/3
    return a