import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from model import Model
from PIL import Image, ImageTk
from random import randint

class Jogo:
    #Inicia a classe da tela do jogo e define os componentes
    #Não entendi muito bem como pegava a janela "mãe" do toplevel então só coloquei como outro
    #parâmetro pro init receber mesmo
    #também recebe o id do jogador para o jogo identificar o chao sempre que necessário
    def __init__(self, master, principal, id_jogador): #self, master, id_jogador
        self.principal = principal
        self.janela = master
        self.modelo = Model()
        self.id_jogador = id_jogador
        
        self.largura_tela = self.janela.winfo_screenwidth()
        self.altura_tela = self.janela.winfo_screenheight()
        pos_x = (self.largura_tela // 2) - 650//2
        pos_y = (self.altura_tela // 2) - 360//2
        self.janela.geometry(f'650x360+{pos_x}+{pos_y}')
        self.janela.title('Chao Garden')
        self.janela.resizable(False, False)
        
        self.mnu_barra = ttk.Menu(self.janela)
        self.mnu_item_arq = ttk.Menu(self.mnu_barra, tearoff=0)
        self.mnu_barra.add_cascade(label='Arquivo', menu=self.mnu_item_arq)
        self.mnu_item_arq.add_command(label='Sair', command=self.sair)
        self.mnu_item_arq.add_command(label='Resetar', command=self.conf_resetar)
        
        self.frm_main = ttk.Frame(self.janela)
        self.frm_main.pack(anchor='center')
        
        self.frm_status = ttk.Frame(self.frm_main)
        self.frm_status.grid(row=0, column=0)
        
        self.lbl_nome = ttk.Label(self.frm_status, text='Nome: Teste') #text=chao.nome
        self.lbl_nome.pack()
        self.lbl_pontos = ttk.Label(self.frm_status, text='Pontuação: 0')
        self.lbl_pontos.pack()
        self.lbl_status = ttk.Label(self.frm_status, text='STATUS:')
        self.lbl_status.pack()
        self.lbl_carinho = ttk.Label(self.frm_status, text='Carinho: 100%')
        self.lbl_carinho.pack()
        self.lbl_higiene = ttk.Label(self.frm_status, text='Higiene: 100%')
        self.lbl_higiene.pack()
        self.lbl_diversao = ttk.Label(self.frm_status, text='Diversao: 100%')
        self.lbl_diversao.pack()
        self.lbl_sono = ttk.Label(self.frm_status, text='Sono: 100%')
        self.lbl_sono.pack()
        self.lbl_fome = ttk.Label(self.frm_status, text='Fome: 100%')
        self.lbl_fome.pack()
        
        self.img_chao = Image.open(self.modelo.con.caminho('imagens/sprite_chao.png'))
        self.img_chao = self.img_chao.resize((304, 304), Image.Resampling.LANCZOS)
        self.img_chaoTk = ImageTk.PhotoImage(self.img_chao)
        self.lbl_img_chao = ttk.Label(self.frm_main, image=self.img_chaoTk)
        self.lbl_img_chao.grid(row=0, column=1)
        
        self.frm_acao = ttk.Frame(self.frm_main)
        self.frm_acao.grid(row=0, column=2)
        
        self.lbl_acoes = ttk.Label(self.frm_acao, text='Ações:')
        self.lbl_acoes.pack()
        self.btn_acao1 = ttk.Button(self.frm_acao, text='Acariciar', bootstyle='success-outline', command=self.acariciar)
        self.btn_acao1.pack()
        self.btn_acao2 = ttk.Button(self.frm_acao, text='Dar banho', bootstyle='success-outline', command=self.dar_banho)
        self.btn_acao2.pack()
        self.btn_acao3 = ttk.Button(self.frm_acao, text='Brincar', bootstyle='success-outline', command=self.brincar)
        self.btn_acao3.pack()
        self.btn_acao4 = ttk.Button(self.frm_acao, text='Fazer dormir', bootstyle='success-outline', command=self.fazer_dormir)
        self.btn_acao4.pack()
        self.btn_acao5 = ttk.Button(self.frm_acao, text='Alimentar', bootstyle='success-outline', command=self.alimentar)
        self.btn_acao5.pack()
        
        self.janela.config(menu=self.mnu_barra)
        
        
        self.atualizar_tela()
    
    #Fecha o jogo e volta pra tela inicial
    def sair(self):
        self.principal.deiconify()
        self.janela.destroy()
    
    #Apaga os dados do chao no banco de dados para que seja criado um novo para o mesmo jogador
    #há um parâmetro para ignorar a messagebox perguntando se quer resetar ou nao
    #por que essa so e pra ser usada quando clica em "resetar" no botao menu
    #acabou ficando meio redundante no código, tentar arrumar mais tarde
    def conf_resetar(self, ign=False):
        if not ign:
            resp = messagebox.askquestion('Aviso', 'Tem certeza que deseja reiniciar o jogo?')
            if resp == 'yes':
                self.modelo.comando(f'DELETE FROM chao WHERE jog_id = {self.id_jogador};')
                self.nomear()
        else:
            self.modelo.comando(f'DELETE FROM chao WHERE jog_id = {self.id_jogador};')
            self.nomear()
    
    #Abre um toplevel para nomear o Chao
    def nomear(self):
        self.janela.iconify()
        self.nome = ttk.StringVar()
        self.tela_nomear = ttk.Toplevel(self.janela)
        pos_x = (self.largura_tela // 2) - 230//2
        pos_y = (self.altura_tela // 2) - 70//2
        self.tela_nomear.geometry(f'230x70+{pos_x}+{pos_y}')
        self.tela_nomear.title('Defina o nome do chao')
        self.tela_nomear.resizable(False, False)
        self.tela_nomear.grab_set()
        
        frm = ttk.Frame(self.tela_nomear)
        frm.pack(anchor='center')
        lbl = ttk.Label(frm, text='Nome:')
        lbl.grid(row=0, column=0)
        ent = ttk.Entry(frm, textvariable=self.nome)
        ent.grid(row=0, column=1)
        ent.bind('<Return>', self.conf_nome)
        btn = ttk.Button(frm, text='Confirmar')
        btn.grid(row=1, column=0, columnspan=2)
        btn.bind('<Button-1>', self.conf_nome)
    
    #Inclui o nome e dados aleatórios entre 80 e 100 nos status do chao no BD e relaciona com o id do jogador
    #Não inicia todos com 100 por que a tela não atualiza em tempo real
    #se mudar pra ela atualizar em tempo real, mudar todos pra 100
    #pode ocorrer apertando a tecla Enter no entry do nome ou clicando no botao confirmar
    def conf_nome(self, event):
        try:
            nome = self.nome.get()
            if nome == '':
                raise Exception
            self.pontos = 0
            self.modelo.comando(f'INSERT INTO chao (nome, carinho, higiene, diversao, sono, fome, pontos, jog_id) VALUES ("{nome}", {randint(80, 100)}, {randint(80, 100)}, {randint(80, 100)}, {randint(80, 100)}, {randint(80, 100)}, 0, {self.id_jogador});')
            messagebox.showinfo('Nome confirmado', 'Chao nomeado com sucesso!')
            self.atualizar_tela()
            self.janela.deiconify()
            self.tela_nomear.destroy()
        except Exception:
            messagebox.showwarning('Campo não preenchido', 'Você deve dar um nome a seu chao!')
        
    #Atualiza as informações das strings na tela e força o reinício se necessario
    #Feito após cada ação em vez de ser em tempo real, o que pode apresentar algumas falhas como
    #poder fechar a tela de nomear o Chao e isso deixar o jogo meio bugado. tentar refazer isso antes do dia 07/10 (entrega)
    def atualizar_tela(self):
        try:
            #isso ta aqui por que quando a tela de nomear fecha ele tira o grab set por algum motivo (???)
            self.janela.grab_set()
            if self.id_jogador not in [i[0] for i in self.modelo.select('SELECT jog_id FROM chao;')]:
                raise Exception
            
            nome, carinho, higiene, diversao, sono, fome, pontos = self.modelo.select(f'SELECT * FROM chao WHERE jog_id = {self.id_jogador};')[0][1:-1]
            
            if 0 in self.modelo.select(f'SELECT * FROM chao WHERE jog_id = {self.id_jogador};')[0][2:-2]:
                messagebox.showinfo('Game Over', f'Seu chao faleceu!\nPontuação final: {pontos-1}\no jogo será reiniciado.')
                raise Exception
            
            self.lbl_nome.config(text=f'Nome: {nome}')
            self.lbl_pontos.config(text=f'Pontuação: {pontos}')
            self.lbl_carinho.config(text=f'Carinho: {carinho}%')
            self.lbl_higiene.config(text=f'Higiene: {higiene}%')
            self.lbl_diversao.config(text=f'Diversão: {diversao}%')
            self.lbl_sono.config(text=f'Sono: {sono}%')
            self.lbl_fome.config(text=f'Fome: {fome}%')
        except Exception:
            self.conf_resetar(True)
    
    #realiza o algoritmo das porcentagens após cada ação realizada
    #mudei um pouco os valores em relação aos diagramas pro jogo ficar menos dificil
    #caso conseguir implementar atualizar a tela em tempo real, lembrar
    #de passar o algoritmo de desconto das acoes pro self.atualizar_tela() e
    #diminuir o randint pra randint(1, 3) e tambem ter um tempo decentemente longo
    #pra tela atualizar (tipo de 3 a 5 segundos), assim o jogo vai ficar mais
    #dinamico. (provavelmente nao vai dar tempo mas enfim)
    #o valor adicionado da açao realizada tbm deve ter um randint caso isso seja feito
    def agir(self, acao):
        acoes = ['carinho', 'higiene', 'diversao', 'sono', 'fome']
        valores = [int(i) for i in self.modelo.select(f'SELECT * FROM chao WHERE jog_id = {self.id_jogador};')[0][2:-1]]
        valor_mod = acao
        
        for i in range(0, 5):
            if acoes[i] == valor_mod:
                if valores[i] + 20 >= 100:
                    valor_novo = 100
                else:
                    valor_novo = valores[i]+20
            else:
                num = randint(1, 10)
                if valores[i] - num < 0:
                    valor_novo = 0
                else:
                    valor_novo = valores[i]-num
                
            self.modelo.comando(f'UPDATE chao SET {acoes[i]} = {valor_novo} WHERE jog_id = {self.id_jogador};')
            
        self.modelo.comando(f'UPDATE chao SET pontos = {valores[5]+1} WHERE jog_id = {self.id_jogador};')
        self.atualizar_tela()
    
    #funções ligadas a cada botão de ação que redirecionam à função self.agir()
    def acariciar(self):
        self.agir('carinho')
    
    def dar_banho(self):
        self.agir('higiene')
    
    def brincar(self):
        self.agir('diversao')
    
    def fazer_dormir(self):
        self.agir('sono')
    
    def alimentar(self):
        self.agir('fome')

#Para testar a janela
#gui = ttk.Window(themename='solar')
#Jogo(gui)
#gui.mainloop()