import sqlite3
from tkinter import messagebox as mb


class Banco_sqlite:
    def __init__(self):
        self.conexao = sqlite3.connect('emails.db')
        self.cursor = self.conexao.cursor()
        self.create_table_cadastro()
        self.create_table_envios_emails()
        self.create_table_email_config()
        self.create_table_dados_pdf()
        self.create_table_envios()
        self.create_mens()

    def create_table_cadastro(self):
        self.conexao.execute("""CREATE TABLE IF NOT EXISTS cadastro(
                codigo INTEGER PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email varchar(100) not null,
                cpf_cnpj varchar(21) UNIQUE
                );""")
        self.conexao.commit()

    def create_table_dados_pdf(self):
        self.conexao.execute(""" CREATE TABLE IF NOT EXISTS "dados_pdf" (
                "cnpj"	varchar(18),
                "razao_social"	varchar(120),
                "numero_nfe"	INTEGER UNIQUE,
                "cod_verificacao"	varchar(45) UNIQUE,
                "local_arquivo"	TEXT,
                "email_cliente"	TEXT,
                "cod_client"	INTEGER,
                "data_env"	TEXT 
                );""")
        self.conexao.commit()

    def create_table_envios_emails(self):
        self.conexao.execute("""CREATE TABLE IF NOT EXISTS envia_email(
                        codigo integer primary key,
                        email_env varchar(100),
                        data_env TEXT,
                        status varchar(16));""")
        self.conexao.commit()

    def create_table_email_config(self):
        self.conexao.execute("""CREATE TABLE IF NOT EXISTS usuarioEmail(
                id INTEGER PRIMARY KEY,
                porta INTEGER,
                SMTP CHAR(40) NOT NULL,
                email CHAR(40) NOT NULL,
                senha CHAR(40) NOT NULL
                );""")
        self.conexao.commit()

    def create_mens(self):
        self.conexao.execute("""CREATE TABLE IF NOT EXISTS mensEmail(
                titulo VARCHAR(50),
                texto VARCHAR(250)
                );""")
        self.conexao.commit()

    def create_table_envios(self):
        self.conexao.execute(""" CREATE TABLE IF NOT EXISTS "envioDados" (
                "cnpj"	varchar(18),
                "razao_social"	varchar(120),
                "numero_nfe",
                "email_cliente"	TEXT,
                "data_env"	TEXT,
                "status"	TEXT);""")
        self.conexao.commit()

    def insere_cadastro(self, codigo, nome, email, cpf_cnpj):
        if str(codigo).isnumeric():
            try:
                self.conexao.execute("INSERT INTO cadastro (codigo, nome, email, cpf_cnpj) "
                                     "VALUES(?, ?, ?, ?)",
                                     (codigo, nome, email, cpf_cnpj))
                self.conexao.commit()
            except:
                return 'Dados ja existe'
        else:
            mb.showwarning("Alerta!", "Código informado deve ser um número inteiro!")

    def insere_dados_email(self, porta, smtp, email, senha_email):
        dados = list()
        valDados = 1
        query = self.conexao.execute("""SELECT id FROM usuarioEmail""")
        for i in query:
            dados.append(i)
        while True:
            if valDados not in dados:
                print(valDados)
                if str(porta).isnumeric():
                    try:
                        self.conexao.execute("INSERT INTO usuarioEmail (id,porta, SMTP, email, senha) VALUES(?, ?,"
                                             "?, ?, ?)",
                                             (valDados, porta, smtp, email, senha_email))
                        self.conexao.commit()
                        mb.showinfo("Cadastrado!", "E-mail cadastrado com sucesso!")
                        break
                    except:
                        print('Chave duplicada!')
                    valDados += 1
                else:
                    return mb.showerror("Erro", "Erro ao inserir e-mail!!")
            else:
                valDados += 1

    def insere_dados_enviados(self, codigo, email_env, data_env, status):
        if str(codigo).isnumeric():
            try:
                self.conexao.execute("INSERT INTO envia_email (codigo, email_env,data_env, status) VALUES(?, ?, ?, ?)",
                                     (codigo, email_env, data_env, status))
                self.conexao.commit()
                return 'Cadastro realizado com sucesso! Mulinhaa'
            except:
                return 'Erro ao cadastrar!'
        else:
            return "Erro ao cadastar dados!"

    def insere_tabela_envios(self, cnpj, razao_social, numero_nfe, email_cliente, data_env, status):
        try:
            self.conexao.execute("INSERT INTO envioDados (cnpj, razao_social, numero_nfe, email_cliente, "
                                 "data_env, status) VALUES(?,?,?,?,?,?)",
                                 (cnpj, razao_social, numero_nfe, email_cliente, data_env, status))
            self.conexao.commit()
            return 'Cadastro realizado com sucesso!'
        except Exception as e:
            return f'Erro ao cadastrar!{e}'


    def insere_mensg_email(self, titulo, texto):
        res = mb.askokcancel("Cadastrar",
                             "Verifique se já tem uma mensagem cadastrada, caso tiver, clique em 'CANCELAR'"
                             " após clique em 'ALTERAR'!")
        if res == True:
            try:
                self.conexao.execute("INSERT INTO mensEmail (titulo,texto) VALUES(?,?)",
                                     (titulo, texto))
                self.conexao.commit()
                mb.showinfo("Cadastrado!", "E-mail cadastrado com sucesso!")
            except:
                return mb.showwarning("Alerta!", "Já existe uma mensagem semelhante cadastrada no banco de dados!")

    def insere_dados_pdf(self, cnpj, razao_social, numero_nfe, cod_verificacao, local_arquivo, email_cliente,
                         cod_cliente, data_env):
        self.conexao.execute("INSERT INTO dados_pdf (cnpj, razao_social,numero_nfe,cod_verificacao,"
                             "local_arquivo,email_cliente,cod_client,data_env) VALUES(?,?,?,?,?,?,?,?)",
                             (cnpj, razao_social, numero_nfe, cod_verificacao, local_arquivo, email_cliente,
                              cod_cliente, data_env))

        self.conexao.commit()
        # self.conexao.close()

    def busca_todos_os_dados_cadastro(self):
        dados = self.conexao.execute("""SELECT * FROM cadastro;""")
        dados_banco = list()
        for i in dados:
            dados_banco.append(i)
        return dados_banco


    def busca_dados_eviados(self):
        dados = self.conexao.execute("""SELECT * FROM envia_email;""")
        dados_banco = list()
        for i in dados:
            dados_banco.append(i)
        return dados_banco

    def busca_email_codigo_cadastro(self, cpf_cnpj):
        print(cpf_cnpj)
        query = self.conexao.execute("""SELECT codigo, email FROM cadastro where  cpf_cnpj  = ? """, (cpf_cnpj,))
        dados = list()
        for i in query:
            dados.append(i)
        if len(dados) < 1:
            dados = [[]]
            dados[0].insert(0, 'Nada')
        return dados

    def busca_todos_os_dados_enviados(self):
        query = self.conexao.execute("""SELECT c.codigo, c.nome, c.email, c.cpf_cnpj, ev.data_env, ev.status FROM 
                    cadastro as c, envia_email as ev where c.codigo = ev.codigo ;""")
        dados = list()
        for i in query:
            dados.append(i)
        return dados

    def retorna_dados_com_envia_dados(self, cpf_cnpj):
        query = self.conexao.execute("""SELECT c.codigo, c.nome, c.email, c.cpf_cnpj, ev.data_env, ev.status 
        FROM cadastro as c, envia_email as ev
                    where c.codigo in (select codigo from envia_email) and c.cpf_cnpj = ?;""", (cpf_cnpj,))
        dados = list()
        for i in query:
            dados.append(i)
        return dados

    def busca_dados_nao_enviados(self):
        query = self.conexao.execute("""SELECT c.codigo, c.nome, c.email, c.cpf_cnpj
                    FROM cadastro as c where c.codigo not in (select codigo from envia_email); """)
        dados = list()
        for i in query:
            dados.append(i)
        return dados

    def busca_nome_empresa_pelo_codigo(self, codigo):

        query = self.conexao.execute("""SELECT nome FROM cadastro 
                                        where codigo = ?""", (codigo,))
        dados = list()
        for i in query:
            dados.append(i)
        return dados
    def busca_tabela_dados_de_evio(self):

        query = self.conexao.execute("""SELECT * FROM envioDados; """)
        dados = list()
        for i in query:
            dados.append(i)
        return dados

    def busca_todos_emails_cadastrados(self):
        query = self.conexao.execute("""SELECT id, porta, SMTP, email, senha FROM usuarioEmail;""")
        dados_usuario = list()
        for i in query:
            dados_usuario.append(i)
        return dados_usuario



    def busca_dados_pdf(self):
        dados_pdf = list()
        query = self.conexao.execute("""SELECT *FROM dados_pdf;""")

        for i in query:
            dados_pdf.append(i)
        return dados_pdf

    def atualiza_dados_cadastro(self, nome, email, cpf_cnpj, codigo):
        resp = mb.askquestion("Atualizar", "Realmente deseja atualizar o cadastro!")
        if resp == 'yes':
            try:
                self.conexao.execute("""
                                    UPDATE
                                    cadastro
                                    SET nome = ?, email = ?,cpf_cnpj = ? where codigo = ?""",
                                     (nome, email, cpf_cnpj, codigo))
                self.conexao.commit()
            except:
                mb.showwarning("Alerta!", "Ocorreu um erro durante a alteração!!")

    def exclui_dados_cadastro(self, codigo):
        resp = mb.askquestion("Excluir arquivo!", "Realmente deseja excluir esse cadastro?")
        if resp != 'no':
            if str(codigo).isnumeric():
                self.conexao.execute("""
                   DELETE FROM cadastro
                   WHERE codigo = ?
                   """, (codigo,))
                self.conexao.commit()

    def exclui_dados_pdf(self):
        resp = mb.askquestion("Excluir arquivo!", "Deseja excluir todos os dados do PDF?")
        if resp != 'no':
                self.conexao.execute("""
                   DELETE FROM dados_pdf;
                   """)
                self.conexao.commit()

    def exclui_tabela_de_envio(self):
        resp = mb.askquestion("Excluir arquivo!", "Deseja excluir todos os dados do PDF?")
        if resp != 'no':
                self.conexao.execute("""
                   DELETE FROM envioDados;
                   """)
                self.conexao.commit()


    def exclui_email_cadastrado(self, codigo):
        resp = mb.askquestion("Excluir arquivo!", "Realmente deseja excluir esses E-mail?")
        if resp != 'no':
            if str(codigo).isnumeric():
                self.conexao.execute("""
                   DELETE FROM usuarioEmail
                   WHERE id = ?
                   """, (codigo,))
                self.conexao.commit()
            else:
                mb.showwarning("Alerta!", "O código informado está incorreto!")
        else:
            mb.showwarning("Cancelado!", "Exclusão cancelada!")


teste = Banco_sqlite()

"""print(teste.busca_dados_pdf())

print(teste.busca_email_codigo_cadastro('29.171.183/0001-90'))"""

# teste.exclui_dados_pdf()


# print(teste.insere_tabela_envios('056457527205','elizeu batiliere',589,'elibatiliere','25-05-2022', 'enviado'))

# print(teste.busca_tabela_dados_de_evio())

# teste.exclui_tabela_de_envio()
# teste.exclui_dados_pdf()
