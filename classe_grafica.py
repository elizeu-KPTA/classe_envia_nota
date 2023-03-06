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
        """self._geom = '200x200+0+0'
        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad))
        self.root.bind('<Escape>', self.tamanho_tela)"""

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
        relatorio.add_command(label="Dados Extraidos", command=self.dados_relatorio)
        relatorio.add_command(label="E-mails enviados", command=self.donothing)
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
        scrollbar = Scrollbar(janela)
        listaDados = Treeview(janela, height=3,
                              column=("col1", "col2", "col3", "col4"), yscrollcommand=scrollbar.set)
        listaDados.heading("#0", text="")
        listaDados.heading("#1", text="Código")
        listaDados.heading("#2", text="Nome")
        listaDados.heading("#3", text="E-mail")
        listaDados.heading("#4", text="CNPJ")
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

        Button(self.cadastro, text='Salvar', command=self.insere_config_mail).place(relx=0.35, rely=0.15,
                                                                                    relwidth=0.09, relheight=0.04)
        Button(self.cadastro, text='Excluir', command=self.mostra_selecao).place(relx=0.45, rely=0.15,
                                                                                 relwidth=0.09, relheight=0.04)
        self.dados_cad_email(self.cadastro)
        self.mensagem_config()

    def dados_cad_email(self, janela):  # Criação da tabela de cadastro.
        dados = banco_sqlite.busca_todos_emails_cadastrados()
        scrollbar = Scrollbar(janela)
        listaDados = Treeview(janela, height=3,
                              column=("col1", "col2", "col3", "col4"), yscrollcommand=scrollbar.set)
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
        scrollbar.pack(side="right", fill="y")  # Criação da barra de rolagem.
        scrollbar.config(command=listaDados.yview)
        scrollbar.place(relx=0.96, rely=0.533, relwidth=0.028, relheight=0.426)
        listaDados.delete(*listaDados.get_children())

        for i in dados:
            print(i)
            listaDados.insert("", END, values=i)

        self.dados_duplo = listaDados
        listaDados.bind("<Double-1>", self.duplo_click_email)  # busca a função para inserir dados.
        self.listaDados = listaDados

    def porta_entry(self, tecla):
        self.senha.focus()

    def senha_entry(self, tecla):
        self.smtp.focus()

    def email_entry(self, tecla):
        self.email.focus()

    def insere_config_mail(self):
        banco_sqlite.insere_dados_email(int(self.porta.get()),
                                        self.smtp.get(), self.email.get(), self.senha.get())

        self.dados_cad_email(self.cadastro)

    def mostra_selecao(self):  # EXCLUI OS DADOS DO E-MAIL   ----->>> RECEBE A POSIÇÃO SELECIONADA NA LISTA DE DADOS
        #  selected_item = self.listaDados.selection()

        selected_item = self.listaDados.focus()
        item_details = self.listaDados.item(selected_item)
        item_lista = item_details.get("values")
        print(item_lista)

        banco_sqlite.exclui_email_cadastrado(item_lista[0])
        self.dados_cad_email(self.cadastro)

    def duplo_click_email(self, event):  # Método será chamado ao clicar duas vezes sobre a tabela.
        self.dados_duplo.selection()
        self.limpa_dados_cad_email()
        for n in self.dados_duplo.selection():
            col1, col2, col3, col4 = self.dados_duplo.item(n, 'values')
            self.porta.insert(END, col2)
            self.smtp.insert(END, col3)
            self.email.insert(END, col4)

    def limpa_dados_cad_email(self):
        self.porta.delete(0, END)
        self.smtp.delete(0, END)
        self.email.delete(0, END)

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

    #  Configuração do menu Envio

    def envio_notas(self):
        pass

    def teste(self):
        return self.var_nao_envio

    def envio_mensagens(self):
        email_usuario = banco_sqlite.busca_todos_emails_cadastrados()
        print(email_usuario)
        cor = '#B6C6D6'
        compri = 600
        altura = 550
        self.envio_mens = Toplevel(self.root)
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

        Button(self.envio_mens, text='Extrair', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 12, 'bold'), command=self.insere_mensage).place(
            relx=0.4,
            rely=0.9,
            relwidth=0.1,
            relheight=0.06)

        titulo = Label(self.envio_mens, text='Para', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.12)

        self.remetente = Entry(self.envio_mens, bg='LightGray', fg='Black')
        self.remetente.place(relx=0.03, rely=0.15, relwidth=0.95)

        titulo = Label(self.envio_mens, text='Assunto', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.22)

        self.assunto = Entry(self.envio_mens, bg='LightGray', fg='Black')
        self.assunto.place(relx=0.03, rely=0.25, relwidth=0.95)

        titulo = Label(self.envio_mens, text='Mensagem', bg=f'{cor}')
        titulo.place(relx=0.03, rely=0.36)

        self.texto = Text(self.envio_mens, bg='LightGray', fg='Black')
        self.texto.place(relx=0.03, rely=0.4, relwidth=0.95, relheight=0.45)
        texto = self.texto.get("1.0", "end")

        x, y = pyautogui.position()
        y = y - 20
        print(x, y)
        self.envio_mens.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))
        self.envio_mens.configure(background=f'{cor}')
        #  novaTela.overrideredirect(False) # Faz com que a janela apareça dentro da outra
        self.envio_mens.title('Avisos')
        self.envio_mens.transient(self.root)  #
        self.envio_mens.focus_force()  #
        # novaTela.grab_set()  #
        self.envio_mens.resizable(False, False)
        self.envio_mens.mainloop()

    def insere_mensage(self):

        email = Email('elibatiliere@gmail.com', 'smtp.gmail.com', 587, 'tqfwymvmdtngfczj')

        print(self.assunto.get())
        print(self.remetente.get())
        print(self.texto.get("1.0", "end"))
        teste = self.texto.get("1.0", "end")

        email.envia_texto(f'{self.remetente.get()}', f'{self.assunto.get()}', f'{teste}')

    def envia_arquivos(self):
        email_usuario = banco_sqlite.busca_todos_emails_cadastrados()  # Busca as informações do e-mail com senha

        cor = '#B6C6D6'
        compri = 600
        altura = 550
        self.envia_arquivo_janela = Toplevel(self.root)

        self.var_nao_envio = IntVar()

        self.checkbutton = Checkbutton(self.envia_arquivo_janela, text="Avisar todos os Clientes", bg=f'{cor}',
                                       variable=self.var_nao_envio, onvalue=1)
        self.checkbutton.place(relx=0.6, rely=0.05)

        # Combo Box  --> Rece dados do banco e retorna ao grid da tela.

        itens = list()
        if len(email_usuario) > 0:
            for i in email_usuario:
                itens.append(i[3])
        Label(self.envia_arquivo_janela, text='E-mail de envio', bg=f'{cor}').place(relx=0.03, rely=0.05)

        self.comboExample = Combobox(self.envia_arquivo_janela,  # -------------------> ComboBOX
                                     values=itens)
        if len(email_usuario) > 0:
            self.comboExample.current(0)
        self.comboExample.place(relx=0.18, rely=0.05, relwidth=0.35)
        print('teste', self.comboExample.get())

        global dadosEmail
        try:
            for i in email_usuario:
                if i[3] == self.comboExample.get():
                    dadosEmail = i
        except Exception as e:
            mb.showwarning('Cadastros', f'{e}')

        self.email = Email('elibatiliere@gmail.com', 'smtp.gmail.com', 587, 'tqfwymvmdtngfczj')

        # Faz o envio das notas para os e-mail dos clientes
        Button(self.envia_arquivo_janela, text='Enviar', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 12, 'bold'), command=self.envios_notas).place(
            relx=0.4,
            rely=0.9,
            relwidth=0.1,
            relheight=0.06)

        Label(self.envia_arquivo_janela, text='Local da NFS', bg=f'{cor}').place(relx=0.03, rely=0.15)

        self.local_arquivo = Entry(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.local_arquivo.place(relx=0.17, rely=0.15, relwidth=0.65)

        Button(self.envia_arquivo_janela, text='Buscar', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 7), command=self.local_arquivo_class).place(
            relx=0.82,
            rely=0.149,
            relwidth=0.06,
            relheight=0.04)

        Label(self.envia_arquivo_janela, text='Extrair Notas', bg=f'{cor}').place(relx=0.03, rely=0.2)

        self.extrai_arquivo = Entry(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.extrai_arquivo.place(relx=0.17, rely=0.2, relwidth=0.65)

        Button(self.envia_arquivo_janela, text='Extrair', fg='Black', bg=f'#FFFFFF',
               font=('Arial', 7), command=self.busca_diretorio_da_pasta).place(
            relx=0.82,
            rely=0.198,
            relwidth=0.06,
            relheight=0.04)

        self.informa_extracao = Text(self.envia_arquivo_janela, bg='LightGray', fg='Black')
        self.informa_extracao.place(relx=0.03, rely=0.4, relwidth=0.95, relheight=0.45)
        texto = self.informa_extracao.get("1.0", "end")

        x, y = pyautogui.position()
        y = y - 20
        self.X =x
        self.Y = y

        self.envia_arquivo_janela.geometry('{}x{}+{}+{}'.format(compri, altura, x, y))
        self.envia_arquivo_janela.configure(background=f'{cor}')
        #  novaTela.overrideredirect(False) # Faz com que a janela apareça dentro da outra
        self.envia_arquivo_janela.title('Envios de Boletos')
        self.envia_arquivo_janela.transient(self.root)  #
        self.envia_arquivo_janela.focus_force()  #
        # novaTela.grab_set()  #
        self.envia_arquivo_janela.resizable(False, False)
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
                    banco_sqlite.insere_dados_pdf(i[0], i[1], i[2], i[3], i[4], 'Não cadastrado!',
                                                  0, data_em_texto)

            except Exception as e:
                print(f'Erro ao salvar dados: {e}')



    def envios_notas(self):
        self.teste = Toplevel(self.root)
        self.teste.geometry(f"300x100+{self.X}+{self.Y}")
        self.teste.transient(self.root)  #
        self.teste.focus_force()  # Não deixa a principal sobrepor
        # self.teste.grab_set()  # Não deixa selecionar outra tela
        # self.teste.winfo_screenwidth() #
        # self.teste.winfo_screenheight() #
        self.teste.resizable(False, False)
        self.centralizar_janelas(self.teste)
        t = Label(self.teste, text='Enviando notas', bg='white')
        t.place(relx=0.3, rely=0.01)
        emailDados = self.comboExample.get()
        email = banco_sqlite.busca_todos_emails_cadastrados()

        if len(email) > 0:
            for i in email:
                if i[3] == emailDados:
                    self.dadosEnvio.append(i)

        try:
            vt = 0
            email = Email(self.dadosEnvio[0][3], self.dadosEnvio[0][2], self.dadosEnvio[0][1], self.dadosEnvio[0][4])
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
                print(self.dadosEnvio)
                self.teste.update_idletasks()
                self.progress.set(100)

                email.envia_emails(i[1] + '.PDF', str(caminho), e, 'Teste de envios', codigo, data)
                dados = i[1]

                texto = Text(self.teste, bg='white', fg='Black', font=('Arial', 10))
                texto.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.3)
                texto.insert('end',dados)
                self.root.update()
                vt += 1
                if inc > 99.38:
                    self.teste.destroy()

        except Exception as e:
            print(e)
        self.teste.mainloop()






    # RELATÓRIO

    def dados_relatorio(self):

        cor = 'white'
        comprimento = 900
        largura = 600
        self.relatorio_janela = Toplevel(self.root)
        x, y = pyautogui.position()
        y = y - 20
        print(x, y)
        self.relatorio_janela.geometry('{}x{}+{}+{}'.format(comprimento, largura, x, y))
        self.relatorio_janela.configure(background=f'{cor}')
        #  novaTela.overrideredirect(False) # Faz com que a janela apareça dentro da outra
        self.relatorio_janela.title('Avisos')
        self.relatorio_janela.transient(self.root)  #
        self.relatorio_janela.focus_force()  #
        # novaTela.grab_set()  #
        self.relatorio_janela.resizable(False, False)

        self.frames_relatorio()
        self.relatorio_janela.mainloop()

    def frames_relatorio(self):
        self.frame_relatorio = Frame(self.relatorio_janela, bd=4, bg='LightGray',
                                     highlightbackground="LightGray")
        self.frame_relatorio.place(relx=0.01, rely=0.01, relwidth=0.99, relheight=0.95)
        self.relatorio(self.frame_relatorio)

    def relatorio(self, janela):  # Criação da tabela de cadastro.
        dados = banco_sqlite.busca_todos_emails_cadastrados()
        scrollbar = Scrollbar(janela)
        listaDados = Treeview(janela, height=3,
                              column=("col1", "col2", "col3", "col4","col5", "col6"), yscrollcommand=scrollbar.set)
        listaDados.heading("#0")
        listaDados.heading("#1", text=" CNPJ/CPF")
        listaDados.heading("#2", text="Número NFS")
        listaDados.heading("#3", text="Razão Social")
        listaDados.heading("#4", text="E-mail")
        listaDados.heading("#5", text="NF-e")
        listaDados.heading("#6", text="Status")
        listaDados.column("#0", width=0)
        listaDados.column("#1", width=20)
        listaDados.column("#2", width=50)
        listaDados.column("#3", width=150)
        listaDados.column("#4", width=150)
        listaDados.column("#5", width=150)
        listaDados.column("#6", width=150)
        listaDados.place(relx=0.02, rely=0.53, relwidth=0.941, relheight=0.43)
        scrollbar.pack(side="right", fill="y")  # Criação da barra de rolagem.
        scrollbar.config(command=listaDados.yview)
        scrollbar.place(relx=0.96, rely=0.533, relwidth=0.028, relheight=0.426)
        listaDados.delete(*listaDados.get_children())

        for i in dados:
            print(i)
            listaDados.insert("", END, values=i)

        self.dados_duplo = listaDados
        listaDados.bind("<Double-1>", self.duplo_click_email)  # busca a função para inserir dados.
        self.listaDados = listaDados

    """ def porta_entry(self, tecla):
        self.senha.focus()

    def senha_entry(self, tecla):
        self.smtp.focus()

    def email_entry(self, tecla):
        self.email.focus()

    def insere_config_mail(self):
        banco_sqlite.insere_dados_email(int(self.porta.get()),
                                        self.smtp.get(), self.email.get(), self.senha.get())

        self.dados_cad_email(self.cadastro)

    def mostra_selecao(self):  # EXCLUI OS DADOS DO E-MAIL   ----->>> RECEBE A POSIÇÃO SELECIONADA NA LISTA DE DADOS
        #  selected_item = self.listaDados.selection()

        selected_item = self.listaDados.focus()
        item_details = self.listaDados.item(selected_item)
        item_lista = item_details.get("values")
        print(item_lista)

        banco_sqlite.exclui_email_cadastrado(item_lista[0])
        self.dados_cad_email(self.cadastro)

    def duplo_click_email(self, event):  # Método será chamado ao clicar duas vezes sobre a tabela.
        self.dados_duplo.selection()
        self.limpa_dados_cad_email()
        for n in self.dados_duplo.selection():
            col1, col2, col3, col4 = self.dados_duplo.item(n, 'values')
            self.porta.insert(END, col2)
            self.smtp.insert(END, col3)
            self.email.insert(END, col4)

    def limpa_dados_cad_email(self):
        self.porta.delete(0, END)
        self.smtp.delete(0, END)
        self.email.delete(0, END)
    """


    def relatorio_dados(self):

        self.scrollbar = Scrollbar(self.frame_relatorio)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = Listbox(self.frame_relatorio, selectmode="multiple", width=95,
                               yscrollcommand=self.scrollbar.set)
        self.listbox.insert("end", "")

        if 0 == 0:
            dados = banco_sqlite.busca_dados_pdf()
            var = 11
            self.listbox.insert("end", "  ", "                                   "
                                             "                                 INFORMAÇÃO SOBRE A NOTA", '', '')
            if len(dados) == 0:
                self.listbox.insert("end", "  ", "                                   "
                                                 "                               Não há dados a serem exibidos", '', '')

            for i in range(len(dados)):
                if 1 == 1:
                    self.listbox.insert("end",
                                        '_______________________________________________________________________' * 2,
                                        '')
                    print(f"     Status:{dados[i][5]}")
                    self.listbox.insert("end",
                                        f"              CNPJ/CPF: {dados[i][0]} "
                                        f"              Número NFS: {dados[i][2]}",
                                        " ",
                                        f"              Razão Social: {dados[i][1]}",
                                        " ",
                                        f"              E-mail: {dados[i][5]}   "
                                        f"  Data: {dados[i][7]}", "")

                    # self.listbox.itemconfig(var, fg="green")
                    var += 10

        self.listbox.pack(side="left", fill="both")
        self.scrollbar.config(command=self.listbox.yview)


interface = Interface()
