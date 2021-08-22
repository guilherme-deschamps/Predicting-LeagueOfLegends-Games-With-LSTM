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
        self.button.bind("<Button-1>", self.plot)
        self.button.grid(row=0)

    def plot(self, event):
        for string_var in self.check_boxes:
            text = string_var.get()
            if text:
                print(text)

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self.container3)
        canvas.get_tk_widget().grid(pady=10, padx=10)
        canvas.draw()


janela = Tk()
janela.title("Modelo preditivo - LSTM")
lstmClass = LstmClass()
lstmClass.init(janela)

# Executar
janela.mainloop()
