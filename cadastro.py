import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Cadastro:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry('750x740')

gui = ttk.Window(themename='solar')
Cadastro(gui)
gui.mainloop()