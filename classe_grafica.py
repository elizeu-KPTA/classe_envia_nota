from tkinter.ttk import *
import pyautogui
from tkinter import *
from tkinter import messagebox as mb

from banco_sqlite import Banco_sqlite
from classe_email import Email
from classe_diretorios import Diretorios
from leitor_de_pdf import LeitorPDF

banco_sqlite = Banco_sqlite()
diretorios = Diretorios()
leitorPdf = LeitorPDF()

from datetime import date


class Interface:
    def __init__(self):
        super().__init__()
        self._geom = None
        self.email = None
        self.root = Tk()
        self.dadosEnvio = list()
        pad = 3
        self.menu()
        self.root.geometry("1000x600")
        self.centralizar_janelas(self.root)
        self.root.title("NFS Faturamento V 1.0")
        self.root.configure(background='#a4bcd4')
        self._geom = '200x200+0+0'
        self.root.state('zoomed')

        self.root.mainloop()

    def tamanho_tela(self, event):
        geom = self.root.winfo_geometry()
        print(geom, self._geom)
        self.root.geometry(self._geom)
        self._geom = geom

    def centralizar_janelas(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def menu(self):
        menuroot = Menu(self.root)
        cadastro = Menu(menuroot, tearoff=0, background='#a4bcd4')
        cadastro.add_command(label="Clientes", command=self.cadastro_config)
        cadastro.add_command(label="Correio Eletrônico", command=self.abas_cadastro_email)

        cadastro.add_separator()

        cadastro.add_command(label="Exit", command=self.root.quit)
        menuroot.add_cascade(label="Cadastro", menu=cadastro)

        enviar = Menu(menuroot, tearoff=0)
        #  enviar.add_separator()
        enviar.add_command(label="Enviar Boletos", command=self.envia_arquivos)
        enviar.add_command(label="Avisos", command=self.envio_mensagens)
        menuroot.add_cascade(label="Enviar", menu=enviar)

        relatorio = Menu(menuroot, tearoff=0)
        relatorio.add_command(label="Notas enviadas", command=self.dados_relatorio_enviado)
        relatorio.add_command(label="Dados extraídos", command=self.dados_relatorio_extraidos)
        relatorio.add_command(label="Dados pendentes", command=self.donothing)

        menuroot.add_cascade(label="Relatórios", menu=relatorio)
        self.root.config(menu=menuroot)

    def donothing(self):
        novaTela = Toplevel(self.root)
        button = Button(novaTela, text="Botão da nova tela")
        button.pack()

    def ent_mud_nome(self, tecla):

        self.nome_entry.focus()

    def ent_mud_email(self, tecla):
        self.e_mail_entry.focus()

    def ent_mud_cpf(self, tecla):
        self.CNPJ_CPF_entry.focus()

    def cadastro_config(self):
        cor = '#B6C6D6'
        novaTela = Toplevel(self.root)
        self.novaTela = novaTela
        self.lb = Label(novaTela, text='CÓDIGO:', bg=f'{cor}')  # Label do código
        self.lb.place(relx=0.04, rely=0.04)

        self.codigo_entry = Entry(novaTela, bg='LightGray', fg='Black')  # Entry código

        self.codigo_entry.place(relx=0.109, rely=0.04, relwidth=0.07)
        self.codigo_entry.bind("<Return>", self.ent_mud_nome)

        self.lb = Label(novaTela, text='NOME:', bg=f'{cor}')  # ------------------------Label do nome
        self.lb.place(relx=0.04, rely=0.15)

        self.nome_entry = Entry(novaTela, bg='LightGray', fg='Black')  # --Entry do nome
        self.nome_entry.place(relx=0.109, rely=0.15, relwidth=0.57)
        self.nome_entry.bind("<Return>", self.ent_mud_email)

        self.lb = Label(novaTela, text='E-MAIL:', bg=f'{cor}')  # -----------------------Label do Email
        self.lb.place(relx=0.04, rely=0.25)

        self.e_mail_entry = Entry(novaTela, bg='LightGray', fg='Black')  # --Entry do nome
        self.e_mail_entry.place(relx=0.109, rely=0.25, relwidth=0.57)
        self.e_mail_entry.bind("<Return>", self.ent_mud_cpf)

        self.lb = Label(novaTela, text='CNPJ/CPF:', bg=f'{cor}')
        self.lb.place(relx=0.03, rely=0.35)

        self.CNPJ_CPF_entry = Entry(novaTela, bg='LightGray', fg='Black')  # Entry CPF/EMAIL
        self.CNPJ_CPF_entry.place(relx=0.109, rely=0.35, relwidth=0.30)
        self.CNPJ_CPF_entry.bind("<Return>", '')

        bt_salva = Button(novaTela, text='Salvar', command=self.insere_Cadastro)

        bt_salva.place(relx=0.3, rely=0.04, relwidth=0.06, relheight=0.04)

        bt_atualiza = Button(novaTela, text='Atualizar', command=self.atualiza_dados_cadastro)
        bt_atualiza.place(relx=0.4, rely=0.04, relwidth=0.06, relheight=0.04)
        bt_exclui = Button(novaTela, text='Excluir', command=self.exclui_dados_cadastro)
        bt_exclui.place(relx=0.5, rely=0.04, relwidth=0.06, relheight=0.04)
        Style().configure("Excluir", padding=6, relief="flat",
                          background="#FFF001")

        x, y = pyautogui.position()
        y = y - 5

        print(x, y)
        compri = 800
        altura = 450
        novaTela.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))
        novaTela.configure(background=f'{cor}')
        #  novaTela.overrideredirect(False) # Faz com que a janela apareça dentro da outra
        novaTela.title('Cadastro de Clientes')
        self.dados_do_banco(novaTela)
        novaTela.transient(self.root)  #
        novaTela.focus_force()  #
        # novaTela.grab_set()  #
        novaTela.mainloop()

    def insere_Cadastro(self):
        print('Código:', self.codigo_entry.get(), 'nome', self.nome_entry.get(), 'E-mail', self.e_mail_entry.get(),
              'CNPJ',
              self.CNPJ_CPF_entry.get())
        try:
            cadastro = banco_sqlite.insere_cadastro(self.codigo_entry.get(), self.nome_entry.get(),
                                                    self.e_mail_entry.get(), self.CNPJ_CPF_entry.get())  # showerror
            print(cadastro)
            if cadastro == 'Dados ja existe':
                mb.showwarning("Este código já existe!", " O códio informado já existe no banco de Dados!")
            self.limpa_dados_cadastro()
            self.dados_do_banco(self.novaTela)
        except:
            return mb.showerror("ERRO!", f" Um erro ocorreu durante a execução do processo, entre em contato com o "
                                         f"desenvolvedor!")

    def atualiza_dados_cadastro(self):
        banco_sqlite.atualiza_dados_cadastro(self.nome_entry.get(),
                                             self.e_mail_entry.get(), self.CNPJ_CPF_entry.get(),
                                             self.codigo_entry.get())
        self.limpa_dados_cadastro()
        self.dados_do_banco(self.novaTela)

    def exclui_dados_cadastro(self):
        banco_sqlite.exclui_dados_cadastro(self.codigo_entry.get())
        self.limpa_dados_cadastro()
        self.dados_do_banco(self.novaTela)

    def limpa_dados_cadastro(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.e_mail_entry.delete(0, END)
        self.CNPJ_CPF_entry.delete(0, END)

    def dados_do_banco(self, janela):  # Criação da tabela de cadastro.
        dados = banco_sqlite.busca_todos_os_dados_cadastro()
        print(dados)
        scrollbar = Scrollbar(janela)
        listaDados = Treeview(janela, height=3,
                              column=("col1", "col2", "col3", "col4"), yscrollcommand=scrollbar.set)
        listaDados.heading("#0", text="")
        listaDados.heading("#1", text="Código",command=lambda: self.ordenar_tabela(listaDados, 0, False))
        listaDados.heading("#2", text="Nome", command=lambda: self.ordenar_tabela(listaDados, 1, False))
        listaDados.heading("#3", text="E-mail", command=lambda: self.ordenar_tabela(listaDados, 2, False))
        listaDados.heading("#4", text="CNPJ", command=lambda: self.ordenar_tabela(listaDados, 3, False))
        listaDados.column("#0", width=0)
        listaDados.column("#1", width=50)
        listaDados.column("#2", width=150)
        listaDados.column("#3", width=150)
        listaDados.column("#4", width=80)
        listaDados.place(relx=0.02, rely=0.43, relwidth=0.941, relheight=0.53)
        scrollbar.pack(side="right", fill="y")  # Criação da barra de rolagem.
        scrollbar.config(command=listaDados.yview)
        scrollbar.place(relx=0.96, rely=0.433, relwidth=0.028, relheight=0.526)
        listaDados.delete(*listaDados.get_children())
        for i in dados:
            listaDados.insert("", END, values=i)
        self.dados_duplo_clice = listaDados
        listaDados.bind("<Double-1>", self.duploclick)  # busca a função para inserir dados.

    def duploclick(self, event):  # Método será chamado ao clicar duas vezes sobre a tabela.
        self.limpa_dados_cadastro()
        self.dados_duplo_clice.selection()
        for n in self.dados_duplo_clice.selection():
            col1, col2, col3, col4 = self.dados_duplo_clice.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.e_mail_entry.insert(END, col3)
            self.CNPJ_CPF_entry.insert(END, col4)


    def abas_cadastro_email(self):
        cor = '#B6C6D6'
        compri = 600
        altura = 450

        self.configuracao = Toplevel(self.root)
        self.tabControl = Notebook(self.configuracao)
        self.cadastro = Frame(self.tabControl, bg=f'{cor}')
        self.mensagem = Frame(self.tabControl, bg=f'{cor}')

        self.tabControl.add(self.cadastro, text='E-mail')

        self.tabControl.add(self.mensagem, text='Mensagem')

        self.tabControl.pack(expand=1, fill="both")
        self.cadastro_email()
        x, y = pyautogui.position()
        y = y - 20
        print(x, y)
        self.configuracao.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))
        self.configuracao.configure(background='#a4bcd4')
        #  novaTela.overrideredirect(False) # Faz com que a janela apareça dentro da outra
        self.configuracao.title('Configuração do e-mail')
        self.configuracao.transient(self.root)  #
        self.configuracao.focus_force()  #
        # novaTela.grab_set()  #
        self.configuracao.mainloop()

    def cadastro_email(self):

        cor = '#B6C6D6'
        Label(self.cadastro, text=f"Porta:", fg='Black', bg=f'{cor}',
              font=('Arial', 10, 'bold')).place(relx=0.058, rely=0.15)

        Label(self.cadastro, text=f"Senha:", fg='Black', bg=f'{cor}',
              font=('Arial', 10, 'bold')).place(relx=0.058, rely=0.25)

        Label(self.cadastro, text=f"SMTP:", fg='Black', bg=f'{cor}',
              font=('Arial', 10, 'bold')).place(relx=0.058, rely=0.35)

        Label(self.cadastro, text=f"E-mail:", fg='Black', bg=f'{cor}',
              font=('Arial', 10, 'bold')).place(relx=0.058, rely=0.45)

        self.porta = Entry(self.cadastro, bg='LightGray', fg='Black', font=('Arial', 10, 'bold'))
        self.porta.place(relx=0.17, rely=0.15, relwidth=0.08)
        self.porta.bind("<Return>", self.porta_entry)

        self.senha = Entry(self.cadastro, bg='LightGray', fg='Black', font=('Arial', 10, 'bold'))
        self.senha.place(relx=0.17, rely=0.25, relwidth=0.3)
        self.senha.bind("<Return>", self.senha_entry)

        self.smtp = Entry(self.cadastro, bg='LightGray', fg='Black', font=('Arial', 10, 'bold'))
        self.smtp.place(relx=0.17, rely=0.35, relwidth=0.6)
        self.smtp.bind("<Return>", self.email_entry)

        self.email = Entry(self.cadastro, bg='LightGray', fg='Black', font=('Arial', 10, 'bold'))
        self.email.place(relx=0.17, rely=0.45, relwidth=0.6)
        self.email.bind("<Return>", lambda event: self.inserir_email())

        self.botao_adicionar = Button(self.cadastro, text='Salvar', command=self.inserir_email)
        self.botao_adicionar.place(relx=0.35, rely=0.15, relwidth=0.09, relheight=0.04)
        Button(self.cadastro, text='Excluir', command=self.excluir_email).place(relx=0.45, rely=0.15,
                                                                                relwidth=0.09, relheight=0.04)
        self.criar_tabela_emails(self.cadastro)
        self.mensagem_config()

    def criar_tabela_emails(self, janela):
        dados = banco_sqlite.busca_todos_emails_cadastrados()
        listaDados = Treeview(janela, height=3, columns=("col1", "col2", "col3", "col4"), show='headings')
        listaDados.heading("#0")
        listaDados.heading("#1", text="Código")
        listaDados.heading("#2", text="Porta")
        listaDados.heading("#3", text="SMTP")
        listaDados.heading("#4", text="E-mail")
        listaDados.column("#0", width=0)
        listaDados.column("#1", width=20)
        listaDados.column("#2", width=50)
        listaDados.column("#3", width=150)
        listaDados.column("#4", width=150)
        listaDados.place(relx=0.02, rely=0.53, relwidth=0.941, relheight=0.43)

        scrollbar = Scrollbar(janela, orient="vertical", command=listaDados.yview)
        scrollbar.place(relx=0.96, rely=0.533, relwidth=0.028, relheight=0.426)
        listaDados.configure(yscrollcommand=scrollbar.set)

        for i in dados:
            listaDados.insert("", "end", values=i)

        listaDados.bind("<Double-1>", self.duplo_click_email)
        self.listaDados = listaDados
        self.definir_estilo_treeview()

    def definir_estilo_treeview(self):
            style = Style()
            style.theme_use("default")
            style.map("Treeview")

    def porta_entry(self, event):
        self.senha.focus()

    def senha_entry(self, event):
        self.smtp.focus()

    def email_entry(self, event):
        self.email.focus()
    def buton_entry(self, event):
        self.botao_adicionar.focus()

    def inserir_email(self):
        banco_sqlite.insere_dados_email(int(self.porta.get()), self.smtp.get(), self.email.get(), self.senha.get())
        self.atualizar_tabela_emails()

    def atualizar_tabela_emails(self):
        dados = banco_sqlite.busca_todos_emails_cadastrados()
        self.listaDados.delete(*self.listaDados.get_children())

        for i in dados:
            self.listaDados.insert("", "end", values=i)

    def excluir_email(self):
        selected_item = self.listaDados.focus()
        item_details = self.listaDados.item(selected_item)
        item_lista = item_details.get("values")

        banco_sqlite.exclui_email_cadastrado(item_lista[0])
        self.atualizar_tabela_emails()

    def duplo_click_email(self, event):
        self.limpar_campos()
        item = self.listaDados.item(self.listaDados.selection())
        values = item['values']
        self.porta.insert(END, values[1])
        self.smtp.insert(END, values[2])
        self.email.insert(END, values[3])

    def limpar_campos(self):
        self.porta.delete(0, END)
        self.smtp.delete(0, END)
        self.email.delete(0, END)
        self.senha.delete(0, END)
        self.porta.focus()

    def mensagem_config(self):

        titulo = Label(self.mensagem, text='Título da Mensagem', bg='#B6C6D6')
        titulo.place(relx=0.03, rely=0.1)

        self.titulo = Entry(self.mensagem, bg='LightGray', fg='Black', font=('Arial', 11, 'bold'))
        self.titulo.place(relx=0.03, rely=0.15, relwidth=0.95)

        titulo = Label(self.mensagem, text='Mensagem', bg='#B6C6D6')
        titulo.place(relx=0.03, rely=0.25)

        self.texto = Text(self.mensagem, bg='LightGray', fg='Black', font=('Arial', 10))
        self.texto.place(relx=0.03, rely=0.3, relwidth=0.95, relheight=0.65)
        texto = self.texto.get("1.0", "end")

    def teste(self):
        return self.var_nao_envio

    def envio_mensagens(self):
        email_usuario = banco_sqlite.busca_todos_emails_cadastrados()
        print(email_usuario)
        cor = '#B6C6D6'
        compri = 600
        altura = 550
        x, y = pyautogui.position()
        y = y - 20
        print(x, y)

        self.envio_mens = Toplevel(self.root)

        self.envio_mens.focus_force()  #
        self.envio_mens.title('Avisos')
        self.envio_mens.transient(self.root)  #
        self.envio_mens.resizable(False, False)
        self.envio_mens.configure(background=f'{cor}')
        self.envio_mens.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))

        self.var_nao_envio = IntVar()
        self.checkbutton = Checkbutton(self.envio_mens, text="Avisar todos os Clientes", bg=f'{cor}',
                                       variable=self.var_nao_envio, onvalue=1)
        self.checkbutton.place(relx=0.5, rely=0.1)
        # Combo Box  --> Rece dados do banco e retorna ao grid da tela.
        itens = list()
        if len(email_usuario) > 0:
            for i in email_usuario:
                itens.append(i[3])

        self.comboExample = Combobox(self.envio_mens,  # -------------------> ComboBOX
                                     values=itens)
        if len(email_usuario) > 0:
            self.comboExample.current(0)
        self.comboExample.place(relx=0.2, rely=0.05)

        # Botão para enviar as mensagens
        Button(self.envio_mens, text='Extrair', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 12, 'bold'), command=self.insere_mensage).place(relx=0.4, rely=0.9, relwidth=0.1,
                                                                              relheight=0.06)

        # Labels para informar os assuntos da tela
        titulo = Label(self.envio_mens, text='Assunto', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.22)
        titulo = Label(self.envio_mens, text='Mensagem', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.36)
        titulo = Label(self.envio_mens, text='Para', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.12)

        # Entrys da Janela envios de Mensagens
        self.assunto = Entry(self.envio_mens, bg='LightGray', fg='Black')
        self.assunto.place(relx=0.03, rely=0.25, relwidth=0.95)
        self.remetente = Entry(self.envio_mens, bg='LightGray', fg='Black')
        self.remetente.place(relx=0.03, rely=0.15, relwidth=0.95)
        self.texto = Text(self.envio_mens, bg='LightGray', fg='Black')
        self.texto.place(relx=0.03, rely=0.4, relwidth=0.95, relheight=0.45)
        texto = self.texto.get("1.0", "end")

        self.envio_mens.mainloop()

    def insere_mensage(self):

        emailDados = self.comboExample.get()
        email = banco_sqlite.busca_todos_emails_cadastrados()
        self.dadosEnvio = [i for i in email if i[3] == emailDados]
        email = Email(self.dadosEnvio[0][3], self.dadosEnvio[0][2], self.dadosEnvio[0][1], self.dadosEnvio[0][4])

        print(self.assunto.get())
        print(self.remetente.get())
        print(self.texto.get("1.0", "end"))
        teste = self.texto.get("1.0", "end")
        email.envia_texto(f'{self.remetente.get()}', f'{self.assunto.get()}', f'{teste}')

    def envia_arquivos(self):
        email_usuario = banco_sqlite.busca_todos_emails_cadastrados()  # Busca as informações do e-mail com senha
        print(email_usuario)

        # self.email = Email('elibatiliere@gmail.com', 'smtp.gmail.com', 587, 'tqfwymvmdtngfczj')

        x, y = pyautogui.position()
        y = y - 20
        self.X = x
        self.Y = y
        cor = '#B6C6D6'
        compri = 600
        altura = 550

        style = Style()
        style.configure('TLabel', background=cor)
        style.configure('TCheckbutton', background=cor)
        style.configure('MeuEstilo.TButton', font=('Arial', 12, 'bold'), foreground='white', background='#4CAF50')

        self.envia_arquivo_janela = Toplevel(self.root)
        self.envia_arquivo_janela.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))
        self.envia_arquivo_janela.configure(background=f'{cor}')
        self.envia_arquivo_janela.title('Envios de Boletos')
        self.envia_arquivo_janela.transient(self.root)  #
        self.envia_arquivo_janela.focus_force()  #
        self.envia_arquivo_janela.resizable(False, False)

        # Cria widgets na janela
        self.var_nao_envio = IntVar()
        self.checkbutton = Checkbutton(
            self.envia_arquivo_janela,
            text="Avisar todos os Clientes",
            bg=cor,
            variable=self.var_nao_envio,
            onvalue=1
        )
        self.checkbutton.place(relx=0.6, rely=0.05)

        itens = [i[3] for i in email_usuario] if email_usuario else []
        self.comboExample = Combobox(
            self.envia_arquivo_janela,
            values=itens
        )
        if itens:
            self.comboExample.current(0)
        self.comboExample.place(relx=0.18, rely=0.05, relwidth=0.35)

        if len(email_usuario) > 0:
            self.comboExample.current(0)
        self.comboExample.place(relx=0.18, rely=0.05, relwidth=0.35)

        global dadosEmail
        try:
            for i in email_usuario:
                if i[3] == self.comboExample.get():
                    dadosEmail = i
        except Exception as e:
            mb.showwarning('Cadastros', f'{e}')

        # Faz o envio das notas para os e-mail dos clientes
        Label(self.envia_arquivo_janela, text='Extrair Notas', bg=f'{cor}').place(relx=0.03, rely=0.2)
        Label(self.envia_arquivo_janela, text='E-mail de envio', bg=f'{cor}').place(relx=0.03, rely=0.05)
        Label(self.envia_arquivo_janela, text='Local da NFS', bg=f'{cor}').place(relx=0.03, rely=0.15)

        # Botões para enviar os dados
        Button(self.envia_arquivo_janela, text='Buscar', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 7), command=self.local_arquivo_class).place(relx=0.82, rely=0.149, relwidth=0.06,
                                                                          relheight=0.04)
        Button(self.envia_arquivo_janela, text='Enviar', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 12, 'bold'), command=self.envios_notas).place(relx=0.4, rely=0.9, relwidth=0.1,
                                                                            relheight=0.06)
        Button(self.envia_arquivo_janela, text='Extrair', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 7), command=self.busca_diretorio_da_pasta).place(relx=0.82, rely=0.198, relwidth=0.06,
                                                                               relheight=0.04)

        # Entry para entrar dados
        self.extrai_arquivo = Entry(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.extrai_arquivo.place(relx=0.17, rely=0.2, relwidth=0.65)
        self.informa_extracao = Text(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.informa_extracao.place(relx=0.03, rely=0.4, relwidth=0.95, relheight=0.45)
        self.local_arquivo = Entry(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.local_arquivo.place(relx=0.17, rely=0.15, relwidth=0.65)

        self.envia_arquivo_janela.mainloop()

    def local_arquivo_class(self):
        local = diretorios.buscar_diretorio_do_arquivo()
        self.local_arquivo.insert(0, local)

    def busca_diretorio_da_pasta(self):
        local = diretorios.busca_diretorio_da_pasta()
        self.extrai_arquivo.insert(0, local)
        self.extrair_renomear_local_arquivo()

    def extrair_renomear_local_arquivo(self):
        local_arquivo = self.local_arquivo.get()
        local_pasta = self.extrai_arquivo.get()
        leitorPdf.extrai_arquivos_envio(str(local_arquivo), str(local_pasta))  # Extrair Páginas do PDF

        self.dados_completos = leitorPdf.extrai_dados_pdf(  # Busca todos os Diretórios dos arquivos
            diretorios.localiza_todos_arquivos_na_pasta(local_pasta))

        leitorPdf.renomeia_arquivos(local_pasta, self.dados_completos)
        self.informa_extracao.insert(END, 'Dados extraídos com sucesso!')
        self.envia_dados()

    def envia_dados(self):
        data_atual = date.today()
        data_em_texto = data_atual.strftime('%d/%m/%Y')

        for i in self.dados_completos:  # I[0] CNPJ, I[1] Razão, I[2] N°NFS, i[3] Chave NFS, I[4] Local da NFS
            try:
                codigo_email = banco_sqlite.busca_email_codigo_cadastro(i[0])
                "Codigo_email vai receber a informação do Código [0] e email [1] dos clientes cadastrados."
                if len(codigo_email[0]) > 1:
                    banco_sqlite.insere_dados_pdf(i[0], i[1], i[2], i[3], i[4], codigo_email[0][1],
                                                  codigo_email[0][0], data_em_texto)

                    print(i[0], i[1], i[2], i[3], i[4], codigo_email[0][1],
                          codigo_email[0][0], data_em_texto)

                else:
                    banco_sqlite.insere_dados_pdf(i[0], i[1], i[2], i[3], i[4], 'Não cadastrado',
                                                  0, data_em_texto)

            except Exception as e:
                print(f'Erro ao salvar dados: {e}')

    def envios_notas(self):
        # Criar janela de progresso
        self.teste = Toplevel(self.root)
        self.teste.geometry(f"300x100+{self.X}+{self.Y}")
        self.teste.transient(self.root)
        self.teste.focus_force()
        self.teste.resizable(False, False)
        self.centralizar_janelas(self.teste)

        # Adicionar rótulo
        Label(self.teste, text='Enviando notas', bg='white').place(relx=0.3, rely=0.01)

        # Buscar e armazenar dados do email selecionado
        emailDados = self.comboExample.get()
        email = banco_sqlite.busca_todos_emails_cadastrados()
        self.dadosEnvio = [i for i in email if i[3] == emailDados]

        # Enviar emails
        try:
            email = Email(self.dadosEnvio[0][3], self.dadosEnvio[0][2], self.dadosEnvio[0][1], self.dadosEnvio[0][4])
            dados_pdf = banco_sqlite.busca_dados_pdf()
            for i, dados in enumerate(dados_pdf):
                caminho = dados[4]
                e = str(dados[5])
                codigo = dados[6]
                data = dados[7]

                # Atualizar barra de progresso
                vt = i + 1
                inc = (vt / len(dados_pdf)) * 100
                self.progress = DoubleVar()
                self.progress.set(inc)
                self.progressBar = Progressbar(self.teste, maximum=100, orient=HORIZONTAL, variable=self.progress)
                self.progressBar.grid(column=3, row=8, columnspan=6, padx=20, pady=40)
                self.progressBar.place(rely=0.3, relwidth=0.99, relheight=0.2)
                self.teste.update_idletasks()

                # Enviar email
                email.envia_emails(dados[1] + '.PDF', str(caminho), e, 'Teste de envios', codigo, data, dados[0],
                                   dados[2])
                texto = Text(self.teste, bg='white', fg='Black', font=('Arial', 10))
                texto.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.3)
                texto.insert('end', dados[1])
                self.root.update()

                # Fechar janela de progresso
                if inc > 99.38:
                    self.teste.destroy()

        except Exception as e:
            print(e)

        self.teste.mainloop()

    # RELATÓRIO

    def dados_relatorio_enviado(self):

        cor = 'white'
        comprimento = 1000
        largura = 600
        self.relatorio_janela = Toplevel(self.root)
        x, y = pyautogui.position()
        y = y - 20
        x = x - 130
        print(x, y)
        self.relatorio_janela.geometry('{}x{}+{}+{}'.format(comprimento, largura, x, y))

        self.relatorio_janela.geometry("1000x600")
        self.relatorio_janela.configure(background=f'{cor}')
        # self.relatorio_janela.overrideredirect(True) # Faz com que a janela apareça dentro da outra
        self.relatorio_janela.title('Avisos')
        # self.relatorio_janela.transient(self.root)  #
        # self.relatorio_janela.focus_force()  #
        # novaTela.grab_set()  #
        # self.relatorio_janela.resizable(False, False)
        self.relatorio(self.relatorio_janela)
        self.relatorio_janela.mainloop()

    def criar_tabela(self, janela):
        tabela = Treeview(janela, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        tabela.heading("#0")
        tabela.heading("#1", text=" CNPJ/CPF", command=lambda: self.ordenar_tabela(tabela, 0, False))
        tabela.heading("#2", text="Razão Social", command=lambda: self.ordenar_tabela(tabela, 1, True))
        tabela.heading("#3", text="N° NFS", command=lambda: self.ordenar_tabela(tabela, 2, False))
        tabela.heading("#4", text="E-mail", command=lambda: self.ordenar_tabela(tabela, 3, False))
        tabela.heading("#5", text="NF-e", command=lambda: self.ordenar_tabela(tabela, 4, False))
        tabela.heading("#6", text="Status", command=lambda: self.ordenar_tabela(tabela, 5, False))
        tabela.column("#0", minwidth=0, width=0)
        tabela.column("#1", minwidth=70, width=90)
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

    def preencher_tabela(self, tabela, dados):
        tabela.delete(*tabela.get_children())
        for i in dados:
            tabela.insert("", END, values=i)

    def adicionar_barra_rolagem(self, janela, tabela):
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

    def buscar_dados(self):
        texto_pesquisa = self.pesquisa_entry.get()

        # Filtra os dados com base no texto digitado pelo usuário
        dados_filtrados = [dados for dados in banco_sqlite.busca_tabela_dados_de_evio() if
                           texto_pesquisa.lower() in dados[1].lower() or texto_pesquisa.lower() in dados[0].lower()
                           or texto_pesquisa.lower() in dados[4].lower()]

        # Ordena os dados e preenche a tabela com os resultados da busca
        dados_ordenados = self.ordenar_dados(dados_filtrados, 1)  # Ordena por razão social
        self.preencher_tabela(self.listaDadosRelatorio, dados_ordenados)

    def relatorio(self, janela):
        dados = banco_sqlite.busca_tabela_dados_de_evio()
        tabela = self.criar_tabela(janela)

        dados_ordenados = self.ordenar_dados(dados, 1)  # Ordena por razão social
        self.preencher_tabela(tabela, dados_ordenados)
        self.adicionar_barra_rolagem(janela, tabela)
        self.definir_estilo_tabela()
        self.dados_duplo = tabela
        self.listaDadosRelatorio = tabela
        self.dados_duplo = tabela
        self.listaDadosRelatorio = tabela
        self.pesquisa_entry = Entry(janela)
        self.pesquisa_entry.place(relx=0.001, rely=0.001, relwidth=0.8, height=25)
        self.pesquisa_entry.bind("<Return>", lambda event: self.buscar_dados())

        self.pesquisa_botao = Button(janela, text="Pesquisar", command=self.buscar_dados)
        self.pesquisa_botao.place(relx=0.81, rely=0.001, relwidth=0.19, height=25)

    def dados_relatorio_extraidos(self):

        cor = 'white'
        comprimento = 1000
        largura = 600
        self.relatorio_janela = Toplevel(self.root)
        x, y = pyautogui.position()
        y = y - 20
        x = x - 130
        print(x, y)
        self.relatorio_janela.geometry('{}x{}+{}+{}'.format(comprimento, largura, x, y))

        self.relatorio_janela.geometry("1000x600")
        self.relatorio_janela.configure(background=f'{cor}')
        # self.relatorio_janela.overrideredirect(True) # Faz com que a janela apareça dentro da outra
        self.relatorio_janela.title('Avisos')
        # self.relatorio_janela.transient(self.root)  #
        # self.relatorio_janela.focus_force()  #
        # novaTela.grab_set()  #
        # self.relatorio_janela.resizable(False, False)
        self.relatorio_dados_extraidos(self.relatorio_janela)
        self.relatorio_janela.mainloop()

    def criar_tabela_dados_extraidos(self, janela):
        colunas =["col1", "col2", "col3", "col4", "col5", "col6", 'col7','col8']

        tabela = Treeview(janela, height=3, column=colunas)
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
        tabela.place(relx=0.001, rely=0.05, relwidth=0.975, relheight=0.94)

        tabela.tag_configure("linha", background="white")

        return tabela

    def ordenar_tabela_dados(self, tabela, coluna, ascendente):
        dados = [(tabela.set(i, coluna), i) for i in tabela.get_children("")]
        dados.sort(reverse=not ascendente)
        for index, (val, k) in enumerate(dados):
            tabela.move(k, '', index)
        tabela.heading("#" + str(coluna), command=lambda: self.ordenar_tabela_dados(tabela, coluna, not ascendente))

    def preencher_tabela_dados(self, tabela, dados):
        tabela.delete(*tabela.get_children())
        for i in dados:
            tabela.insert("", END, values=i)

    def adicionar_barra_rolagem_dados(self, janela, tabela):
        scrollbar = Scrollbar(janela, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scrollbar.place(relx=0.981, rely=0.05, relwidth=0.015, relheight=0.926)

    def definir_estilo_tabela_dados(self):
        style = Style()
        style.theme_use("default")
        style.map("Treeview")

    """def ordenar_coluna(self, tabela, coluna, ordem='crescente'):
        # Obtém os dados da tabela como uma lista de tuplas
        dados = [(tabela.set(id_, coluna), id_) for id_ in tabela.get_children('')]

        # Ordena os dados
        dados.sort(reverse=(ordem == 'decrescente'))

        # Reorganiza as linhas da tabela com base nos dados ordenados
        for index, (valor, id_) in enumerate(dados):
            tabela.move(id_, '', index)
            tabela.item(id_, values=tuple(valor))"""

    def ordenar_dados_extraidos(self, dados, coluna):
        """
        Ordena os dados de acordo com a coluna selecionada.
        """
        return sorted(dados, key=lambda x: x[coluna])

    def buscar_dados_extraidos(self):
        texto_pesquisa = self.pesquisa_entry.get()

        # Filtra os dados com base no texto digitado pelo usuário
        dados_filtrados = [dados for dados in banco_sqlite.busca_dados_pdf() if
                           texto_pesquisa.lower() in dados[1].lower() or texto_pesquisa.lower() in dados[0].lower()
                           or texto_pesquisa.lower() in dados[4].lower()]

        # Ordena os dados e preenche a tabela com os resultados da busca
        dados_ordenados = self.ordenar_dados_extraidos(dados_filtrados, 1)  # Ordena por razão social
        self.preencher_tabela_dados(self.listaDadosRelatorio, dados_ordenados)

    def relatorio_dados_extraidos(self, janela):
        dados = banco_sqlite.busca_dados_pdf()
        tabela = self.criar_tabela_dados_extraidos(janela)

        dados_ordenados = self.ordenar_dados_extraidos(dados, 1)  # Ordena por razão social
        self.preencher_tabela_dados(tabela, dados_ordenados)
        self.adicionar_barra_rolagem_dados(janela, tabela)
        self.definir_estilo_tabela_dados()
        self.dados_duplo = tabela
        self.listaDadosRelatorio = tabela
        self.dados_duplo = tabela
        self.listaDadosRelatorio = tabela
        self.pesquisa_entry = Entry(janela)
        self.pesquisa_entry.place(relx=0.001, rely=0.001, relwidth=0.8, height=25)
        self.pesquisa_entry.bind("<Return>", lambda event: self.buscar_dados_extraidos())

        self.pesquisa_botao = Button(janela, text="Pesquisar", command=self.buscar_dados_extraidos)
        self.pesquisa_botao.place(relx=0.81, rely=0.001, relwidth=0.19, height=25)




if __name__ == '__main__':
    interface = Interface()