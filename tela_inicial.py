import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from model import Model
import pygame
import bcrypt
from jogo import Jogo

pygame.init()
pygame.mixer.init()

from PIL import Image, ImageTk

#A tela de login utilizada para entrar no jogo
class TelaInicial:
    def __init__(self, master):
        self.janela = master
        self.largura_tela = self.janela.winfo_screenwidth()
        self.altura_tela = self.janela.winfo_screenheight()
        pos_x = (self.largura_tela // 2) - 750//2
        pos_y = (self.altura_tela // 2) - 450//2
        self.janela.geometry(f'750x450+{pos_x}+{pos_y}')
        self.janela.title('Login')
        self.janela.resizable(False, False)
        pygame.mixer.music.load('musica/bg_music.ogg')
        pygame.mixer.music.play(-1)
        
        self.var_usuario = ttk.StringVar()
        self.var_senha = ttk.StringVar()
        self.var_cad_nome = ttk.StringVar()
        self.var_cad_senha = ttk.StringVar()
        self.var_cad_senha_conf = ttk.StringVar()
        self.modelo = Model()
        
        self.frm_logo = ttk.Frame(self.janela)
        self.frm_logo.grid(row=0, column=0)
        
        self.game_logo = Image.open('imagens/game_logo.png')
        self.game_logo = self.game_logo.resize((482, 260), Image.Resampling.LANCZOS)
        self.game_logo_Tk = ImageTk.PhotoImage(self.game_logo)
        self.lbl_img_logo = ttk.Label(self.frm_logo, image=self.game_logo_Tk)
        self.lbl_img_logo.image = self.game_logo_Tk
        self.lbl_img_logo.grid(row=0, column=0)
        
        self.frm_login = ttk.Frame(self.janela)
        self.frm_login.grid(row=1, column=0)
        
        self.lbl_usuario = ttk.Label(self.frm_login, text='Login: ')
        self.lbl_usuario.grid(row=0, column=0)
        self.ent_usuario = ttk.Entry(self.frm_login, textvariable=self.var_usuario)
        self.ent_usuario.grid(row=0, column=1, columnspan=3)
        
        self.lbl_senha = ttk.Label(self.frm_login, text='Senha: ')
        self.lbl_senha.grid(row=1, column=0)
        self.ent_senha = ttk.Entry(self.frm_login, textvariable=self.var_senha, show='*')
        self.ent_senha.grid(row=1, column=1, columnspan=3)
        self.ent_senha.bind('<Return>', self.entrar)
        
        self.btn_entrar = ttk.Button(self.frm_login, text='Entrar', width=10)
        self.btn_entrar.grid(row=2, column=0, columnspan=2)
        self.btn_entrar.bind('<Button-1>', self.entrar)
        self.btn_cadastrar = ttk.Button(self.frm_login, text='Cadastrar', width=10)
        self.btn_cadastrar.grid(row=2, column=2, columnspan=2)
        self.btn_cadastrar.bind('<Button-1>', self.tela_cadastro)
        
        self.img_chao = Image.open('imagens/chao.webp')
        self.img_chao = self.img_chao.resize((215, 344), Image.Resampling.LANCZOS)
        self.img_chao_Tk = ImageTk.PhotoImage(self.img_chao)
        self.lbl_img_chao = ttk.Label(self.janela, image=self.img_chao_Tk)
        self.lbl_img_chao.image = self.img_chao_Tk
        self.lbl_img_chao.grid(row=0, column=1, rowspan=2)
    
    #Utilizado para fazer o login em si
    #funciona pertando a tecla Enter no entry da senha e no botão "entrar"
    #tambem cria o toplevel da tela do jogo e carrega os componentes pela classe Jogo() pra não poluir
    #esse script q ja ta gigantesco kkkkkkk
    def entrar(self, event):
        nome = self.var_usuario.get()
        senha = self.var_senha.get()
        senha_bytes = senha.encode('utf-8')
        
        try:
            if nome in [i[0] for i in self.modelo.select('SELECT nome FROM usuarios;')]:
                senha_criptografada = self.modelo.select(f"SELECT senha FROM usuarios WHERE nome = '{nome}';")[0][0][2:-1]
                senha_criptografada_bytes = senha_criptografada.encode('utf-8')
                if bcrypt.checkpw(senha_bytes, senha_criptografada_bytes):
                    messagebox.showinfo('Login', 'Login realizado com sucesso!')
                else:
                    raise ValueError
            else:
                raise ValueError
            
            id_jogador = self.modelo.select(f"SELECT id FROM usuarios WHERE nome = '{nome}';")[0][0]
            
            self.janela.iconify()
            jogo = ttk.Toplevel(self.janela)
            Jogo(jogo, self.janela, id_jogador)
            self.var_usuario.set('')
            self.var_senha.set('')
            
        except ValueError:
            messagebox.showwarning('Aviso', 'O usuário ou a senha estão incorretos. Tente novamente.')
    
    #Abre e cria os componentes de um toplevel para a tela de cadastro em que o usuario inclui os dados no BD
    def tela_cadastro(self, event):
        self.top_cadastro = ttk.Toplevel(self.janela)
        pos_x = (self.largura_tela // 2) - 290//2
        pos_y = (self.altura_tela // 2) - 140//2
        self.top_cadastro.geometry(f'290x140+{pos_x}+{pos_y}')
        self.top_cadastro.resizable(False, False)
        self.top_cadastro.title('Cadastro')
        self.top_cadastro.grab_set()
        
        self.cad_lbl_nome = ttk.Label(self.top_cadastro, text='Nome:')
        self.cad_lbl_nome.grid(row=0, column=0)
        self.cad_ent_nome = ttk.Entry(self.top_cadastro, textvariable=self.var_cad_nome)
        self.cad_ent_nome.grid(row=0, column=1)
        
        self.cad_lbl_senha = ttk.Label(self.top_cadastro, text='Senha:')
        self.cad_lbl_senha.grid(row=1, column=0)
        self.cad_ent_senha = ttk.Entry(self.top_cadastro, textvariable=self.var_cad_senha, show='*')
        self.cad_ent_senha.grid(row=1, column=1)
        
        self.cad_lbl_senha_conf = ttk.Label(self.top_cadastro, text='Confirmar senha:')
        self.cad_lbl_senha_conf.grid(row=2, column=0)
        self.cad_ent_senha_conf = ttk.Entry(self.top_cadastro, textvariable=self.var_cad_senha_conf, show='*')
        self.cad_ent_senha_conf.grid(row=2, column=1)
        self.cad_ent_senha_conf.bind('<Return>', self.confirmar_cadastro)
        
        self.cad_btn_conf = ttk.Button(self.top_cadastro, text='Confirmar')
        self.cad_btn_conf.grid(row=3, column=0, columnspan=2)
        self.cad_btn_conf.bind('<Button-1>', self.confirmar_cadastro)
    
    
    #Inclui os dados do cadastro do usuario no BD
    #funciona tanto apertando a tecla Enter no entry do confirmar senha quanto no botao entrar
    def confirmar_cadastro(self, event):
        nome = self.var_cad_nome.get()
        senha = self.var_cad_senha.get()
        senha_conf = self.var_cad_senha_conf.get()
        
        try:
            if nome == '' or senha == '' or senha_conf == '':
                messagebox.showwarning('Aviso', 'Todos os campos devem ser preenchidos!')
                raise ValueError
            if nome in [i[0] for i in self.modelo.select('SELECT nome FROM usuarios;')]:
                messagebox.showwarning('Aviso', 'Usuário já registrado no sistema!')
                raise ValueError
            if senha != senha_conf:
                messagebox.showwarning('Aviso', 'Senhas devem ser iguais!')
                raise ValueError
            
            senha_em_bytes = senha.encode('utf-8')
            senha_criptografada = bcrypt.hashpw(senha_em_bytes, bcrypt.gensalt())
            
            sql = f'INSERT into usuarios (nome, senha) VALUES ("{nome}", "{senha_criptografada}");'
            self.modelo.comando(sql)
            messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')
            self.top_cadastro.destroy()
        except ValueError:
            pass

#Roda a janela principal do programa
gui = ttk.Window(themename='solar')
TelaInicial(gui)
gui.mainloop()