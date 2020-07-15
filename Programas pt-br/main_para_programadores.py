import numpy as np
from matplotlib import pyplot
from estrela_nv1 import estrela
from eclipse_nv1 import Eclipse
from verify import Validar,calSemiEixo,calculaLat

raio= 373. #default (pixel)
intensidadeMaxima=240 #default
tamanhoMatriz = 856 #default
raioStar=1.05 #raio da estrela em relacao ao raio do sol
raioStar=raioStar*696340 #multiplicando pelo raio solar em Km 
coeficienteHum=0.405
coeficienteDois=0.262


#cria estrela
estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)

Nx= estrela_.getNx() #Nx  e Ny necessarios para a plotagem do eclipse
Ny= estrela_.getNy()
dtor = np.pi/180.  

periodo = 1.4857108  # em dias
anguloInclinacao = 87.2  # em graus

dec=int(input("Deseja calular o semieixo Orbital do planeta através da 3a LEI DE KEPLER? 1. Sim 2.Não |"))
if dec==1:
    mass=0. #colocar massa da estrela em relação a massa do sol
    semieixoorbital = calSemiEixo(mass,periodo)
    semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
    #transforma em km para fazer em relação ao raio da estrela
else:
    semiEixoRaioStar = Validar('Semi eixo (em UA:)')
    # em unidades de Rstar
    semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
    #multiplicando pelas UA (transformando em Km) e convertendo em relacao ao raio da estrela 


raioPlanetaRstar = 1.312 #em relação ao raio de jupiter
raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplicando pelo raio de jupiter em km 

latsugerida = calculaLat(semiEixoRaioStar,anguloInclinacao)
print("A latitude sugerida para que a mancha influencie na curva de luz da estrela é:", latsugerida)

#manchas
count=0
quantidade=1 #quantidade de manchas desejadas
#cria vetores do tamanho de quantidade para colocar os parametros das manchas
fa = [0.]*quantidade #vetor area manchas
fi = [0.]*quantidade #vetor intensidade manchas
li = [0.]*quantidade #vetor longitude manchas

while count!=quantidade: #o laço ira rodar a quantidade de manchas selecionada pelo usuario
    print('\033[1;35m\n\n══════════════════ Parâmetros da mancha ',count+1,'═══════════════════\n\n\033[m')
    r = Validar('Digite o raio da mancha em função do raio da estrela em pixels:')
                
    intensidadeMancha= float(input('Digite a intensidade da mancha em função da intensidade máxima da estrela:'))
    fi[count]=intensidadeMancha
    lat=float(input('Latitude da mancha:'))
    longt=float(input('Longitude da mancha:'))
    li[count]=longt

    raioMancha= r*raioStar
    area = np.pi *(raioMancha**2)
    fa[count]= area

    estrela=estrela_.manchas(r,intensidadeMancha,lat,longt) #recebe a escolha de se irá receber manchas ou não
    count+=1

#print vetor de intensidade, longitude e area da mancha para testes
print(fi)
print(li)
print(fa)


#para plotar a estrela 
#caso nao queira plotar a estrela, comentar linhas abaixo
estrela = estrela_.getEstrela()
estrela_.Plotar(tamanhoMatriz,estrela)

#eclipse

eclipse= Eclipse(Nx,Ny,raio,estrela) 
eclipse.criarEclipse(periodo, semiEixoRaioStar, anguloInclinacao, raioPlanetaRstar)


print ("Tempo Total (Trânsito):",eclipse.getTempoTransito()) 
tempoTransito=eclipse.getTempoTransito()
curvaLuz=eclipse.getCurvaLuz()
tempoHoras=eclipse.getTempoHoras()

#Plotagem da curva de luz 
pyplot.plot(tempoHoras,curvaLuz)
pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
pyplot.show()



           