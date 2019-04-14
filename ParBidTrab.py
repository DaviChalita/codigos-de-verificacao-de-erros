import random
import math
import sys

def decodePacket(transmittedPacket, linha, coluna):

    parityMatrix  = [[0 for x in range(coluna)] for y in range(linha)]
    parityColumns =  [0 for x in range(coluna)]
    parityRows    =  [0 for x in range(linha)]
    decodedPacket =  [0 for x in range(len(transmittedPacket))]

    n = 0

    for i in range(0, len(transmittedPacket), (linha*coluna+linha+coluna)):

        for j in range(linha):
            for k in range(coluna):
                parityMatrix[j][k] = transmittedPacket[i + coluna * j + k]

        for j in range(coluna):
            parityColumns[j] = transmittedPacket[i + (linha*coluna) + j]

        for j in range(linha):
            parityRows[j] = transmittedPacket[i + (linha*coluna+coluna) + j]

        errorInColumn = -1
        somaMatrizColuna = somarColunaMatriz(parityMatrix, linha, j)
        for j in range(coluna):
            if (somaMatrizColuna) % 2 != parityColumns[j]:
                errorInColumn = j
                break

        errorInRow = -1
        for j in range(linha):
            somaMatrizLinha = somarLinhaMatriz(parityMatrix, coluna, j)
            if (somaMatrizLinha) % 2 != parityRows[j]:
                errorInRow = j
                break

        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        for j in range(linha):
            for k in range(coluna):
                decodedPacket[(linha*coluna) * n + coluna * j + k] = parityMatrix[j][k]

        n = n + 1

    return decodedPacket

def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

def insertErrors(codedPacket, errorProb):
    i = -1
    n = 0

    transmittedPacket = list(codedPacket)

    while 1:

        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

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

def countErrors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

def codePacket(originalPacket,linha,coluna):

    parityMatrix = [[0 for x in range(coluna)] for y in range(linha)]
    codedLen = len(originalPacket) / (linha*coluna) * (linha*coluna+linha+coluna);
    codedPacket = [0 for x in range(int(codedLen))]

    for i in range(len(originalPacket) // (linha*coluna)):

        for j in range(linha):
            for k in range(coluna):
                parityMatrix[j][k] = originalPacket[(i * linha*coluna) + (coluna * j) + k]

        for j in range((linha*coluna)):
            codedPacket[i * (linha*coluna+linha+coluna) + j] = originalPacket[i * (linha*coluna) + j]

        for j in range(coluna):
            somaMatrizColuna = somarColunaMatriz(parityMatrix, linha, j)
            if (somaMatrizColuna) % 2 == 0:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 0
            else:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 1

        for j in range(linha):
            somaMatrizLinha = somarLinhaMatriz(parityMatrix, coluna, j)
            if (somaMatrizLinha) % 2 == 0:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna+coluna) + j] = 0
            else:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna+coluna) + j] = 1

    return codedPacket

def contabilizadorErros(bitErrorCount):
    totalBitErrorCount = 0
    totalPacketErrorCount = 0
    if bitErrorCount > 0:
        totalBitErrorCount += bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1
    return totalBitErrorCount, totalPacketErrorCount

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
originalPacket3 = generateRandomPacket(packetLength, 9)
print(originalPacket3)

codedPacket1 = codePacket(originalPacket1, 2, 2)
print(codedPacket1)
codedPacket2 = codePacket(originalPacket2, 2, 3)
print(codedPacket2)
codedPacket3 = codePacket(originalPacket3, 3, 3)
print(codedPacket3)

totalInsertedErrorCount1 = 0
totalInsertedErrorCount2 = 0
totalInsertedErrorCount3 = 0

for i in range(reps):
    insertedErrorCount1, transmittedPacket1 = insertErrors(codedPacket1, errorProb)
    totalInsertedErrorCount1 = totalInsertedErrorCount1 + insertedErrorCount1

    insertedErrorCount2, transmittedPacket2 = insertErrors(codedPacket2, errorProb)
    totalInsertedErrorCount2 = totalInsertedErrorCount2 + insertedErrorCount2

    insertedErrorCount3, transmittedPacket3 = insertErrors(codedPacket3, errorProb)
    totalInsertedErrorCount3 = totalInsertedErrorCount3 + insertedErrorCount3

    decodedPacket1 = decodePacket(transmittedPacket1, 2, 2)
    decodedPacket2 = decodePacket(transmittedPacket2, 2, 3)
    decodedPacket3 = decodePacket(transmittedPacket3, 3, 3)

    bitErrorCount1 = countErrors(originalPacket1, decodedPacket1)
    bitErrorCount2 = countErrors(originalPacket2, decodedPacket2)
    bitErrorCount3 = countErrors(originalPacket3, decodedPacket3)

    totalBitErrorCount1, totalPacketErrorCount1 = contabilizadorErros(bitErrorCount1)
    totalBitErrorCount2, totalPacketErrorCount2 = contabilizadorErros(bitErrorCount2)
    totalBitErrorCount3, totalPacketErrorCount3 = contabilizadorErros(bitErrorCount3)

def printsFinais(codedPacket, linha, coluna, totalInsertedErrorCount, totalBitErrorCount, totalPacketErrorCount):
    print('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
    print('Numero de bits transmitidos: {0:d}'.format(reps * packetLength * (linha*coluna)))
    print('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
    print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(
        float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
    print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
    print('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(
        float(totalBitErrorCount) / float(reps * packetLength * (linha*coluna)) * 100.0))
    print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
    print('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))

print('\nMatriz 1:\n')
printsFinais(codedPacket1, 2, 2, totalInsertedErrorCount1, totalBitErrorCount1, totalPacketErrorCount1)
print('\nMatriz 2:\n')
printsFinais(codedPacket2, 2, 3, totalInsertedErrorCount2, totalBitErrorCount2, totalPacketErrorCount2)
print('\nMatriz 3:\n')
printsFinais(codedPacket3, 3, 3, totalInsertedErrorCount3, totalBitErrorCount3, totalPacketErrorCount3)