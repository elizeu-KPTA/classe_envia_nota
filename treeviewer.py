from tkinter import *
from tkinter.ttk import *

class Relatorio:
    def __init__(self):
        self.janela = Tk()
        self.janela.geometry("800x600")
        self.criar_tabela_dados_extraidos()

    def criar_tabela_dados_extraidos(self, janela):
        colunas = ["col1", "col2", "col3", "col4", "col5", "col6", 'col7', 'col8']

        # Criar uma Frame para a tabela
        tabela_frame = Frame(janela, bd=2, relief="solid")
        tabela_frame.place(relx=0.001, rely=0.05, relwidth=0.975, relheight=0.94)

        tabela = Treeview(tabela_frame, height=3, column=colunas)
        tabela.heading("#0")
        tabela.heading("#1", text=" CNPJ/CPF", command=lambda: self.ordenar_tabela_dados(tabela, 0, False))
        tabela.heading("#2", text="Razão Social", command=lambda: self.ordenar_tabela_dados(tabela, 1, True))
        tabela.heading("#3", text="N° NFS", command=lambda: self.ordenar_tabela_dados(tabela, 2, False))
        tabela.heading("#4", text="Chave NFE", command=lambda: self.ordenar_tabela_dados(tabela, 3, False))
        tabela.heading("#5", text="Diretório", command=lambda: self.ordenar_tabela_dados(tabela, 4, False))
        tabela.heading("#6", text="E-mail", command=lambda: self.ordenar_tabela_dados(tabela, 5, False))
        tabela.heading("#7", text="N inf", command=lambda: self.ordenar_tabela_dados(tabela, 3, False))
        tabela.heading("#8", text="Data", command=lambda: self.ordenar_tabela_dados(tabela, 4, False))
        tabela.column("#0", minwidth=0, width=0)
        tabela.column("#1", minwidth=70, width=90)
        tabela.column("#2", width=250)
        tabela.column("#3", width=30, anchor=CENTER)
        tabela.column("#4", width=150, anchor=CENTER)
        tabela.column("#5", width=100, anchor=CENTER)
        tabela.column("#6", width=50, anchor=CENTER)
        tabela.column("#7", width=10, anchor=CENTER)
        tabela.column("#8", width=50, anchor=CENTER)
        tabela.pack(fill=BOTH, expand=1)
        return tabela

        tabela.configure(borderwidth=2, relief="solid")

        # Adicionando as linhas com tags
        for i in range(10):
            linha = tabela.insert("", "end", text=f"Linha {i+1}")
            for col in colunas:
                tabela.set(linha, col, f"{col}-{i+1}")
            tabela.tag_configure(f"linha-{i+1}", background="white")
            tabela.tag_add(f"linha-{i+1}", linha)

        # Adicionando linhas horizontais na tabela
        tabela.tag_configure("linha-horizontal", background="black")
        for i, col in enumerate(colunas):
            if i == 0:
                continue
            tabela.insert("", "end", text="", values=[""]*len(colunas))
            tabela.tag_add("linha-horizontal", f"{i}::", f"{i}::")

        self.janela.mainloop()

relatorio = Relatorio()