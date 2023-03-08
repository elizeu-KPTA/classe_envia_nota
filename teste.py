from tkinter import *
from  tkinter.ttk import *
from banco_sqlite import Banco_sqlite

banco_sqlite = Banco_sqlite()


class tabela:
    def __init__(self):
        janela = Tk()
        teste = Toplevel(janela)
        self.relatorio(teste)
        janela.geometry("1000x600")
        janela.mainloop()
    def criar_tabela(self,janela):
        tabela = Treeview(janela, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        tabela.heading("#0")
        tabela.heading("#1", text=" CNPJ/CPF", command=lambda: self.ordenar_tabela(tabela, 1, False))
        tabela.heading("#2", text="Razão Social", command=lambda: self.ordenar_tabela(tabela, 4, True))
        tabela.heading("#3", text="N° NFS", command=lambda: self.ordenar_tabela(tabela, 3, False))
        tabela.heading("#4", text="E-mail", command=lambda: self.ordenar_tabela(tabela, 4, False))
        tabela.heading("#5", text="NF-e", command=lambda: self.ordenar_tabela(tabela, 5, False))
        tabela.heading("#6", text="Status", command=lambda: self.ordenar_tabela(tabela, 6, False))
        tabela.column("#0", minwidth=0, width=0)
        tabela.column("#1", minwidth=70, width=90, anchor=CENTER)
        tabela.column("#2", width=250)
        tabela.column("#3", width=50, anchor=CENTER)
        tabela.column("#4", width=200, anchor=CENTER)
        tabela.column("#5", width=100, anchor=CENTER)
        tabela.column("#6", width=50, anchor=CENTER)
        tabela.place(relx=0.001, rely=0.05, relwidth=0.975, relheight=0.94)
        return tabela

    def ordenar_tabela(self, tabela, coluna, ascendente):
        dados = [(tabela.set(i, coluna), i) for i in tabela.get_children("")]
        dados.sort(reverse=not ascendente)
        for index, (val, k) in enumerate(dados):
            tabela.move(k, '', index)
        tabela.heading("#" + str(coluna), command=lambda: self.ordenar_tabela(tabela, coluna, not ascendente))
    def preencher_tabela(self,tabela, dados):
        tabela.delete(*tabela.get_children())
        for i in dados:
            tabela.insert("", END, values=i)


    def adicionar_barra_rolagem(self,janela, tabela):
        scrollbar = Scrollbar(janela, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scrollbar.place(relx=0.981, rely=0.05, relwidth=0.015, relheight=0.926)


    def definir_estilo_tabela(self):
        style = Style()
        style.theme_use("default")
        style.map("Treeview")

    def ordenar_coluna(self, tabela, coluna, ordem='crescente'):
        # Obtém os dados da tabela como uma lista de tuplas
        dados = [(tabela.set(id_, coluna), id_) for id_ in tabela.get_children('')]

        # Ordena os dados
        dados.sort(reverse=(ordem == 'decrescente'))

        # Reorganiza as linhas da tabela com base nos dados ordenados
        for index, (valor, id_) in enumerate(dados):
            tabela.move(id_, '', index)
            tabela.item(id_, values=tuple(valor))

    def ordenar_dados(self, dados, coluna):
        """
        Ordena os dados de acordo com a coluna selecionada.
        """
        return sorted(dados, key=lambda x: x[coluna])


    def relatorio(self, janela):
        dados = banco_sqlite.busca_dados_pdf()

        dados_ordenados = self.ordenar_dados(dados, 1)  # Ordena por razão social
        tabela = self.criar_tabela(janela)
        #tabela.heading("#1", text=" CNPJ/CPF", command=lambda: self.ordenar_coluna(tabela, "col1"))
        self.preencher_tabela(tabela, dados_ordenados)
        self.adicionar_barra_rolagem(janela, tabela)
        self.definir_estilo_tabela()

        # tabela.bind("<Double-1>", self.duplo_click_email)
        self.dados_duplo = tabela
        self.listaDadosRelatorio = tabela

tabela()