# Um Simulador que não é bem um simulador.

# Trabalho realizado para a disciplina de Arquitetura e Organização de Computadores.
# Do Curso de Engenharia da Computação.
# Ministrado pelo Prof.Me. Rodrigo Porfírio da Silva Sacchi

# Autor: Mateus Souza Silva

# Dourados-MS 2022

from math import log2   # Importando no pacote de matematica apenas o log na base 2.
import os  # Pacote que serve para utilizar os comando do SO, que utilizei posteriormente.
from funcoes.recursos import *  # Arquivo que contém todas as funções de auxilio do projeto, que eu criei.
from random import randint  # Importando no pacote randômico apenas o método randômico de números inteiros


# Por questão de boas práticas, criei a função principal do programa, por mais que não seja necessário para organização
# é proveitoso fazer.
def main():
    menu()


def menu(arq_name='', tipo=''):

    print_menu(arq_name, tipo)
    op = input("Escolha uma das opções acima:")
    match op:
        case '1':
            path = input("Digite o diretório do arquivo:")
            if path != '':
                arq_name = os.path.basename(path)
                file, tipo = menu() if open_file(path) is None else open_file(path)
                cache = new_mc(file[2])
                if tipo == 'Associativo por Conjunto':
                    cache_set = new_mc_set(file[2], file[3])
                    print_menu(arq_name, tipo)
                    switch_mapping(arq_name, tipo, file, cache, cache_set)
                else:
                    switch_mapping(arq_name, tipo, file, cache)

            else:
                print('Diretório Inválido')
                menu()
                input()
                os.system('cls'if os.name == 'nt' else 'close')
        case 'S' | 's' | 'n' | 'N':
            print('Saindo...')
            exit()


def switch_mapping(arq_name='', tipo='', file=None, cache=None, cache_set=None):
    match tipo:
        case 'Direto':
            print('Mapeamento Direto')
            direct_mapping(file, cache, name=arq_name, tp=tipo)
            menu(arq_name, tipo)
        case 'Associativo':
            print('Mapeamento Associativo')
            associative_mapping(file, cache, name=arq_name, tp=tipo)
        case 'Associativo por Conjunto':
            print('Mapeamento Associativo por Conjunto')
            set_associative(file, cache_set, name=arq_name, tp=tipo)


def direct_mapping(dados, cache, fim='', acerto=0.0, falha=0.0, total=0.0, name='', tp=''):
    if fim == 'sair':
        print('Total de acertos e falhas')
        print_miss_hit(acerto, falha, total)
        input()
        os.system('cls' if os.name == 'nt' else 'close')
        menu(name, tp)
    else:
        ender = treatment_input(dados)
        mc = cache
        address = int(log2(dados[0]))
        s = int(log2(dados[0]/dados[1]))
        r = int(log2(dados[2]))
        w = int(log2(dados[1]))
        tag = s - r
        binario, result = slice_bin(address, ender)

        print(f'Endereço :{binario}')
        print('S:', result[:s])
        print('Tag:', result[:tag], 'R:', result[tag:-w] if w > 0 else result[tag:],
              'W:', result[-w:] if w > 0 else 0)

        linha = result[tag:-w] if w > 0 else result[tag:]
        linha = [str(i) for i in linha]
        r_linha = "".join(map(str, linha))
        pos_linha = int(bin_to_decimal(r_linha))
        if mc[pos_linha][:] == 'Vazia' or mc[pos_linha][0] != result[:tag]:
            mc[pos_linha][:] = result[:tag], 'dados'
            falha += 1
            total += 1
        elif mc[pos_linha][0] == result[:tag]:
            acerto += 1
            total += 1

        print_cache(cache, pos_linha, r)

        print_miss_hit(acerto, falha, total)

        fim = input('Digite (sair) pra terminar o mapeamento ou enter para continuar mapeando:').lower()
        os.system('cls' if os.name == 'nt' else 'close')
        direct_mapping(dados, cache, fim, acerto, falha, total, name, tp)


def associative_mapping(dados, cache, fim='', init=0, quant=0, acerto=0.0, falha=0.0, total=0.0, name='', tp=''):

    def cache_cheia(ini):
        if ini == int(dados[2]):
            return True
        return False

    def tag_compare(tg, cache_busca):
        for i in range(len(cache_busca)):
            if cache_busca[i][0] == tg:
                return i
        return -1

    if fim == 'sair':
        print('Total de acertos e falhas')
        print_miss_hit(acerto, falha, total)
        input()
        os.system('cls' if os.name == 'nt' else 'close')
        menu(name, tp)
    else:
        mc = cache
        address = int(log2(dados[0]))
        tam_cache = dados[2]
        tag = int(log2(dados[0] / dados[1]))
        w = int(log2(dados[1]))
        ender = treatment_input(dados)
        binario, result = slice_bin(address, ender)
        busca = tag_compare(result[:tag], cache)

        print(f'Endereço :{binario}')
        print('S/Tag:', result[:tag], 'W:', result[-w:] if w > 0 else 0)

        if busca != -1:
            acerto += 1
            total += 1
            print('Acerto')
            print_cache(mc, busca, tam_cache, tp)
        elif not cache_cheia(quant):
            mc[init][:] = result[:tag], 'dados'
            quant += 1
            falha += 1
            total += 1
            print_cache(mc, init, tam_cache, tp)
            if init == tam_cache-1:
                init = 0
            else:
                init += 1
        else:
            init = randint(0, tam_cache-1)
            mc[init][:] = result[:tag], 'dados'
            falha += 1
            total += 1
            print_cache(mc, init, tam_cache, tp)

        print_miss_hit(acerto, falha, total)

        fim = input('Digite (sair) pra terminar o mapeamento ou enter para continuar mapeando:').lower()
        os.system('cls' if os.name == 'nt' else 'close')
        associative_mapping(dados, cache, fim, init, quant, acerto, falha, total, name, tp)


def set_associative(dados, cache, fim='', fifo=0,  acerto=0.0, falha=0.0, total=0.0, name='', tp=''):
    if fim == 'sair':
        print('Total de acertos e falhas')
        print_miss_hit(acerto, falha, total)
        input()
        os.system('cls' if os.name == 'nt' else 'close')
        menu(name, tp)
    else:
        ender = treatment_input(dados)
        mc = cache
        address = int(log2(dados[0]))
        s = int(log2(dados[0] / dados[1]))
        tam_cache = int(dados[2]/dados[3])
        d = int(log2(dados[3]))
        w = int(log2(dados[1]))
        tag = s - d
        binario, result = slice_bin(address, ender)

        print(f'Endereço :{binario}')
        print('S:', result[:s])
        print('Tag:', result[:tag], 'D:', result[tag:-w] if w > 0 else result[d:],
              'W:', result[-w:] if w > 0 else 0)
        print(tam_cache)
        linha = result[tag:-w] if w > 0 else result[d:]
        linha = [str(i) for i in linha]
        r_linha = "".join(map(str, linha))
        pos_linha = int(bin_to_decimal(r_linha))
        for i in range(tam_cache):
            if mc[pos_linha][i] == 'Vazia':
                mc[pos_linha][i] = result[:tag]
                falha += 1
                total += 1
                break
            elif mc[pos_linha][i] == result[:tag]:
                acerto += 1
                total += 1
                break
            elif 'Vazia' not in mc[pos_linha]:
                mc[pos_linha][fifo] = result[:tag]
                if fifo == (tam_cache-1):
                    fifo = 0
                else:
                    fifo += 1
                break

        print_cache(cache, pos_linha, d)

        print_miss_hit(acerto, falha, total)

        fim = input('Digite (sair) pra terminar o mapeamento ou enter para continuar mapeando:').lower()
        os.system('cls' if os.name == 'nt' else 'close')
        set_associative(dados, cache, fim, fifo, acerto, falha, total, name, tp)


if __name__ == '__main__':
    main()
