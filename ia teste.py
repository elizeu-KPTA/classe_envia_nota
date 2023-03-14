# Importando as bibliotecas necessárias
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# Criando um conjunto de dados de treinamento para a operação AND
X_and = np.array([[0,0],[0,1],[1,0],[1,1]])
y_and = np.array([0,0,0,1])

# Criando um modelo de rede neural para a operação AND
model_and = Sequential()
model_and.add(Dense(1, input_dim=2, activation='sigmoid'))
model_and.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinando o modelo para a operação AND
model_and.fit(X_and, y_and, epochs=1000, verbose=0)

# Avaliando o modelo para a operação AND
score_and = model_and.evaluate(X_and, y_and)
print("\nAcurácia da rede neural para a operação AND: %.2f%%" % (score_and[1]*100))


# Criando um conjunto de dados de treinamento para a operação NAND
X_nand = np.array([[0,0],[0,1],[1,0],[1,1]])
y_nand = np.array([1,1,1,0])

# Criando um modelo de rede neural para a operação NAND
model_nand = Sequential()
model_nand.add(Dense(1, input_dim=2, activation='sigmoid'))
model_nand.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinando o modelo para a operação NAND
model_nand.fit(X_nand, y_nand, epochs=1000, verbose=0)

# Avaliando o modelo para a operação NAND
score_nand = model_nand.evaluate(X_nand, y_nand)
print("\nAcurácia da rede neural para a operação NAND: %.2f%%" % (score_nand[1]*100))


# Criando um conjunto de dados de treinamento para a operação OR
X_or = np.array([[0,0],[0,1],[1,0],[1,1]])
y_or = np.array([0,1,1,1])

# Criando um modelo de rede neural para a operação OR
model_or = Sequential()
model_or.add(Dense(1, input_dim=2, activation='sigmoid'))
model_or.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinando o modelo para a operação OR
model_or.fit(X_or, y_or, epochs=1000, verbose=0)

# Avaliando o modelo para a operação OR
score_or = model_or.evaluate(X_or, y_or)
print("\nAcurácia da rede neural para a operação OR: %.2f%%" % (score_or[1]*100))