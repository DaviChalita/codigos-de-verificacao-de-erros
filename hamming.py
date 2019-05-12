import random
import math
import sys

#########
# Implementacao um esquema sem qualquer metodo de codificao.
#
# Cada byte do pacote original eh mapeado para o mesmo byte no pacote
# codificado.
##

##
# Função composta por duas funções, não é muito eficiente
# pois percorre o array duas vezes: Uma para inserir os bits
# de paridade e outra para atribuir o valor correto
##

def insereBitsParidade(arr):
    arr = posicionaBitsParidade(arr)
    arr = atribuiValorBitsParidade(arr)
    return arr

def posicionaBitsParidade(palavra):
    
    arrLen = len(palavra)

    if (arrLen < 247):
        ##
        # Bit inserido identificado pelo número 2,
        # valor é posteriormente corrigido
        ##
        for (expoente = 0; ((2 ** expoente) - 1) <= arrLen - 1; expoente+=1):
            ##
            # Acrescenta uma posição ao array
            ##
            arrLen = arrLen + 1
            for (i = arrLen - 1; i >= 0; i-=1):
                palavra[i + 1] = palavra[i]

                if (i == 2^expoente - 1):

                    ##
                    # Insere bit de paridade
                    ##

                    palavra[i] = 2;
                    break
    else:
        print("Entre com um tamanho de mensagem váido")
    return palavra

def atribuiValorBitsParidade(arr):

    for (expoente = 0; 2^expoente - 1 < len(arr) - 1; expoente+=1):
        bitParidade = 2^expoente - 1

        if (arr[bitParidade] == 2):
            cont = 0

            for (i = bitParidade; i < len(arr); i += arr[bitParidade] + 1):
                for (j = 0; j < arr[bitParidade]; j+=1):

                    ##
                    # Condição garante que bit de paridade não verifique ele mesmo
                    ##

                    if (i+j != bitParidade):
                        cont+= arr[i+j]

            arr[bitParidade] = cont%2

    return arr


######
# JP #
######
# Função para criar um novo pacate a partir da plavra original
def criaNovoPacote(palavraOriginal):

    # Calcula o tamanho da palavra
    tamPalavraOriginal = len(palavraOriginal)

    # https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Hamming#Estrutura
    if (tamPalavraOriginal <= 247):
        # Calcula a quantidade de bits de paridade
        qtdParidade = math.log(tamPalavraOriginal, 2)
        # Calcula o tamanho total da mensagem, com os bits de paridade
        tamNovaPalavra = tamPalavraOriginal + qtdParidade


        # Variável para identificar as potências de 2
        expoente = 0
        # Variável que representa o índice atual da palavra original
        indexPalavraOriginal = 0
        # Nova mensagem
        novaPalavra = []
        # Laço que percorrerá a nova mensagem
        for x in tamNovaPalavra:
            # Caso a posição atual seja de um bit de paridade (potência de 2)
            if ((x+1) == math.pow(2, expoente)):
                # Incrementamos o valor do expoente para achar a próxima
                # Por hora, não adicionaremos valores a esta posição
                expoente+=1
            # Caso a posição atual seja de dados
            else:
                # Coloca o bit da palavra original nesta posição, respeitando sua ordem
                novaPalavra[x] = palavraOriginal[indexPalavraOriginal]
                indexPalavraOriginal+=1

        # Retorna a nova mensagem coms os bits de dados inseridos
        return novaPalavra
    else:
        print("Entre com um tamanho válido de palavra!")
    return None


######
# JP #
######
def defineParidade(palavraOriginal):

    # Calcula o tamanho da palavra
    tamPalavraOriginal = len(palavraOriginal)

    if (tamPalavraOriginal <= 255):


    else:
        print("Entre com um tamanho válido de palavra!")
    return None


##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
def codePacket(originalPacket):



    ##
    # TODO: completar!
    # Argumentos:
    #  - originalPacket: pacote original a ser codificado na forma de uma lista.
    # Cada entrada na lista representa um bit do pacote (inteiro 0 ou 1).
    # Valor de retorno: pacote codificado no mesmo formato.
    ##
    return ...

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket):

    ##
    # TODO: completar!
    # Argumentos:
    #  - transmittedPacket: pacote apos simulacao da transmissao, potencialmente
    # contendo erros. Cada entrada na lista representa um bit do pacote
    # (inteiro 0 ou 1).
    # Valor de retorno: pacote decodificado no mesmo formato.
    ##
    return ...

###
##
# Outras funcoes.
##
###

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(8 * l)]

##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
def insertErrors(codedPacket, errorProb):

    i = -1
    n = 0 # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while 1:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket

##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

##
# Exibe modo de uso e aborta execucao.
##
def help(selfName):

    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

    sys.exit(1)

##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##

##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

originalPacket = generateRandomPacket(packetLength)
codedPacket = codePacket(originalPacket)

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    decodedPacket = decodePacket(transmittedPacket)

    ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:

        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))
