"""
Classe que extrai e lê dados de PDF, retornando os resultados.
Desenvolvida por ELizeu Batiliere dia 22/01/2023 UTF8-BOM
"""


from PyPDF2 import PdfFileReader, PdfFileWriter
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from tkinter.ttk import *
from tkinter import *
import os



class LeitorPDF:
    def __init__(self):
        pass

    def extrai_arquivos_envio(self, caminho_arquivo, local_salvar):
        """
        :param caminho_arquivo: busca o PDF do faturamento.
        :param local_salvar: localiza a pasta para extrair:return: extrai as informações na pasta.
        """
        busca = PdfFileReader(open(caminho_arquivo, "rb"))
        for i in range(busca.numPages):
            saida = PdfFileWriter()
            saida.addPage(busca.getPage(i))
            with open(local_salvar + r"\Faturamento-SCI-%s.pdf" % i, "wb") as outputStream:
                saida.write(outputStream)

    def __extrai_pagenas_pdf(self, caminho_pdf):
        """
        :param caminho_pdf: busca o caminho do arquivo:return: retorna os dados extraidos.
        """
        with open(caminho_pdf, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager,
                                      fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager,
                                                  converter)
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()  # extrai as informações do arquivo pdf para o texto
        yield text
        converter.close()

    def _extrai_p(self, caminho_pdf):

        for page in self.__extrai_pagenas_pdf(caminho_pdf):  # Recebe o local do arquivo pdf
            return page

    def extrai_dados_pdf(self, caminho_arquivos):
        """
        :param caminho_arquivos: recebe o diretório as NFS.
        Return: retorna o CNPJ, Razão Social, Número da NFS, código de verificação, diretório do arquivo.
        """
        dados_completos = list()
        try:
            self.teste = Tk()
            self.teste.geometry("300x100")
            num = len(caminho_arquivos)
            print(num)
            vt =0

            for i in caminho_arquivos:
                dados = self._extrai_p(i)
                try:
                    nome_razao = dados.split('Nome/Razão Social')
                    nome_razao = nome_razao[1].split('RG/Inscrição Estadual')

                    cpf_cnpj = dados.split('CPF/CNPJ/Documento')
                    cpf_cnpj = cpf_cnpj[1].split('Bairro')

                    numero_nfs = dados.split('NFS-e DE NÚMERO ')
                    numero_nfs = numero_nfs[1].split(' E CÓDIGO DE VERIFICAÇÃO')

                    verifi_autencidade = dados.split('Código de Verificação de Autenticidade')
                    verifi_autencidade = verifi_autencidade[1].split(' às')
                    dados_completos.append([cpf_cnpj[0], nome_razao[0], numero_nfs[0], verifi_autencidade[0], i])

                    nc = (vt / num) * 100
                    print(nc)
                    Label(self.teste, text=f'Extraindo notas: {nc:.2f}% Concluído.').place(rely=0.1,relx=0.2)
                    self.teste.update()
                    vt += 1
                    if nc > 99.38:
                        try:
                            # self.teste.destroy()
                            self.teste.destroy()
                        except Exception as e:
                            print(e)

                except EXCEPTION as e:
                    print(e)

            self.teste.focus_force()  #
            # novaTela.grab_set()  #
            self.teste.resizable(False, False)
            self.teste.mainloop()
        except Exception as e:
            print(e)

        return dados_completos

    def renomeia_arquivos(self, local_da_pasta, dados_extraidos):
        """
        :param local_da_pasta: busca a pasta onde está o arquivo.
        :param dados_extraidos: busca a lista de dados já extraidas da nota para renomear os arquivos.
        Return: todos os arquivos serão renomeados conforme a Razão dos nomes.
        """
        for info in dados_extraidos:
            try:
                f = os.path.join(local_da_pasta, info[1] + '.PDF')
                os.rename(info[4], f)
                info.insert(4, f)
            except:
                print(f"Deu erro ao renomeiar arquivo")


