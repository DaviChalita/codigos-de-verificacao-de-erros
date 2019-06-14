![logos](http://www.professores.uff.br/kowada/wp-content/uploads/sites/63/2017/08/UFF-IC-logos.png)
# Jogo da memória on-line
Trabalho semestral apresentado para a disciplina Redes de Computadores II para Sistemas de Informação.

**Alunos:** Davi Chalita, José Paulo Gomes, Matheus Baldissara

**Instituição:** Universidade Federal Fluminense

**Curso:** Bacharelado em Sistemas de Informação

**Disciplina/período:** TCC00228 - Redes de computadores II para Sistemas de Informação/2018.2

**Professor:** Diego Gimenez Passos

## Utilização
### Preparação do ambiente
Este projeto foi desenvolvido em Python 3.7.0. Portanto, faz-se necessário instalação desta ou superiores versões.

Utilizou-se o módulo [pickle](https://docs.python.org/3/library/pickle.html) do Python para serialização e de-serialização binária de objetos, como arrays e números inteiros ao serem transmitidos pelo socket TCP desta aplicação.

### Baixando repositório
```bash
$ git init
$ git clone https://github.com/DaviChalita/codigos-de-verificacao-de-erros.git
$ cd codigos-de-verificacao-de-erros
```

### Executando os arquivos
Primeiro, deve-se executar o arquivo servidor pelo comando:
```bash
$ py servidor.py [NUMERO_JOGADORES] [DIMENSÃO_TABULEIRO]
```
O programa servidor utiliza a porta 12000. Caso queira trocá-la, a linha 13 deve ser alterada.
Além disso, o programa servidor mostra um "gabarito" com os valores de cada peça.

Após, os clientes são executados pelo comando: 
```bash
$ py cliente.py [IP_SERVIDOR] [PORTA_SOCKET_SERVIDOR]
```

Agora é só aproveitar o jogo!

## Estrutura do projeto
### Estrutura
- main
  - cliente.py: arquivo do programa cliente
  - servidor.py: arquivo do programa servidor
  - utils.py: arquivo com funções variadas
- model
  - jogador.py: arquivo da classe Jogador e seus respectivos métodos e atributos, como identificador, pontuação, socket e endereço;
  - partida.py: arquivo da classe Partida e seus respectivos métodos e atributos, como lista de jogadores, um tabuleiro e número de jogadores;
  - tabuleiro.py: arquivo da classe Tabuleiro e seus respectivos métodos e atributos, como dimensão, número de peças, pares totais e pares descobertos, além um array contendo os valores das peças e outro com os as informações a serem mostradas;

Alguns métodos serão citados e explicados mais adiante.
### Especificação dos métodos e funcionamento 

#### Servidor
##### Método _startTCPServer(serverPort)_
Essa função faz a criação do Socket TCP no servidor, utilizando a variável “serverPort” que contém o número de porta especificada e comunica que está aguardando conexão dos jogadores para o programa servidor.
##### Método  _sendStatus(numPlayers, match)_
Através do socket de cada jogador, essa função é responsável por enviar a todos os jogadores o status da partida, como tabuleiro(de display, sem os valores do tabuleiro original) atualizado, placar de pontuação atualizado e o jogador da vez.
##### Método _sendRoundPlayer(numPlayers, match, roundPlayers)_
Esta função tem como objetivo enviar a todos os jogadores o atual jogador da vez(roundPlayer). Para isso, recebe a partida (contendo o vetor de jogadores), o número de jogadores e o jogador da vez como parâmetros.
##### Método _sendTile(numPlayers, match, tileCoord, tileValue)_
Após receber as coordenadas do jogador da vez, essa função fica responsável por enviar apenas o valor e as coordenadas, revelando assim o valor da peça no tabuleiro display para todos os jogadores da partida.

#### Cliente
##### Método _startTCPClient(serverIp, serverPort)_
Essa função é utilizada para criar um socket cliente TCP informando o IP do servidor (serverIp) e sua porta (serverPort). Após, comunica ao cliente que a conexão foi estabelecida e está aguardando demais jogadores.
##### Método _getCoordinates(dimen)_
Utilizada para ler as coordenadas (de 1 peça por vez) do cliente quando for sua vez de jogar. Faz verificações de valores inválidos, ou seja, que não equivalham a nenhuma peça do tabuleiro, neste caso, pede novamente as coordenadas. Caso as coordenadas sejam válidas, ela as retorna.

#### Utils
Possui dois métodos: um para limpar a tela e outro para apresentar o tabuleiro formatado. Optou-se por criar esta classe para evitar repetição de código, uma vez que esses métodos são utulizados tanto no cliente, quanto no servidor.

#### Partida
Como dito previamente, é a classe referente a uma partida. Possui, como atributos, o úmero de jogaores, uma instância de Tabuleiro e um vetor de jogadores.
##### Métodos  _getters_
Funções para recuperarem o valor dos atributos do objeto
##### Método _addPlayer(self, ident, socket, address)_
Adiociona um novo jogador ao vetor de jogadores
##### Método _showScore(self)_
Cria uma string formatada com as pontuações de cada jogador 

#### Jogador
Como dito previamente, é a classe referente a um jogador. Possui como atributos, um identificado, a pontuação (inicialmente 0), um socket e uma tupla de endereço (contendo IP do hosto do cliente e pota em que o processo está sendo executado).

Além disso, possui métodos para incrementar a pontuação, encerrar a conexão, dentre outras.

#### Tabuleiro
Como dito previamente, é a classe referente a um tabuleiro. Possui como atributos, a dimensão, o número total de peças e de pares. Além do número de pares descobertos , um vetor com os valores das peças e outro vetor de display. 

Além dos métodos a seguir, possui outros para recuperar os atributos supracitados.
##### Método _revealPiece(self, i, j)_
Caso seja um valor válido, retorna o valor indicado pelas coordenadas dadas. Caso contrário, retorna 0.
##### Método _hidePiece(self, i, j)_
Caso seja um valor válido, "esconde" a peça (display nas coordenadas = '?'), posição no array de valores passa a ser negativa, indicando que está fechada, e retorna _true_, indicando que a operação foi realizada. Caso contrário, retorna _false_.
##### Método _removePiece(self, i, j)_
Remove uma peça do tabuleiro de display. Caso ela já tenhaa sido removida, retorna _false_. Se não, retira a peça e retornan _true_, indicando o sucesso da operação.

## Fluxograma - Servidor
1. Cria _socket_ TCP para receber conexões de clientes
2. Inicia-se um laço de repetição (Enquanto o servidor ainda quisere hospedar partidas)
    1. Instancia um objeto da classe Partida, informando o número de jogadores e a dimensão do tabuleiro
    2. Apresenta tabuleiro de valor no servidor
    3. Laço de repetição para aguardar a conexão de todos clientes
       1. Socket do servidor aceita conexão, criando um socket de conexão com o cliente e gaurda seu enderço (IP e porta)
       2. Um novo jogador é adicionado a partida, informando seu identificador, socket de conexão e endereço
       3. Envia identificador para cliente 
    4. Inicia a partida (laço de repetição enquanto ainda houverem peças a serem descobertas)
       - Enquanto for a vez do jogador atual (laço de repetição)
          1. Envia tabuleiro atualizado e pontuação dos jogadores
          2. Envia jogador da vez para todos clientes
          3. Laço para receber as coordenadas da **primeira** peça (caso o jogador envie coordenadas inválidas):
             1. Recebe a mensagem do cliente
             2. Consulta valor da peça
             3. Envia valor da peça
          4. Laço para receber as coordenadas da **segunda** peça (caso o jogador envie coordenadas inválidas):
             1. Recebe a mensagem do cliente
             2. Consulta valor da peça
             3. Envia valor da peça
          5. Verifica se jogador pontuou (caso valores da speças sejam iguais e válidas)
             - Caso pontuou
               1. Incremente placar do jogador
               2. Remove peças
               3. Apresenta tabuleiro no servidor
               4. Caso não haja pares a serem descobertos, encerra laço do tópico 2.IV
             - Caso não pontuou
               1. Esconde valor das peças
               2. Verifica pares descobertos
                  - Caso todos pares foram descobertos, envia "-1" como jogador da vez, indicando aos clientes que a partida acabou
                  - Caso contrário, muda o jogador da vez
               3. Encerra laço 2.IV
    5. Envia tabuleiro atualizado e pontuação dos jogadores
    6. Envia "-1" como jogador da vez para clientes, indicando que partida acabou
    7. Envia vencedor, caso haja, para clientes. Caso haja empate, não haverá vencedor (código "-1")
    8. laço de repetição para encerrar conexão com clientes
    9. Pergunta se deseja iniciar nova partida
       - Caso **queira**, volta ao laço do tópico 2
       - Caso **não** queira, encerra programa

## Fluxograma - Cliente
1. Cria um _socket_ de conexão utilizando o IP e porta do servidor
2. Recebe identificador do servidor
3. Inicia-se a partida (Laço de repetição enquanto jogador da vez for diferente de "-1")
   1. Recebe tabuleiro de display do servidor e o converte em um array utilizando o _pickle_
   2. Recebe a dimensão do tabuleiro do servidor
   3. Recebe o placar do servidor
   4. Recebe o jogador da vez do servidor
   5. Verifica se o jogador da vez
      - Caso seja diferente de "-1", continua no laço
      - Caso seja igual a "-1", vai para tópico 4
   6. Apresenta tabuleiro e placar
   7. Pedindo **primeira** peça
      - Caso o cliente seja o jogador da vez
        1. Solicita coordenadas
        2. Solicita coordenadas enqualto elaas forem inválidas (fora da dimensão do tabuleiro ou fora do padrão de _input_)
        3. Envia coordenadas para servidor
      - Caso o cliente não seja o jogador da vez
        1. Informa quem é o jogador da vez
   8. Clientes recebem valor da peça e coordenadas dela
   9. Verifica validade da peça
      - Se valor for inválido (igual a 0)
        - Pede novas coordenadas para jogador da vez 
        - Informa que jogador da vez esoclheu uma peça inválida para demais clientes
      - Caso contrário, atualiza tabuleiro de display com valor da peça e o apresenta
   10. Pedindo **segunda** peça
      - Caso o cliente seja o jogador da vez
        1. Solicita coordenadas
        2. Solicita coordenadas enqualto elaas forem inválidas (fora da dimensão do tabuleiro ou fora do padrão de _input_)
        3. Envia coordenadas para servidor
      - Caso o cliente não seja o jogador da vez
        1. Informa quem é o jogador da vez
   11. Clientes recebem valor da peça e coordenadas dela
   12. Verifica validade da peça
      - Se valor for inválido (igual a 0)
        - Pede novas coordenadas para jogador da vez 
        - Informa que jogador da vez esoclheu uma peça inválida para demais clientes
      - Caso contrário, atualiza tabuleiro de display com valor da peça e o apresenta
   13. Apresenta as peças escolhidas e informa se jogador pontuou ou não
4. Apresenta placar
5. Informa que o jogo acabou
6. Recebe jogador vencedor
   - Se valor recebido for "-1", houve um empate e, portanto, não houve vencedor
   - Se for diferente, informa o jogador vencedor
7. Encerra conexão
