import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from banco_sqlite import Banco_sqlite

banco_sqlite = Banco_sqlite()

"""
Classe de correio eletronico, busca o local do arquivo pra enviar ou apenas envia mensagens.

Elizeu Batiliere Dos Santos 23-01-2023 UTF-8 bom
"""

# tqfwymvmdtngfczj


class Email:
    def __init__(self, email_p_envio, smtp_ep_envio, port_envio, senha_email):  # e-mail que vai enviar as notas
        self.email_p_envio = email_p_envio
        self.smtp_ep_envio = smtp_ep_envio
        self.port_envio = port_envio
        self.__senha_email = senha_email

    def envia_emails(self, nome_aruivo, caminho_arquivo, email, msg_arquivo
                     , codigo, data):  # Endereço eletrónico e arquivos que
        # serão enviados
        try:
            fromaddr = self.email_p_envio
            toaddr = str(email)
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = str(msg_arquivo)
            body = str('teste de envio')
            msg.attach(MIMEText(body, 'plain'))
            filename = str(nome_aruivo)
            attachment = open(str(caminho_arquivo), 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
            attachment.close()
            server = smtplib.SMTP(self.smtp_ep_envio, self.port_envio)  # porta
            server.starttls()
            server.login(fromaddr, self.__senha_email)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print('\nEmail e anexos enviado com sucesso!')
            banco_sqlite.insere_dados_enviados(codigo, email, data, 'Enviado')

        except Exception as e:
            print(e)
            banco_sqlite.insere_dados_enviados(codigo, email, data, 'Falha ao enviar')

    def envia_texto(self, email_rec, titulo, mensagem):
        smtp_ssl_host = self.smtp_ep_envio
        smtp_ssl_port = 465

        username = self.email_p_envio
        password = self.__senha_email

        from_addr = self.email_p_envio
        to_addrs = [email_rec]

        message = MIMEText(mensagem)
        message['subject'] = titulo
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()
        print('Mensagem enviada com sucesso')
