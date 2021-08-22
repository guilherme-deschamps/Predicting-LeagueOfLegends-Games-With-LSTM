import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# # tamanho da fatia
tamanho = 5000

for fatia in pd.read_csv('games.csv', chunksize=tamanho):
    # seu código aqui
    data = fatia

data.head()

# ideia: a partir de winner + first blood + first tower prever quem vence uma partida
df = data[['firstBlood', 'firstTower', 'firstInhibitor', 'firstBaron', 'firstDragon', 'firstRiftHerald', 'winner']]

# prévia:    [1,1,1] [2,2,?]
df.head()

# #creating an array
# pred_data = df.to_numpy()

# print(df)

from numpy import array
from numpy import hstack


# split a multivariate sequence into samples
def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1, -1]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


n_steps = 6

X, y = split_sequences(df.values, n_steps)

# summarize the data
for i in range(len(X)):
    print(X[i], y[i])

# carrega o método train_test_split
from sklearn.model_selection import train_test_split

# define qualquer valor para o parâmetro random_state.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=5)

# imprime a quantidade de linhas dos conjuntos
print('X_train: numero de linhas e colunas: {}'.format(X_train.shape))
print('X_test: numero de linhas e colunas: {}'.format(X_test.shape))
print('y_train: numero de linhas e colunas: {}'.format(y_train.shape))
print('y_test: numero de linhas e colunas: {}'.format(y_test.shape))

from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

n_steps = X.shape[2]

# define model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(6, n_steps)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# fit model
model.fit(X_train, y_train, epochs=100, verbose=0)

# demonstrate prediction
x_input = array(X_test)
# x_input = x_input.reshape((1, X_test, n_features))
yhat = model.predict(x_input)
print(yhat)

from sklearn.metrics import accuracy_score

accuracy_score(y_test, np.round(abs(yhat)), normalize=True)

import plotly.graph_objects as go

# cria um dataframe vazio
df_results = pd.DataFrame()
# adiciona a coluna valor_real
df_results['valor_real'] = y_test
# cria a coluna valor_predito_baseline com as predicoes
df_results['valor_predito_baseline'] = yhat

# Create traces
fig = go.Figure()

# Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_real,
                         mode='markers',
                         name='Valor Real'))

# Linha com os dados de baseline
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_predito_baseline,
                         mode='lines+markers',
                         name='Previsão'))

# Plota a figura
fig.show()

pyinstaller - -onefile - w
