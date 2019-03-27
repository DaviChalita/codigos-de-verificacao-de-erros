import random
import math
import sys

def decodePacket(transmittedPacket, linha, coluna):

    parityMatrix = [[0 for x in range(4)] for y in range(2)]
    parityColumns = [0 for x in range(4)]
    parityRows = [0 for x in range(2)]
    decodedPacket = [0 for x in range(len(transmittedPacket))]

    n = 0

    for i in range(0, len(transmittedPacket), 14):

        for j in range(2):
            for k in range(4):
                parityMatrix[j][k] = transmittedPacket[i + 4 * j + k]

        ##
        # Bits de paridade das colunas.
        ##
        for j in range(4):
            parityColumns[j] = transmittedPacket[i + 8 + j]

        ##
        # Bits de paridade das linhas.
        ##
        for j in range(2):
            parityRows[j] = transmittedPacket[i + 12 + j]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInColumn = -1
        for j in range(4):
            if (parityMatrix[0][j] + parityMatrix[1][j]) % 2 != parityColumns[j]:
                errorInColumn = j
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInRow = -1
        for j in range(2):

            if (parityMatrix[j][0] + parityMatrix[j][1] + parityMatrix[j][2] + parityMatrix[j][3]) % 2 != parityRows[j]:
                errorInRow = j
                break

        ##
        # Se algum erro foi encontrado, corrigir.
        ##
        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##
        for j in range(2):
            for k in range(4):
                decodedPacket[8 * n + 4 * j + k] = parityMatrix[j][k]

        ##
        # Incrementar numero de bytes na saida.
        ##
        n = n + 1

    return decodedPacket

def insertErrors(codedPacket, errorProb):
    i = -1
    n = 0

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


def generateRandomPacket(l,linha):

    return [random.randint(0,1) for x in range(linha * l)]

def somarColunaMatriz(parityMatrix, linha, j):
    somaMatrizColuna = 0
    for i in range(linha):
        somaMatrizColuna += parityMatrix[i][j]

    return somaMatrizColuna

def somarLinhaMatriz(parityMatrix, coluna, i):
    somaMatrizLinha = 0
    for j in range(coluna):
        somaMatrizLinha += parityMatrix[i][j]

    return somaMatrizLinha

def codePacket(originalPacket,linha,coluna):

    parityMatrix = [[0 for x in range(coluna)] for y in range(linha)]
    codedLen = len(originalPacket) / (linha*coluna) * (linha*coluna+linha+coluna);
    codedPacket = [0 for x in range(codedLen)]

    ##
    # Itera por cada byte do pacote original.
    ##
    for i in range(len(originalPacket) / (linha*coluna)):

        ##
        # Bits do i-esimo byte sao dispostos na matriz.
        ##
        for j in range(linha):
            for k in range(coluna):
                parityMatrix[j][k] = originalPacket[(i * linha*coluna) + (coluna * j) + k]

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for j in range((linha*coluna)):
            codedPacket[i * (linha*coluna+linha+coluna) + j] = originalPacket[i * (linha*coluna) + j]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##

        for j in range(coluna):
            somaMatrizColuna = somarColunaMatriz(parityMatrix, linha, j)
            if (somaMatrizColuna) % 2 == 0:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 0
            else:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##

        for j in range(linha):
            somaMatrizLinha = somarLinhaMatriz(parityMatrix, coluna, j)
            if (somaMatrizLinha) % 2 == 0:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna+coluna) + j] = 0
            else:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna+coluna) + j] = 1

    return codedPacket

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

totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(sys.argv[0])

random.seed()

originalPacket1 = generateRandomPacket(packetLength, 4)
print(originalPacket1)
originalPacket2 = generateRandomPacket(packetLength, 6)
print(originalPacket2)
originalPacket3 = generateRandomPacket(packetLength,9 )
print(originalPacket3)
codedPacket1 = codePacket(originalPacket1, 2, 2)
print(codedPacket1)
codedPacket2 = codePacket(originalPacket2, 2, 3)
print(codedPacket2)
codedPacket3 = codePacket(originalPacket3, 3, 3)
print(codedPacket3)


def contadorErros(bitErrorCount):
    if bitErrorCount > 0:
        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1
    return totalBitErrorCount, totalPacketErrorCount


for i in range(reps):
    insertedErrorCount1, transmittedPacket1 = insertErrors(codedPacket1, errorProb)
    totalInsertedErrorCount1 = totalInsertedErrorCount1 + insertedErrorCount1

    insertedErrorCount2, transmittedPacket2 = insertErrors(codedPacket2, errorProb)
    totalInsertedErrorCount2 = totalInsertedErrorCount2 + insertedErrorCount2

    insertedErrorCount3, transmittedPacket3 = insertErrors(codedPacket3, errorProb)
    totalInsertedErrorCount3 = totalInsertedErrorCount3 + insertedErrorCount3

    decodedPacket1 = decodePacket(transmittedPacket, 2, 2)
    decodedPacket2 = decodePacket(transmittedPacket, 2, 3)
    decodedPacket3 = decodePacket(transmittedPacket, 3, 3)

    bitErrorCount1 = countErrors(originalPacket1, decodedPacket1)
    bitErrorCount2 = countErrors(originalPacket2, decodedPacket2)
    bitErrorCount3 = countErrors(originalPacket3, decodedPacket3)

    totalBitErrorCount1, totalPacketErrorCount1 = contadorErros(bitErrorCount1)
    totalBitErrorCount2, totalPacketErrorCount2 = contadorErros(bitErrorCount2)
    totalBitErrorCount3, totalPacketErrorCount3 = contadorErros(bitErrorCount3)
    
#CONTINUAR DAQUI!!!
#da matriz 2x2
print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))

#da matriz 2x3
print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))

#da matriz 3x3
print ('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
print ('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8))
print ('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
print ('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
print ('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
print ('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0))
print ('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
print ('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))