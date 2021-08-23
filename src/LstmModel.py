import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from numpy import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go

class LstmModel:
    def init(self, entries):
        self.n_steps = 2
        self.neurons = 50
        self.loadData()
        self.setModelEntries(entries)
        self.X, self.y = self.split_sequences(self.df.values, self.n_steps)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.5,
                                                                                random_state=5)
        self.n_features = self.X.shape[2]
        self.createModel()
        self.fitAndPredict()
        self.getAccuracy()
        self.writeImage()

    def loadData(self):
        tamanho = 5000

        for fatia in pd.read_csv('datasets\games.csv', chunksize=tamanho):
            self.data = fatia

    def setModelEntries(self, entries):
        self.df = self.data[entries]

    # Split sequences: divide sequências de dados multivariados em X (entradas) e Y (saída)
    def split_sequences(self, sequences, n_steps):
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

    def createModel(self):
        self.model = Sequential()
        self.model.add(LSTM(self.neurons, activation='relu', input_shape=(self.n_steps, self.n_features)))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mse')

    def fitAndPredict(self):
        self.model.fit(self.X_train, self.y_train, epochs=50, verbose=0)
        x_input = array(self.X_test)
        # x_input = x_input.reshape((1, X_test, n_features))
        self.yhat = self.model.predict(x_input)

    def getAccuracy(self):
        return accuracy_score(self.y_test, np.round(abs(self.yhat)), normalize=True)

    def writeImage(self):
        # cria um dataframe vazio
        df_results = pd.DataFrame()
        # adiciona a coluna valor_real
        df_results['valor_real'] = self.y_test
        # cria a coluna valor_predito_baseline com as predicoes
        df_results['valor_predito_baseline'] = self.yhat

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

        fig.write_image("./fig.png")