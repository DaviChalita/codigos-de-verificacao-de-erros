import random
import math
import sys

##


def generateRandomPacket(l, tamanho):

    return [random.randint(0, 1) for x in range(tamanho * l)]

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
    transmittedPacket = codedPacket

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


def numeroBitsParidade(originalPacket):
    qtdBitsParidade = 0
    while 2**qtdBitsParidade <= len(originalPacket)+qtdBitsParidade:
        qtdBitsParidade += 1

    return qtdBitsParidade

def insereEspacosParaBitsParidade(originalPacket):
    #coloca valor 0 nas posicoes aonde ficarao os bits de paridade
    n = numeroBitsParidade(originalPacket) #conta qts bits de paridade precisa
    i = 0
    nBitsPari = 0
    nBitsDado = 0
    pacoteComBitsParidade = list() #cria lista para facilitar manipulacao
    while i < n + len(originalPacket):
        if i == (2**nBitsPari - 1):
            pacoteComBitsParidade.insert(i, 0)
            nBitsPari += 1
        else:
            pacoteComBitsParidade.insert(i, originalPacket[nBitsDado])
            nBitsDado += 1
        i += 1

    return pacoteComBitsParidade


def hamming(dados):
    n = numeroBitsParidade(dados)
    lista = insereEspacosParaBitsParidade(dados)
    #lista ja esta com os bits de paridade posiconados, seus valores nao estao corretos
    i = 0
    while i < n:
        k = 2**i #posicao dos bits de paridade eh potencia de 2
        j = 1 #bits de dados comecam na posicao 1
        total = 0
        #percorre as posicoes dos bits de paridade e separa em sublistas
        while j*k - 1 < len(lista):
            if (j*k - 1 == len(lista) - 1) or ((j+1)*k - 1 >= len(lista)):
                indiceInferior = j * k - 1
                temp = lista[int(indiceInferior):len(lista)]
            elif (j+1)*k - 1 < len(lista)-1:
                indiceInferior = (j * k) - 1
                indiceSuperior = (j+1)*k - 1
                temp = lista[int(indiceInferior):int(indiceSuperior)]
            #soma valores para verificar bit de paridade
            total = total + sum(int(e) for e in temp)
            j += 2
        #se bit de paridade nao for divisivel por 2 entao posicao recebe 1
        #senao, mantem o 0 atribuido anteriormente
        if total % 2 > 0:
            lista[int(k-1)] = 1
        i += 1

    return lista

## \/ esse nao funciona corretamente
def hammingCorrecao(codedPacketComErros):
    n = numeroBitsParidade(codedPacketComErros)
    i = 0
    lista = list(codedPacketComErros)
    errorthBit = 0
    while i < n:
        k = 2.**i
        j = 1
        total = 0
        while j*k - 1 < len(lista):
            if j*k - 1 == len(lista)-1:
                lower_index = j*k - 1
                temp = lista[int(lower_index):len(lista)]
            elif(j+1)*k - 1 >= len(lista):
                lower_index = j*k - 1
                temp = lista[int(lower_index):len(lista)]
            elif(j+1)*k - 1 < len(lista)-1:
                lower_index = (j*k)-1
                upper_index = (j+1)*k - 1
                temp = lista[int(lower_index):int(upper_index)]
            total += sum(int(e) for e in temp)
            j += 2
        if total % 2 > 0:
            errorthBit += k
        i += 1
    if errorthBit >= 1:
        if lista[int(errorthBit - 1)] == '0' or lista[int(errorthBit-1)] == 0:
            lista[int(errorthBit-1)] = 1
        else:
            lista[int(errorthBit-1)] = 0
    lista2 = list()
    i = 0
    j = 0
    k = 0
    while i < len(lista):
        if i != (2**k)-1:
            temp = lista[int(i)]
            lista2.append(temp)
            j += 1
        else:
            k += 1
        i += 1
    return lista2

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
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

#originalPacket1 = generateRandomPacket(packetLength, 1)
originalPacket2 = generateRandomPacket(packetLength, 4)
#originalPacket3 = generateRandomPacket(packetLength, 11)
print(originalPacket2)
#ok
#codedPacket1 = hamming(originalPacket1)
codedPacket2 = hamming(originalPacket2)
#codedPacket3 = hamming(originalPacket3)
print("codificado\n")
print(codedPacket2)
#ok
#totalInsertedErrorCount1 = 0
totalInsertedErrorCount2 = 0
#totalInsertedErrorCount3 = 0

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
   # insertedErrorCount1, transmittedPacket1 = insertErrors(codedPacket1, errorProb)
   # totalInsertedErrorCount1 = totalInsertedErrorCount1 + insertedErrorCount1

    insertedErrorCount2, transmittedPacket2 = insertErrors(codedPacket2, errorProb)
    totalInsertedErrorCount2 = totalInsertedErrorCount2 + insertedErrorCount2

   # insertedErrorCount3, transmittedPacket3 = insertErrors(codedPacket3, errorProb)
   # totalInsertedErrorCount3 = totalInsertedErrorCount3 + insertedErrorCount3
    print(transmittedPacket2)
#ok
    ##
    # Gerar versao decodificada do pacote.
    ##
    #decodedPacket1 = hammingCorrecao(transmittedPacket1)
    decodedPacket2 = hammingCorrecao(transmittedPacket2)
   # decodedPacket3 = hammingCorrecao(transmittedPacket3)
    print(decodedPacket2)
  #  bitErrorCount1 = countErrors(originalPacket1, decodedPacket1)
  #  bitErrorCount2 = countErrors(originalPacket2, decodedPacket2)
  #  bitErrorCount3 = countErrors(originalPacket3, decodedPacket3)

 #   totalBitErrorCount1, totalPacketErrorCount1 = contabilizadorErros(bitErrorCount1)
  #  totalBitErrorCount2, totalPacketErrorCount2 = contabilizadorErros(bitErrorCount2)
  #  totalBitErrorCount3, totalPacketErrorCount3 = contabilizadorErros(bitErrorCount3)


def printsFinais(codedPacket, param, totalInsertedErrorCount, totalBitErrorCount, totalPacketErrorCount):
    print('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
    print('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * param))
    print('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
    print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(
        float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
    print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
    print('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(
        float(totalBitErrorCount) / float(reps * packetLength * param) * 100.0))
    print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
    print('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))


#print('\nMatriz 1:\n')
#printsFinais(codedPacket1, 1, totalInsertedErrorCount1, totalBitErrorCount1, totalPacketErrorCount1)
#print('\nMatriz 2:\n')
#printsFinais(codedPacket2, 4, totalInsertedErrorCount2, totalBitErrorCount2, totalPacketErrorCount2)
#print('\nMatriz 3:\n')
#printsFinais(codedPacket3, 11, totalInsertedErrorCount3, totalBitErrorCount3, totalPacketErrorCount3)