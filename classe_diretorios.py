from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os


class Diretorios:
    def __init__(self):
        pass

    def buscar_diretorio_do_arquivo(self):  # Retorna o diretório absoluto do arquivo
        Tk().withdraw()
        local_arquivo = askopenfilename()
        return local_arquivo

    def busca_diretorio_da_pasta(self):  # Busca leva o locar para salvar o arquivo
        local = askdirectory()
        return local

    def localiza_todos_arquivos_na_pasta(self, local):  # Recebe o diretório e localiza todos os registros
        caminho_absoluto = list()
        nome_arquivo = list()
        caminhoAbsoluto = os.path.abspath(local)
        for pastaAtual, subPastas, arquivos in os.walk(caminhoAbsoluto):
            caminho_absoluto.extend([os.path.join(pastaAtual, arquivo)
                                     for arquivo in arquivos if arquivo.endswith('.pdf')])
            nome_arquivo.extend([os.path.join(arquivo) for arquivo in arquivos if arquivo.endswith('.pdf')])
        return caminho_absoluto


