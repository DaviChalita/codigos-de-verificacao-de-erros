import random
import math
import sys


##


def generateRandomPacket(tamanho):
    return [random.randint(0, 1) for x in range(tamanho)]


##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##


def geomRand(p):
    uRand = 0
    while (uRand == 0):
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
    n = 0  # Numero de erros inseridos no pacote.

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

        n += 1

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
    while 2 ** qtdBitsParidade <= len(originalPacket) + qtdBitsParidade:
        qtdBitsParidade += 1

    return qtdBitsParidade


def insereEspacosParaBitsParidade(originalPacket):
    # coloca valor 0 nas posicoes aonde ficarao os bits de paridade
    n = numeroBitsParidade(originalPacket)  # conta qts bits de paridade precisa
    cont = nBitsPari = nBitsDado = 0
    pacoteComBitsParidade = list()  # cria lista para facilitar manipulacao
    while cont < n + len(originalPacket):
        if cont == (2 ** nBitsPari - 1):
            pacoteComBitsParidade.insert(cont, 0)
            nBitsPari += 1
        else:
            pacoteComBitsParidade.insert(cont, originalPacket[nBitsDado])
            nBitsDado += 1
        cont += 1

    return pacoteComBitsParidade


# separa o codigo em sublistas, com seu primeiro bit sendo o de paridade
# e o restante dos bits relacionados a ele facilita a implementacao,
# com j sendo a posicao dos bits de dados
# e k sendo a posicao dos bits de paridade
# formula geral da lista: lista[(j*k)-1:((j+1)*k)-1]
def hamming(dados):
    n = numeroBitsParidade(dados)
    lista = insereEspacosParaBitsParidade(dados)
    # lista ja esta com os bits de paridade posiconados, seus valores nao estao corretos
    cont = 0
    # comeco do core do hamming, eh repetido na correcao
    while cont < n:
        k = 2 ** cont  # posicao dos bits de paridade eh potencia de 2
        j = 1  # bits de dados comecam na posicao 1
        total = 0
        # percorre as posicoes dos bits de paridade e separa em sublistas
        while j * k - 1 < len(lista):
            if (j * k - 1 == len(lista) - 1) or ((j + 1) * k - 1 >= len(lista)):
                indiceInferior = j * k - 1
                # lista temporaria com tamanho comecando do indice inferior e
                # terminando no ultimo indice da lista
                listaTemporaria = lista[int(indiceInferior):len(lista)]
            elif (j + 1) * k - 1 < len(lista) - 1:
                indiceInferior = (j * k) - 1
                indiceSuperior = (j + 1) * k - 1
                listaTemporaria = lista[int(indiceInferior):int(indiceSuperior)]
            # soma valores para verificar bit de paridade
            total = total + sum(int(x) for x in listaTemporaria)
            j += 2
            # fim do core do hamming
        # se bit de paridade nao for divisivel por 2 entao posicao recebe 1
        # senao, mantem o 0 atribuido anteriormente
        if total % 2 > 0:
            lista[int(k - 1)] = 1
        cont += 1

    return lista


# mesmo comentario do hamming
def hammingCorrecao(codedPacketComErros):
    n = numeroBitsParidade(codedPacketComErros)
    cont = bitErrado = 0
    lista = list(codedPacketComErros)
    # comeco do core do hamming, ver def hamming para comentarios mais detalhados
    while cont < n:
        k = 2. ** cont
        j = 1
        total = 0
        while j * k - 1 < len(lista):
            if (j * k - 1 == len(lista) - 1) or ((j + 1) * k - 1 >= len(lista)):
                indiceInferior = j * k - 1
                listaTemporaria = lista[int(indiceInferior):len(lista)]
            elif (j + 1) * k - 1 < len(lista) - 1:
                indiceInferior = (j * k) - 1
                indiceSuperior = (j + 1) * k - 1
                listaTemporaria = lista[int(indiceInferior):int(indiceSuperior)]
            total += sum(int(x) for x in listaTemporaria)
            j += 2
            # fim do core do hamming
        if total % 2 > 0:
            bitErrado += k
        cont += 1
    if bitErrado >= 1:
        if lista[int(bitErrado - 1)] in ('0', 0):
            lista[int(bitErrado - 1)] = 1
        else:
            lista[int(bitErrado - 1)] = 0
    # inicializa nova lista
    listaCorrigida = list()
    cont = j = k = 0
    # realoca os bits apos correcao para nova lista
    while cont < len(lista):
        if cont != ((2 ** k) - 1):
            listaTemporaria = lista[int(cont)]
            listaCorrigida.append(listaTemporaria)
            j += 1
        else:
            k += 1
        cont += 1
    return listaCorrigida


def contabilizadorErros(bitErrorCount):
    totalBitErrorCount = 0
    totalPacketErrorCount = 0
    if bitErrorCount > 0:
        totalBitErrorCount += bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1
    return totalBitErrorCount, totalPacketErrorCount


##
# Exibe modo de uso e aborta execucao.
##


def help(selfName):
    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write(
        "\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bits, deve ser de um tamanho compativel com hamming: 1, 4, 11, 26, 57, 120 ou 247).\n")
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


totalBitErrorCount = totalPacketErrorCount = totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

# verifica se tamanho do pacote eh compativel com hamming e verifica as repeticoes
# e a probabilidade de erro
if packetLength not in (1, 4, 11, 26, 57, 120, 247) or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##
originalPacket = generateRandomPacket(packetLength)
print("Pacote original: ")
print(originalPacket)
codedPacket = hamming(originalPacket)
print("Pacote codificado: ")
print(codedPacket)
print("-------------------------------------------------")
totalInsertedErrorCount = 0
##
# Loop de repeticoes da simulacao.
##
for i in range(reps):
    # Cria novo pacote com erros, alem de contar qnt erros foram inseridos
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)

    # Contabiliza quantos erros foram gerados no total
    totalInsertedErrorCount += insertedErrorCount

    # Decodificando pacote
    decodedPacket = hammingCorrecao(transmittedPacket)
    # Verifica quantos erros foram inseridos
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    totalBitErrorCount, totalPacketErrorCount = contabilizadorErros(bitErrorCount)


def printsFinais(codedPacket, totalInsertedErrorCount, totalBitErrorCount, totalPacketErrorCount):
    print('Numero de transmissoes simuladas: {0:d}'.format(reps))
    print('Numero de bits transmitidos: {0:d}'.format(reps * len(codedPacket)))
    print('Numero de bits errados inseridos: {0:d}'.format(totalInsertedErrorCount))
    print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(
        float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
    print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
    print('Taxa de erro de bits (apos decodificacao): {0:.2f}%'.format(
        float(totalBitErrorCount) / float(reps * len(codedPacket)) * 100.0))
    print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
    print('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))


printsFinais(codedPacket, totalInsertedErrorCount, totalBitErrorCount, totalPacketErrorCount)
