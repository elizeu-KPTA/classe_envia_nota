import tkinter as tk
from PIL import Image, ImageTk

# cria uma janela
janela = tk.Tk()

# cria um canvas para desenhar o ícone da lixeirapip install --upgrade pip
canvas = tk.Canvas(janela, width=100, height=100)

# desenha o ícone da lixeira no canvas
canvas.create_rectangle(20, 30, 80, 80, fill="black")
canvas.create_polygon(10, 30, 20, 30, 20, 10, 80, 10, 80, 30, 90, 30, 90, 90, 80, 90, 80, 70, 20, 70, 20, 90, 10, 90, fill="white")

# salva o desenho do canvas em um arquivo .gif
canvas.postscript(file="icone.ps", colormode='color')
Image.open("icone.ps").save("icone.gif")

# cria um objeto PhotoImage a partir do arquivo .gif
imagem = tk.PhotoImage(file="icone.gif")

# cria um botão com a imagem da lixeira
botao = tk.Button(janela, image=imagem, text="Lixeira", compound="top")
botao.pack()

# inicia o loop principal da janela
janela.mainloop()