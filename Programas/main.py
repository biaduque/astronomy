__author__ = "Adriana Valio, Beatriz Duque"
__copyright__ = "..."
__credits__ = ["Universidade Presbiteriana Mackenzie, CRAAM"]
__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = "biaduque7@hotmail.com"
__status__ = "Production"



import numpy as np
from matplotlib.pyplot import *
from matplotlib import pyplot
from estrela_nv1 import estrela
from eclipse_nv1 import Eclipse
from verify import Validar,calSemiEixo


############CRIAÇÃO DA ESTRELA#############


'''
No main, as funções estrela e eclipse sao chamadas. 
Primeiramente a estrela é criada, enquanto o usuário adiciona os parâmetros que desejar
como por exemplo, manchas, flares, fáculas, etc.
Após a conclusão dessa etapa, o usuário deve adicionar parâmetros do planeta
em relação a estrela para que assim seja plotada a curva de luz característica deste.

importações 
verify:função criada para validar entradas, por exemplo numeros nao float/int ou negativos
estrela: classe Estrela que possui como objetos manchas, faculas e flares
eclipse: classe eclipse que recebe estrela e calcula sua curva de luz 
'''

print('''\033[1;36m
╔═════════════»»» ESTRELA EXEMPLO «««════════════╗
║-RAIO EM PIXEL: 373                             ║      
║ -INTENSIDADE DO CENTRO DA ESTRELA: 240         ║
║ COEFICIENTE DE ESCURECIMENTO DE LIMBO          ║
║ -UM: 0.5                                       ║
║-DOIS:0.3                                       ║
╚════════════════════════════════════════════════╝\033[m\n\n''')
#default
#raio da estrela em pixels
raio = 373.
#intensidade do centro da estrela (ou intensidade máxima)
intensidadeMaxima=240.
error=-1
while error==-1:
    try:
        x=int(input('1. Plotar a estrela exemplo|2. Adicionar parâmetros a estrela:'))
        if x==1:
            raioStar=1.
        #parametros dos coeficientes de escurecimento de limbo
            coeficienteHum = 0.5
            coeficienteDois = 0.3
        elif x==2:
            raioStar= Validar('Raio da estrela (em relação ao raio do sol):')
            raioStar=raioStar*696340 #multiplicando pelo raio solar em Km 
            coeficienteHum = float(input('Coeficiente de escurecimento de limbo 1:'))
            coeficienteDois = float(input('Coeficiente de escurecimento de limbo 2:'))

        #fazer um if de config recomendada
        x=int(input('Tamanho da matriz definido como 856, deseja alterar? 1.Sim 2.Não :'))
        if x== 1:
            tamanhoMatriz=int(input('Digite o tamanho da Matriz:'))
        elif x==2:
            tamanhoMatriz = 856
        # Construcao da estrela com escurecimento de limbo 
        #Criação do objeto estrlea dentro de estrela.
        error=0 #se passar de todas as etapas, erro=0 e sai do laço
    except Exception as erro:
         print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m') #retorna o tipo de erro




error=-1 #trata o erro

#ESTRELA
while error==-1: #enquanto o erro for -1, o while irá rodar, ou seja, o usuario terá que refazer o processo se estiver apresentando algum erro
    #se passar por todos os inputs sem erro, a função retornará 0, e assim, sairá do laço e passará para a próxima etapa
    try:
        estrela_ = estrela(raio,intensidadeMaxima,coeficienteHum,coeficienteDois,tamanhoMatriz)
        error=estrela_.getError() #se não houver nenhum erro, ele receberá 0, o que o fará sair do laço.
    except Exception as erro:
        print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m') #retorna o tipo de erro

#MANCHA DA ESTRELA
error=-1
while error==-1:
    try:
        escolha= Validar('\033[1;35mDeseja adicionar manchas em sua estrela? 1. Sim 2. Não |\033[m')  #x define a escolha, se haverá mancha ou não.
        if escolha==1:
            quantidade= Validar('\033[1;35mDigite a quantidade de manchas a serem adicionadas:\033[m')
            count=0
            while count!=quantidade: #o laço ira rodar a quantidade de manchas selecionada pelo usuario
                print('\033[1;35m\n\n══════════════════ Parâmetros da mancha ',count+1,'═══════════════════\n\n\033[m')
                r = Validar('Digite o raio da mancha em função do raio da estrela em pixels:')
                intensidadeMancha= float(input('Digite a intensidade da mancha em função da intensidade máxima da estrela:'))
                estrela=estrela_.manchas(r,intensidadeMancha,count) #recebe a escolha de se irá receber manchas ou não
                error=estrela_.getError()
                count+=1
        else:
            estrela = estrela_.getEstrela()  # armazena o que esta guardado no objeto estrela para sobrescrever
            error=0    
    except Exception as erro:
        print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')

#FACULA DA ESTRELA
error=-1
while error==-1:
    try:
        escolha= Validar('\033[1;92mDeseja adicionar fáculas em sua estrela? 1. Sim 2. Não |')
        #var facula define a escolha, se haverá facula ou não.
        if escolha==1:
            quantidade= Validar('Digite a quantidade de fáculas a serem adicionadas:')
            count=0
            while count!=quantidade:
                print('*****Parâmetros da fácula ',count+1,'.*****\033[m')
                estrela = estrela_.faculas(estrela,count) #facula recebe a estrela agora atualizada
                error = estrela_.getError()
                count+=1
        else:
            estrela = estrela_.getEstrela()  # armazena o que esta guardado no objeto estrela para sobrescrever  
            error=0    
    except Exception as erro:
        print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')

#FLARES DA ESTRELA
error=-1
while error==-1:
    try:
        #parâmetros dos flares 
        escolha = Validar('Deseja adicionar flares em sua estrela? 1. Sim 2. Não |')
        
        #var facula define a escolha, se haverá flares ou não.
        if escolha==1:
            quantidade= Validar('Digite a quantidade de flares a serem adicionadas:')
            count=0
            while count!=quantidade:
                print('*****Parâmetros do flare ',count+1,'.*****\033[m')
                estrela = estrela_.getEstrela() #flare recebe a estrela agora atualizada
                error = estrela_.getError()
                count+=1
        else:
            estrela = estrela_.getEstrela() #flare recebe a estrela agora atualizada
            error=0    
    except Exception as erro:
        print(f'O valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')

#CHAMDA DE VARIÁVEIS NECESSÁRIAS PARA O CÁLCULO DA CURVA DE LUZ 
Nx= estrela_.getNx() #Nx  e Ny necessarios para a plotagem do eclipse
Ny= estrela_.getNy()
raioEstrelaPixel = estrela_.getRaioStar()
estrelaManchada= estrela_.getEstrela()#retorna na verdade a estrela sem manchas para plotar no final
#atribuição de variáveis dadas pelos parâmetros para que sejam plotadas.


##################### INICIANDO O ECLIPSE ##########################

#planeta,transito,curvaLuz 
print('''\033[1;33m
        ╔══════════════════════════»»» ECLIPSE EXEMPLO «««══════════════════════════════╗
        ║- PERÍODO: 10 (em dias)                                                        ║           
        ║- SEMI EIXO (em relação ao raio da estrela): 15                               	║
        ║- ÂNGULO DE INCLINAÇÃO (em graus):88                                       	║
        ║- RAIO DO PLANETA (em relação ao raio da estrela):0.1                         	║
        ╚═══════════════════════════════════════════════════════════════════════════════╝\033[m'''
        )
dtor = np.pi/180.  
aux= True
while aux == True: 
    try:
        x=int(input('1.Eclipse Exemplo. 2.Alterar:')) #escolha de como passar os parametros do eclipse
        aux= False
    except Exception as erro:
        print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')
                
if x==1:
#entradas default
    periodo = 10.  # em dias
    semiEixoRaioStar = 15   # em unidades de Rstar
    anguloInclinacao = 88.  # em graus
    raioPlanetaRstar = 0.1   # em unidades de Rstar
           
            
elif x==2:
    dec=0 #decisao se ira calcular o semi eixo ou nao 
    aux= True
    while aux == True:
        try:
            periodo = Validar("Período:")
            dec=int(input("Deseja calular o semieixo Orbital do planeta através da 3a LEI DE KEPLER? 1. Sim 2.Não |"))
            if dec==1:
                semieixoorbital = calSemiEixo(periodo)
                semiEixoRaioStar = ((semieixoorbital/1000)/raioStar)
                #transforma em km para fazer em relação ao raio da estrela
            else:
                semiEixoRaioStar = Validar('Semi eixo (em UA:)')
                # em unidades de Rstar
                semiEixoRaioStar = ((1.469*(10**8))*semiEixoRaioStar)/raioStar
                #multiplicando pelas UA (transformando em Km) e convertendo em relacao ao raio da estrela    
            
            anguloInclinacao = float(input('Angulo de inclinação:')) 

            raioPlanetaRstar = Validar('Raio do planeta (em relação ao raio de Júpiter:)')
            raioPlanetaRstar = (raioPlanetaRstar*69911)/raioStar #multiplicando pelo raio de jupiter em km 
            while semiEixoRaioStar*np.cos(anguloInclinacao*dtor) >= 1: 
                print('Planet does not eclipse star (change inclination angle)')
                anguloInclinacao = float(input('Angulo de inclinação:')) 
            
            aux= False
        
        except Exception as erro:
            print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')
                

error=-1 #tratando os erros em eclipse
eclipse= Eclipse(Nx,Ny,raioEstrelaPixel,estrelaManchada) 
while error==-1:
    try:
        eclipse.criarEclipse(periodo, semiEixoRaioStar, anguloInclinacao, raioPlanetaRstar)
        error=eclipse.getError()
    except Exception as erro:
        print(f'\033[0;31mO valor digitado é inválido. Por favor, digite novamente. O tipo de problema encontrado foi{erro.__class__}\n\n\033[m')

#COMENTARIOS PRINTADOS ABAIXO APENAS PARA TESTE

print ("Tempo Total (Trânsito):",eclipse.getTempoTransito()) 
tempoTransito=eclipse.getTempoTransito()
#print("Curva Luz:",eclipse.getCurvaLuz())
curvaLuz=eclipse.getCurvaLuz()
#print("Tempo Horas:",eclipse.getTempoHoras())
tempoHoras=eclipse.getTempoHoras()

#Plotagem da curva de luz 
pyplot.plot(tempoHoras,curvaLuz)
pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
pyplot.show()
