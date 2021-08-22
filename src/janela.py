import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk


class LstmClass:
    def init(self, master=None):
        self.master = master
        self.container1 = Frame(self.master)
        self.container1.grid()
        self.textoInicial = Label(self.container1, text="Selecione abaixo as entradas do modelo")
        self.textoInicial.grid(row=0)
        self.initVariables()
        self.initCheckboxes()
        self.initButton()

    # Definição das variáveis
    def initVariables(self):
        self.gameDuration = tk.StringVar()
        self.firstBlood = tk.StringVar()
        self.firstTower = tk.StringVar()
        self.firstInhibitor = tk.StringVar()
        self.firstBaron = tk.StringVar()
        self.firstDragon = tk.StringVar()
        self.firstRiftHerald = tk.StringVar()

    # Checkbuttons com as seleções das variáveis
    def initCheckboxes(self):
        self.container2 = Frame(self.master)
        self.container2.grid()
        self.chkGameDuration = tk.Checkbutton(self.container2, text='Tempo de jogo', var=self.gameDuration)
        self.chkGameDuration.grid(column=0, row=0, padx=10, pady=10)
        self.chkFirstBlood = tk.Checkbutton(self.container2, text='Primeiro abate', var=self.firstBlood,
                                            onvalue="FirstBlood", offvalue="")
        self.chkFirstBlood.grid(column=1, row=0, padx=10, pady=10)
        self.chkfirstTower = tk.Checkbutton(self.container2, text='Primeira torre', var=self.firstTower)
        self.chkfirstTower.grid(column=2, row=0, padx=10, pady=10)
        self.chkfirstInhibitor = tk.Checkbutton(self.container2, text='Primeiro inibidor', var=self.firstInhibitor)
        self.chkfirstInhibitor.grid(column=3, row=0, padx=10, pady=10)
        self.chkfirstBaron = tk.Checkbutton(self.container2, text='Primeiro baron', var=self.firstBaron)
        self.chkfirstBaron.grid(column=0, row=1, padx=10, pady=10)
        self.chkfirstDragon = tk.Checkbutton(self.container2, text='Primeiro dragão', var=self.firstDragon)
        self.chkfirstDragon.grid(column=1, row=1, padx=10, pady=10)
        self.chkfirstRiftHerald = tk.Checkbutton(self.container2, text='Primeiro arauto', var=self.firstRiftHerald)
        self.chkfirstRiftHerald.grid(column=2, row=1, padx=10, pady=10)

    # Botão de iniciar modelo
    def initButton(self):
        self.container3 = Frame(self.master)
        self.container3.grid(pady=10)
        self.button = Button(self.container3)
        self.button["text"] = "Executar"
        self.button["pady"] = 5
        self.button["width"] = 10
        self.button.bind("<Button-1>", self.plot)
        self.button.grid(row=0)

    def plot(self, event):
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self.container3)
        canvas.get_tk_widget().grid(row=1, pady=10, padx=10)
        canvas.draw()


janela = Tk()
janela.title("Modelo preditivo - LSTM")
lstmClass = LstmClass()
lstmClass.init(janela)

# Executar
janela.mainloop()
