import random
import math
import sys

def generateRandomPacket(l,linha):

    return [random.randint(0,1) for x in range(linha * l)]

def codePacket(originalPacket,linha,coluna):
    somaMatrizes = 0
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
                parityMatrix[j][k] = originalPacket[i * (linha*coluna) + (coluna * j) + k]

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
            if (parityMatrix[0][j] + parityMatrix[1][j]) % 2 == 0:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 0
            else:
                codedPacket[i * (linha*coluna+linha+coluna) + (linha*coluna) + j] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
        ##CONTINUAR DAQUI
        for j in range(linha):
            for k in range(coluna):
                somaMatrizes += parityMatrix[j][k]
        for j in range(linha):
            if (somaMatrizes % 2 == 0):
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

originalPacket1 = generateRandomPacket(packetLength,4)
print(originalPacket1)
originalPacket2 = generateRandomPacket(packetLength,6)
print(originalPacket2)
originalPacket3 = generateRandomPacket(packetLength,9)
print(originalPacket3)
codedPacket1 = codePacket(originalPacket1,2,2)
print(codedPacket1)
codedPacket2 = codePacket(originalPacket2,2,3)
print(codedPacket2)
codedPacket3 = codePacket(originalPacket3,3,3)
print(codedPacket3)