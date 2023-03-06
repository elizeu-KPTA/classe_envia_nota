import sys
from time import sleep
from tkinter import *
from tkinter.ttk import Progressbar
from classe_email import Email
from banco_sqlite import Banco_sqlite

banco_sqlite = Banco_sqlite()

class Gui:

    def __init__(self):
        self.Window = Tk()
        self.Window.geometry('{0}x{1}'.format(600, 400))
        self.iniciar()

    def iniciar(self):
        self.startButton = Button(self.Window, text='Iniciar', command=self.start)
        self.startButton.grid(row=0, column=2)

    def envios_notas(self):
        self.teste = Toplevel(self.Window)
        self.teste.geometry("300x100")
        t = Label(self.teste, text='Enviando notas', bg='white')
        t.place(relx=0.3, rely=0.01)

        try:
            vt = 0
            email = Email('elibatiliere@gmail.com', 'smtp.gmail.com', 587, 'tqfwymvmdtngfczj')
            dados_pdf = banco_sqlite.busca_dados_pdf()
            for i in dados_pdf:
                dados = len(dados_pdf)
                caminho = i[4]
                e = str(i[5])
                codigo = i[6]
                data = i[7]
                self.progress = DoubleVar()
                self.progress.set(0)
                self.progressBar = Progressbar(self.teste, maximum=100, orient=HORIZONTAL, variable=self.progress)
                self.progressBar.grid(column=3, row=8, columnspan=6, padx=20, pady=40)
                self.progressBar.place(rely=0.3, relwidth=0.99, relheight=0.2)
                inc = (vt / dados) * 100
                self.progress.set(inc)
                print(inc)
                self.teste.update_idletasks()
                self.progress.set(100)
                email.envia_emails(i[1] + '.PDF', str(caminho), e, 'Teste de envios', codigo, data)
                dados = i[1]

                texto = Text(self.teste, bg='white', fg='Black', font=('Arial', 10))
                texto.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.3)
                texto.insert('end',dados)
                self.Window.update()
                vt += 1
                if inc > 99.38:
                    self.teste.destroy()

        except Exception as e:
            print(e)

        self.teste.transient(self.Window)  #
        self.teste.focus_force()  #
        # novaTela.grab_set()  #
        self.teste.resizable(False, False)
        self.teste.mainloop()


    def run(self):
        self.Window.mainloop()
        return 0

if __name__ == '__main__':
    Gui = Gui()
    sys.exit(Gui.run())



