from customtkinter import *
from rich.traceback import install

install()

set_appearance_mode('dark')

# Variaveis
vez = True
vitoria = ''
pnts_o = 0
pnts_x = 0
partidas_tot = 0

# TopLevel do fim_de_jogo
def reiniciar(origin, root):
    global vez, vitoria

    for linha in root.lista_casas_linha:
        for cont in range(3):
            linha[cont].configure(text='')

    vez = True
    vitoria = ''

    origin.destroy()
    root.deiconify()

class TplFimDeJogo(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title('Fim de Jogo')
        self.geometry('500x350')
        self.resizable(False, False)
        self.grid_propagate(False)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        self.master.withdraw()

        global partidas_tot, pnts_o, pnts_x

        partidas_tot += 1

        self.frame_main = CTkFrame(self,
                                   width=450,
                                   height=300,
                                   fg_color='#303030')
        self.frame_main.grid_propagate(False)
        self.frame_main.grid(row=0, column=0, pady=25, padx=25)

        # Label para exibir os pontos e o total de partidas
        self.lbl_pnts = CTkLabel(self.frame_main,
                                text_color='#efefef',
                                text=f'''
           Pontos do círculo: {pnts_o}
Pontos do X: {pnts_x}
         Total de partidas: {partidas_tot}
                                        ''',
                                font=CTkFont(family='Roboto', size=30),
                                anchor='w')
        self.lbl_pnts.grid(row=0, column=0, columnspan=2, pady=25)

        # Botoes para reiniciar ou sair
        self.but_reiniciar = CTkButton(self.frame_main,
                                       text='Reiniciar',
                                       text_color='#efefef',
                                       width=100,
                                       height=40,
                                       font=CTkFont(family='Roboto', size=17),
                                       command=lambda: reiniciar(self, self.master))
        self.but_reiniciar.grid(row=1, column=0, pady=0, padx=(100, 10))

        self.but_sair = CTkButton(self.frame_main,
                                       text='Sair',
                                       text_color='#efefef',
                                       width=100,
                                       height=40,
                                       font=CTkFont(family='Roboto', size=17),
                                       command=lambda: self.master.destroy())
        self.but_sair.grid(row=1, column=1, pady=0)

# Casa
def func_casa(casa):
    global vez

    if casa.cget('text') == '':
        if vez:
            casa.configure(text='o')
            vez = False
        else:
            casa.configure(text='x')
            vez = True
    else:
        print('inválido')

    # Verificando se houve vitória
    fim_de_jogo(casa.master)


class Casa(CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master,
                         **kwargs,
                         fg_color='#353535',
                         width=300,
                         height=300,
                         corner_radius=0,
                         text='',
                         hover_color='#404040',
                         command=lambda: func_casa(self),
                         font=CTkFont(family='Segoe UI', size=200))


# Função de vitória e empate
def fim_de_jogo(root):
    global vitoria, pnts_o, pnts_x

    # Linha
    for linha in root.lista_casas_linha:
        if linha[0].cget('text') == linha[1].cget('text') == linha[2].cget('text'):
            if linha[0].cget('text') == 'o':
                vitoria = 'o'
            elif linha[0].cget('text') == 'x':
                vitoria = 'x'

    # Coluna
    for coluna in root.lista_casas_coluna:
        if coluna[0].cget('text') == coluna[1].cget('text') == coluna[2].cget('text'):
            if coluna[0].cget('text') == 'o':
                vitoria = 'o'
            elif coluna[0].cget('text') == 'x':
                vitoria = 'x'

    # Diagonal
    if root.lista_casas_linha[1][1].cget('text') != '':
        simbolo_meio = root.lista_casas_linha[1][1].cget('text')

        if root.lista_casas_linha[0][0].cget('text') == simbolo_meio == root.lista_casas_linha[2][2].cget('text'):
            vitoria = str(simbolo_meio)

        if root.lista_casas_linha[2][0].cget('text') == simbolo_meio == root.lista_casas_linha[0][2].cget('text'):
            vitoria = str(simbolo_meio)

    if vitoria == 'x':
        pnts_x += 1
        tpl_end_game = TplFimDeJogo(root)
    elif vitoria == 'o':
        pnts_o += 1
        tpl_end_game = TplFimDeJogo(root)

    # Empate
    cont_linhas_comp = 0
    linhas_analisadas = []
    for linha in root.lista_casas_linha:
        if linha[0].cget('text') != '' and linha[1].cget('text') != '' and linha[2].cget('text') != '' and linha not in linhas_analisadas:
            cont_linhas_comp += 1
            linhas_analisadas.append(linha)

    if cont_linhas_comp == 3 and vitoria == '':
        tpl_end_game = TplFimDeJogo(root)


# MainRoot
class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('960x960')
        self.title('Jogo da velha')
        self.resizable(False, False)
        self.grid_propagate(False)
        self.configure(fg_color='#dfdfdf')

        global vitoria

        # Criando as casas
        self.lista_casas_linha = [[None, None, None],
                                  [None, None, None],
                                  [None, None, None]]

        self.lista_casas_coluna = [[None, None, None],
                                   [None, None, None],
                                   [None, None, None]]

        for x in range(3):
            for y in range(3):
                casa = Casa(self)

                self.lista_casas_linha[x][y] = casa
                self.lista_casas_coluna[y][x] = casa

                casa.grid(row=x, column=y, pady=10, padx=10)

app = App()
app.mainloop()
