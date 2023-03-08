from tkinter import *
from tkinter import ttk

janela = Tk()
janela.geometry("500x500")

# Criando um objeto Style
style = ttk.Style()

# Definindo as propriedades para personalizar a barra de rolagem
style.theme_use("default")
style.configure("Vertical.TScrollbar", troughcolor="grey", sliderlength=30)

# Criando uma tabela
tabela = ttk.Treeview(janela)
tabela.pack(fill=BOTH, expand=1)

# Adicionando uma barra de rolagem personalizada
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview, style="Vertical.TScrollbar")
tabela.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

janela.mainloop()



