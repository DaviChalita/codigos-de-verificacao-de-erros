![logos](http://www.professores.uff.br/kowada/wp-content/uploads/sites/63/2017/08/UFF-IC-logos.png)
# Estudo dos mecanismos de detecção e correção de erros
Trabalho semestral apresentado para a disciplina Redes de Computadores II para Sistemas de Informação.

**Alunos:** Davi Chalita, José Paulo Gomes, Matheus Baldissara

**Instituição:** Universidade Federal Fluminense

**Curso:** Bacharelado em Sistemas de Informação

**Disciplina/período:** TCC00228 - Redes de computadores II para Sistemas de Informação/2018.2

**Professor:** Diego Gimenez Passos

## Descrição

Este trabalho visa apresentar, explicar e analisar alguns métodos de detecção e correção de erros utilizados em redes de computadores. 

Dentre os diversos métodos existentes, serão abordados três. São eles: sem método de correção, paridade bidimensional e código de Hamming. 
Nas sessões a seguir, explicaremos sobre os três métodos.

### Sem codificação

Aqui, os pacotes não passam por nenhum método de codificação/decodificação. Ou seja, não há a detecção ou correção de erros.

### Paridade Bidimensional
Os bits de dados são dispostos em uma matriz _m_ por _n_ e, então, adicionada uma linha e ma coluna para os bits de paridade.
Os bits de cada linha e coluna são somados, a paridade deles é calculada e um bit de paridade é adicionada ao final de cada linha e coluna. Casa haja um número par de bits 1, o bit de paridade tem valor 0 (paridade par) ou 1 (paridade ímpar).

Após calculada a paridade, o pacote codificado é enviado para o destinatário. Este, por sua vez, verifica cada célula da matriz de paridade cruzando o bit de paridade da linha com o da coluna, sendo capaz de detectar e corrigir quando há um, e somente um, bit errado.

### Código de Hamming
Código de correção de erro (corrige no máximo 1 bit por pacote), seus bits de paridade se encontram nas posições com potência de 2, eles são inseridos durante o processo de codificação. 

Valores dos bits de paridade são designados comparando com os bits relacionados a eles(exemplo: paridade 1, verifica 1 bit a partir da posição do mesmo, pula uma casa, verifica mais 1 bit e assim sucessivamente até o final do pacote, a 2, verifica 2 bits a partir da posição do mesmo, pula duas casas, verifica mais 2 bits, etc). Para designar o valor, é feita a soma dos bits, se soma for par, então bit de paridade é 0, se for ímpar, é 1.

Na verificação se compara os mesmos bits relacionados a suas paridades, se bit de paridade for 0 então o resultado tem que ser par, senão, houve um erro que pode ser corrigido caso seja único no pacote, se tiver mais de um erro eles somente são detectados.

## Implementação e execução

Este projeto foi desenvolvido em Python 3.7.0. Portanto, faz-se necessário que esta versão ou uma mais recente esteja instalada.

**Baixando repositório**
```bash
$ git init
$ git clone https://github.com/DaviChalita/codigos-de-verificacao-de-erros.git
$ cd codigos-de-verificacao-de-erros
```

### Sem codificação
**Executando**
```bash
$ py noFEC.py <tam_pacote> <reps> <prob. erro>
```

Veremos, a seguir, uma breve descrição das principais funções utilizadas
#### Função _codePacket(originalPacket)_
"Codifica" o pacote. Porém, como não há codificação, apenas retorna o pacote original.
#### Função _decodePacket(transmittedPacket)_
"Decodifica" o pacote. Porém, como não decodificação, apenas retorna o pacote transmitido.
#### Função _generateRandomPacket(l)_
Gera um pacote aleatório de tamanho _l_.
#### Função _geomRand(p)_
Gera um numero pseudo-aleatorio com distribuicao geometrica.
#### Função _insertErrors(codedPacket, errorProb)_
Insere erros no pacote _codedPacket_ com probabilidade _errorProb_.
#### Função _countErrors(originalPacket, decodedPacket)_
Conta a quantidade de erros inseridos, comparando os bits do pacote original com os bits do pacote "decodificado".


### Paridade Bidimensional

**Executando**
```bash
$ py bidimensional-parity-check.py <tam_pacote> <reps> <prob. erro>
```

Após a escolha dos parâmetros do usuário, os pacotes das matrizes 2x2, 2x3 e 3x3 são gerados e codificados, então os erros são inseridos aleatoriamente. Na decodificação dos pacotes, o programa gera novos bits de paridade sobre os bits do pacote recebido, verificando sua integridade e corrigindo até 1 bit errado por matriz. Então o programa imprime o resultado. 

Veremos, a seguir, uma breve descrição das principais funções utilizadas:
#### Função _geomRand(p)_
Gera um numero pseudo-aleatorio com distribuicao geometrica.
#### Função _insertErrors(codedPacket, errorProb)_
Insere erros no pacote _codedPacket_ com probabilidade _errorProb_.
#### Função _generateRandomPacket(l,linha)_
Gera um pacote aleatório, passando o tamanho do pacote e a quantidade de linhas da matriz.
#### Função _codePacket(originalPacket,linha,coluna)_
Codifica o pacote, passando o pacote original, a quantidade de linahs e colunas como parâmetros.
#### Função _decodePacket(transmittedPacket, linha, coluna)_
Decodifica o pacote transmitido.
#### Função _countErrors(originalPacket, decodedPacket)_
Conta a quantidade de erros inseridos, comparando os bits do pacote original com os bits do pacote decodificado.
#### Função _somarColunaMatriz(parityMatrix, linha, j)_
Soma todos os valores na coluna _j_ da _parityMatrix_. A variável _linha_ é utilizada para percorrer todas as linhas da matriz.
#### Função _somarLinhaMatriz(parityMatrix, coluna, i)_
Soma todos os valores na linha _i_ da _parityMatrix_. A variável _coluna_ é utilizada para percorrer todas as colunas da matriz.

### Código de Hamming
**Executando**
```bash
$ py hamming.py <qtd_bits_dados> <reps> <prob. erro>
```

Veremos, a seguir, uma breve descrição das principais funções utilizadas
#### Função _geomRand(p)_
Gera um numero pseudo-aleatorio com distribuicao geometrica.
#### Função _insertErrors(codedPacket, errorProb)_
Insere erros no pacote _codedPacket_ com probabilidade _errorProb_.
#### Função _generateRandomPacket(tamanho)_
Gera um pacote aleatório, passando a quantidade de bits de dados.
#### Função _countErrors(originalPacket, decodedPacket)_
Conta a quantidade de erros inseridos, comparando os bits do pacote original com os bits do pacote decodificado.
#### Função _numeroBitsParidade(originalPacket)_
Determina a quantidade de bits de paridade, recebendo os bits de dados como parâmetro.
#### Função _insereEspacosParaBitsParidade(originalPacket)_
Cria um novo pacote, com espaços para os bits de paridade e com os bits de dados em suas devidas posições.
#### Função _hamming(dados)_
Cria um novo pacote, já com os valores finais dos bits de paridade.
#### Função _hammingCorrecao(codedPacketComErros)_
Função para decodificação e correção do pacote recebido.


## Análise dos métodos

<dl>
  <dt>
    Como os diferentes parâmetros afetam a eficiência dos métodos implementados?
  <dt>
  <dd>
    Quanto maior o tamanho do pacote, mais bits errados são inseridos, quanto maior o número de repetições menor proporcionalmente é a taxa de erros e quanto maior a probabilidade de erro, maior a taxa de erros de bits.
  </dd>
  <dt>
    O quão eficazes esses métodos são em relação a uma solução sem utilização de mecanismos de codificação?
  <dt>
  <dd>
    Esses métodos são mais eficazes porque eles conseguem verificar uma quantidade maior de bits (vários bits de dados para 1 bit de controle) do que uma verificação sem mecanismo de codificação, <span style="color:red;"><b>que não tem bits de controle???</b></span>
  </dd>
  <dt>
    Qual método (paridade bidimensional ou Codificação de Hamming) foi mais eficiente em geral?
  <dt>
  <dd>
    Resposta aqui
  </dd>
  <dt>
    É possível estabelecer uma relação entre o percentual de overhead introduzido (i.e., o quanto o pacote cresce com a adição de
    paridade) e a taxa de erro de bits resultante para cada um dos dois métodos?
  <dt>
  <dd>
    Resposta aqui
  </dd>  
</dl>

## Bibliografia
[Código de Hamming - Codificação, Decodificação e Correção](https://www.youtube.com/watch?v=jmcWNPbsrD4)

[Python function for generating hamming code and detecting single bit error for any size of data length](https://gist.github.com/vatsal-sodha/f8f16b1999a0b5228143e637d617c797)

[Módulo Códigos: código de Hamming](http://eaulas.usp.br/portal/video.action?idItem=7727)
