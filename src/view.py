import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.LstmModel import LstmModel

matplotlib.use('TkAgg')
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class LstmClass:
    def init(self, master=None):
        self.master = master
        self.lstmModel = LstmModel()
        self.container1 = Frame(self.master)
        self.container1.grid()
        self.textoInicial = Label(self.container1, text="Selecione abaixo as entradas do modelo")
        self.textoInicial.grid(row=0)
        self.initCheckboxes()
        self.initButton()

    # Checkbuttons com os textos das entradas
    def initCheckboxes(self):
        self.container2 = Frame(self.master)
        self.container2.grid()

        my_entries = ['gameDuration', 'firstBlood', 'firstTower', 'firstInhibitor', 'firstBaron', 'firstDragon',
                      'firstRiftHerald']
        self.check_boxes = []

        for item in my_entries:
            string_var = tk.StringVar()
            self.check_boxes.append(string_var)

            cb = tk.Checkbutton(self.container2, text=item, variable=string_var, anchor='w', onvalue=item, offvalue='',
                                width=50)
            cb.grid()

    # Botão de iniciar modelo
    def initButton(self):
        self.container3 = Frame(self.master)
        self.container3.grid(pady=10)
        self.button = Button(self.container3)
        self.button["text"] = "Executar"
        self.button["pady"] = 5
        self.button["width"] = 10
        self.button.bind("<Button-1>", self.runLstm)
        self.button.grid(row=0)

    def runLstm(self, event):
        entries = []

        for string_var in self.check_boxes:
            text = string_var.get()
            if text:
                entries.append(text)

        entries.append("winner")
        self.lstmModel.init(entries)

        path = ("./fig.png")
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)

        label = Label(self.container3, image=photo)
        label.image = photo
        label.grid(row=1)
        # label.pack()

janela = Tk()
janela.title("Modelo preditivo - LSTM")
lstmClass = LstmClass()
lstmClass.init(janela)

# Executar
janela.mainloop()
