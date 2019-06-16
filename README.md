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

Dentre os diversos métodos existentes, serão abordados três. São eles: paridade bidimensional, código de Hamming e Código Convolucional utilizado no IEEE 802.11g. Este último, ao contrário dos demais, conterá somente uma descrição.

Nas sessões a seguir, explicaremos sobre os três métodos.

### Sem codificação

### Paridade Bidimensional

### Código de Hamming

### Código Convolucional do IEEE 802.11g


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
#### Função _A()_
lorem ipsum
#### Função _B()_
lorem ipsum


### Paridade Bidimensional
**Executando**
```bash
$ py bidimensional-parity-check.py <tam_pacote> <reps> <prob. erro>
```

Veremos, a seguir, uma breve descrição das principais funções utilizadas
#### Função _A()_
lorem ipsum
#### Função _B()_
lorem ipsum

### Código de Hamming
**Executando**
```bash
$ py hamming.py <tam_pacote> <reps> <prob. erro>
```

Veremos, a seguir, uma breve descrição das principais funções utilizadas
#### Função _A()_
lorem ipsum
#### Função _B()_
lorem ipsum


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
    Esses métodos são mais eficazes porque eles conseguem verificar uma quantidade maior de bits (vários bits de dados para 1 bit de controle) do que uma verificação sem mecanismo de codificação, 

- ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `que não tem bits de controle?????`
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
