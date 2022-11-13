# Arquivo que possui todas as funções que têm mais a ver com recursos necessários para tratamento de dados, converte
# comparações, prints. Para que o projeto em si fique mais organizado, foi separado dessa forma os arquivos
# Com isso, neste arquivo contém apenas as funções de auxilio.

# Cores para deixar o print mais intuitivo.
certo = "\033[92m"
reset = '\033[0m'
aviso = '\033[91m'


# É uma função para printar o menu já todo formatado corretamente, mostrando o arquivo carregado e tipo de mapeamento
def print_menu(arq_name='', tipo=''):
    if arq_name == '' and tipo == '':
        arq_name = 'Nenhum arquivo carregado'
        tipo = 'Nenhum mapeamento ativo'
    print("-"*69)
    print("|" + " "*23, "* Menu Principal *" + " "*24, "|")
    print("-" * 69)
    print(f"|-> Carregar Arquivo  1 | Arquivo Carregado:{arq_name:<24}|")
    print(f"|-> Tipo de Mapeamento:{tipo}")
    print("|-> Sair [S/n]"+" "*54+"|")
    print("-" * 69)


# Função que abre o arquivo em modo de leitura, retira os dados e armazena em uma lista.
# Usando um for para percorrer o arquivo retirando o \n dos dados e convertendo em inteiro
# Em um caso especial do Associativo por Conjunto em que busca : para separar a quantidade de linha por conjunto e
# a quantidade de conjunto
def open_file(path):
    arq = open(path, 'r')
    if arq is None:
        print('Não foi possível abrir o arquivo')
        return None
    tipo = ''
    dados = []
    for line in arq:
        if ':' in line:
            aux = line.split(':')
            if aux[1] > aux[0]:
                raise Exception('Número de conjuntos maior que o número de linhas da cache!!!\n'
                                'Mude no arquivo por favor')
            else:
                dados.append(int(aux[0]))
                dados.append(int(aux[1].strip('\n')))
            continue
        if '\n' in line:
            dados.append(int(line.strip('\n')))
        else:
            tipo = line

    arq.close()

    return dados, tipo


# Cria uma lista de lista para representar a cache
# Com um conceito chamado list comprehensions que basicamente faz um for dentro da lista colocando outra lista com um
# Valor 'Vazio' para representar uma linha da cache não preenchida, que foi necessário para fazer do mundo que eu achei 
# melhor de fazer que era de considerar o endereço em binário como uma lista separando bit a bit
def new_mc(line):
    new_cache = [['Vazio'] for _ in range(line)]
    return new_cache


# Cria uma lista tridimensional para representar a cache no mapeamento Associativo por Conjunto
# Que na forma que eu projetei todos os mapeamentos baseado em lista o endereço em binario, acabou ficando uma lista
# Tridimensional, para representar a Cache, o Conjunto e a linha 
def new_mc_set(line, mc_set):
    if mc_set is not None:
        new_cache_set = [['Vazia' for _ in range(int(line/mc_set))] for _ in range(mc_set)]
        return new_cache_set


# Função para converter um número binario para decimal
def bin_to_decimal(n):
    return int(n, 2)


# Uma função que recebe um endereço fornecido por parametro na função e completa com a quantidade
# de bits do endereço da MP
def quant_bin(qtd, num):
    binario = str(bin(num).removeprefix('0b'))
    binario = ((qtd - len(binario)) * '0') + binario

    return binario


# É passando por parametro um endereço e o tamanho do enderço da MP, e como é uma função recorrente, primeiro converte
# em binario e adiciona 0 que faltam para atingir os bits necessários de endereço, e depois faz um processo de separar
# bit a bit em uma lista, para que fique mais facil de separar cada sessão.
def slice_bin(address, ender):
    a = 1
    result = []
    binario = quant_bin(address, ender)
    for i in range(0, len(binario), a):
        # Converte para inteiro, depois do processo de fatiamento
        result.append(int(binario[i: i + a]))

    return binario, result


# O intuito dessa função é apenas de tratar a entrada do usuário para que ele não digite um número de endereço
# maior que a MP permite, usando de uma técnica chamada Expressão Condicional, que é muito similar a ideia
# do Operador Ternario, que faz um if e else em uma linha.
def treatment_input(dados):
    ender = -1
    while ender < 0 or ender > (dados[0] - 1):
        # a barra invertida(\) nessa linha é só pra continuar a expressão condicional em outra linha
        # caso não funcione, só deixar tudo na mesma linha.
        ender = int(input(f'Digite o endereço entre 0 e {dados[0] - 1}:')) \
            if ender < 0 or ender > (dados[0] - 1) else print('Você digitou um número fora da faixa, por favor')
    return ender


# Um função print que têm como objetivo mostrar a linha da cache endereçada, duas antes e duas após
# Como o print é comum aos 3 mapeamentos, como via de praticidade foi feita uma função para englobar a todos
# No caso do Associativo, que têm uma idéia diferente por ser aleatório, o print dele é diferente dos outros, para que
# possa ser impresso corretamente ele, o print_cache recebe o tipo como parâmetro e verifica se é o Associativo para
# fazer essa distinção
def print_cache(cache, pos, tam, tp=''):
    tipo = 'associativo'
    if tp.casefold() == tipo.casefold():
        print('Tipo:', tp)
        print('Posição | Tag e Conteudo')
        print(pos)
        print(bin(pos - 2).removeprefix('0b'), ':',
              cache[pos - 2] if pos - 2 >= 0 else aviso + 'Fora da linha' + reset)
        print(bin(pos - 1).removeprefix('0b'), ':',
              cache[pos - 1] if pos - 1 >= 0 else aviso + 'Fora da linha' + reset)
        print(certo, (bin(pos).removeprefix('0b')), ':', cache[pos], reset)
        print(bin(pos + 1).removeprefix('0b'), ':',
              cache[pos + 1] if pos + 1 <= tam - 1 else aviso + 'Fora da linha' + reset)
        print(bin(pos + 2).removeprefix('0b'), ':',
              cache[pos + 2] if pos + 2 <= tam - 1 else aviso + 'Fora da linha' + reset)
    else:
        print('Posição | Tag e Conteudo')
        print(quant_bin(tam, pos - 2) + 4 * ' ' + ':',
              cache[pos - 2] if pos > 1 else aviso + 'Fora da linha' + reset)
        print(quant_bin(tam, pos - 1) + 4 * ' ' + ':',
              cache[pos - 1] if pos > 0 else aviso + 'Fora da linha' + reset)
        print(certo + (quant_bin(tam, pos)) + 4 * ' ' + ':', cache[pos], reset)
        print(quant_bin(tam, pos + 1) + 4 * ' ' + ':',
              cache[pos + 1] if pos + 1 <= (2 ** tam) - 1 else aviso + 'Fora da linha' + reset)
        print(quant_bin(tam, pos + 2) + 4 * ' ' + ':',
              cache[pos + 2] if pos + 2 <= (2 ** tam) - 1 else aviso + 'Fora da linha' + reset)


# Todos os mapeamentos possuem o acerto e falha, então para evitar repetição de código, foi feita essa função para que
# Evita-se isso e também para que seja padronizada todos as impressões em todos os mapeamentos
def print_miss_hit(acerto, falha, total):
    if total > 0:
        print(f'Falha:{(falha / total) * 100:0.2f}%\tAcerto:{(acerto / total) * 100:0.2f}%')
