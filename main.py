from pygame import *

init()

# Criando a tela
tela = display.set_mode((1180, 590))
display.set_caption('Jogo da velha')

# Criando as divisoes
divisao_um = Rect(190, 0, 10, 590)
divisao_dois = Rect(390, 0, 10, 590)

divisao_tres = Rect(0, 190, 590, 10)
divisao_quatro = Rect(0, 390, 590, 10)

divisao_jogo = Rect(620, 0, 10, 590)

# Criando as areas clicaveis
def criar_areas_clicaveis():
    lado = 190
    blocos = []
    for x in range(3):
        for y in range(3):
            bloco = Rect(y*200, x*200, lado, lado)
            blocos.append(bloco)

    return blocos

areas_clicaveis = criar_areas_clicaveis()

# Funções de criar 'x' e 'o'
lista_x = []
lista_o = []

def criar_x():
    linha = Surface((10, 150), SRCALPHA)
    linha.fill(cores['red'])
    linha_um = transform.rotate(linha, -45)
    linha_dois = transform.rotate(linha, 45)

    linhas = (linha_um, linha_dois)

    lista_x.append(linhas)

    return linhas

def desenhar_x(pos_x, pos_y):
    linhas = criar_x()
    for linha in linhas:
        tela.blit(linha, (pos_x, pos_y))

def desenhar_o(pos_x, pos_y):
    lista_o.append(draw.circle(tela, cores['blue'], (pos_x, pos_y), 60, 10))

# Cores
cores = {
    'white': (180, 210, 255),
    'black': (40, 40, 50),
    'red': (155, 30, 22),
    'blue': (0, 0, 225),
    'yellow': (225, 225, 10)
}

vez = True
total_partidas = 0
pontos_x = 0
pontos_o = 0

# Desenhando as coisas na tela
tela.fill(cores['black'])

# Desenhando as divisoes
draw.rect(tela, cores['white'], divisao_um)
draw.rect(tela, cores['white'], divisao_dois)
draw.rect(tela, cores['white'], divisao_tres)
draw.rect(tela, cores['white'], divisao_quatro)

draw.rect(tela, cores['yellow'], divisao_jogo)

# Desenhando as areas clicaveis
for area in areas_clicaveis:
    draw.rect(tela, cores['black'], area)

# Desenhando a pontuação
def pontuacao():
    global total_partidas
    total_partidas += 1

    textos = []
    fonte = font.SysFont(None, size=50)

    texto_o = fonte.render(f'Pontos do círculo: {pontos_o}', True, cores['white'], None)
    textos.append(texto_o)

    texto_x = fonte.render(f'Pontos do x: {pontos_x}', True, cores['white'], None)
    textos.append(texto_x)

    texto_tot = fonte.render(f'Total de partidas: {total_partidas}', True, cores['white'], None)
    textos.append(texto_tot)

    pos_y = 150
    for texto in textos:
        tela.blit(texto, (680, pos_y))
        pos_y += 70

# Funçao de limpar o tabuleiro
def limpar_tabuleiro():
    global areas_preenchidas, simbolos_por_area, colunas

    lista_x.clear()
    lista_o.clear()
    areas_preenchidas.clear()

    simbolos_por_area = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    colunas = [[], [], []]

    # Redesenhar o tabuleiro
    tela.fill(cores['black'])

    draw.rect(tela, cores['white'], divisao_um)
    draw.rect(tela, cores['white'], divisao_dois)
    draw.rect(tela, cores['white'], divisao_tres)
    draw.rect(tela, cores['white'], divisao_quatro)
    draw.rect(tela, cores['yellow'], divisao_jogo)

    for area in areas_clicaveis:
        draw.rect(tela, cores['black'], area)

# Criando o mainloop
areas_preenchidas = []
simbolos_por_area = [[None, None, None], [None, None, None], [None, None, None]]
colunas = [[], [], []]

while True:
    for evento in event.get():
        if evento.type == QUIT:
            print(simbolos_por_area)
            print(colunas)
            print(lista_x)
            print(lista_o)
            quit()
            exit()
        elif evento.type == MOUSEBUTTONDOWN:
            for area in areas_clicaveis:
                if area.collidepoint(evento.pos):
                    # print(f'Clicou em {areas_clicaveis.index(area)}')
                    meio_area = (area.center[0] - 55, area.center[1] - 55)

                    # Fazendo a parte gráfica de pôr os simbolos (x, o)
                    if vez and area not in areas_preenchidas:
                        desenhar_o(area.center[0], area.center[1])

                        linha = 0
                        if areas_clicaveis.index(area) <= 2:
                            linha = 0
                            simbolos_por_area[linha][areas_clicaveis.index(area)] = 'circle'
                        elif 2 < areas_clicaveis.index(area) <= 5:
                            linha = 1
                            simbolos_por_area[linha][areas_clicaveis.index(area) - 3] = 'circle'
                        elif 5 < areas_clicaveis.index(area) <= 8:
                            linha = 2
                            simbolos_por_area[linha][areas_clicaveis.index(area) - 6] = 'circle'

                        coluna = 0
                        if areas_clicaveis.index(area) in [0, 3, 6]:
                            coluna = 0
                        elif areas_clicaveis.index(area) in [1, 4, 7]:
                            coluna = 1
                        elif areas_clicaveis.index(area) in [2, 5, 8]:
                            coluna = 2
                        colunas[coluna].insert(areas_clicaveis.index(area), 'circle')

                        areas_preenchidas.append(area)
                        vez = False
                    elif not vez and area not in areas_preenchidas:
                        desenhar_x(meio_area[0], meio_area[1])

                        linha = 0
                        if areas_clicaveis.index(area) <= 2:
                            linha = 0
                            simbolos_por_area[linha][areas_clicaveis.index(area)] = 'x'
                        elif areas_clicaveis.index(area) <= 5:
                            linha = 1
                            simbolos_por_area[linha][areas_clicaveis.index(area) - 3] = 'x'
                        elif areas_clicaveis.index(area) <= 8:
                            linha = 2
                            simbolos_por_area[linha][areas_clicaveis.index(area) - 6] = 'x'

                        coluna = 0
                        if areas_clicaveis.index(area) in [0, 3, 6]:
                            coluna = 0
                        elif areas_clicaveis.index(area) in [1, 4, 7]:
                            coluna = 1
                        elif areas_clicaveis.index(area) in [2, 5, 8]:
                            coluna = 2
                        colunas[coluna].insert(areas_clicaveis.index(area), 'x')

                        areas_preenchidas.append(area)
                        vez = True

                    # Sistema de vitória
                    # Testando linha
                    for linha in simbolos_por_area:
                        if linha[0] is not None and linha[1] is not None and linha[2] is not None and all(x == linha[0] for x in linha):
                            if linha[0] == 'x':
                                pontos_x += 1
                            elif linha[0] == 'circle':
                                pontos_o += 1
                            limpar_tabuleiro()
                            pontuacao()

                    # Testando coluna
                    for column in colunas:
                        if len(column) >= 3 and all(x == column[0] for x in column):
                            if column[0] == 'x':
                                pontos_x += 1
                            elif column[0] == 'circle':
                                pontos_o += 1
                            limpar_tabuleiro()
                            pontuacao()

                    # Testando diagonais
                    if areas_clicaveis.index(area) % 2 == 0:
                        if areas_clicaveis[4] in areas_preenchidas:
                            simbolo_meio = simbolos_por_area[1][1]

                            # 1 Diagonal
                            if (areas_clicaveis[0] in areas_preenchidas and simbolos_por_area[0][0] == simbolo_meio) and (areas_clicaveis[8] in areas_preenchidas and simbolos_por_area[-1][-1] == simbolo_meio):
                                if simbolo_meio == 'x':
                                    pontos_x += 1
                                elif simbolo_meio == 'circle':
                                    pontos_o += 1
                                limpar_tabuleiro()
                                pontuacao()

                            # 2 Diagonal
                            elif (areas_clicaveis[2] in areas_preenchidas and simbolos_por_area[0][-1] == simbolo_meio) and (areas_clicaveis[6] in areas_preenchidas and simbolos_por_area[-1][0] == simbolo_meio):
                                if simbolo_meio == 'x':
                                    pontos_x += 1
                                elif simbolo_meio == 'circle':
                                    pontos_o += 1
                                limpar_tabuleiro()
                                pontuacao()

    # Atualizando a tela do jogo
    time.wait(1)
    display.flip()
