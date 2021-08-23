# Predicting-LeagueOfLegends-Games-With-LSTM
Trabalho implementado na disciplina de Inteligência Computacional, que busca identificar qual o time vencedor em uma partida de League of Legends baseado em informações limitadas.

1. [Guilherme Rafael Deschamps](https://github.com/guilherme-deschamps)
2. [Rodrigo Valle](https://github.com/rrrovalle)

# Sumário
1. [Problema](#problema)
2. [Dataset](#dataset)
3. [Técnica](#técnica)
4. [Resultados obtidos](#resultados-obtidos)
5. [Instruções de uso](#instruções-de-uso)
6. [Vídeo](#vídeo)

## Problema
No jogo de League of Legends, você deve entrar em partidas separadas e desempenhar com seu time de maneira estratégica, visando eliminar a estrutura central do time inimigo (denominada *Nexus*). Dessa forma, decisões tomadas no início do jogo causam impactos no decorrer de toda a partida, sobre os objetivos adquiridos e a chance de vitória de cada time. Dito isto, este projeto busca avaliar determinadas situações ocorridas em início de jogo para identificar seus impactos no resultado final das partidas de [League of Legends](https://br.leagueoflegends.com/pt-br/). O trabalho será aplicado sobre partidas de jogadores de alto nível, a fim de obter maior regularidade no nível dos jogadores e no desempenho ao longo do tempo.

![image](https://user-images.githubusercontent.com/39662856/130374262-0a34536b-3d26-44a5-a293-7c684f4bc0db.png)

## Dataset
O dataset utilizado se encontra disponível em: [(LoL) League of Legends Ranked Games](https://www.kaggle.com/datasnaek/league-of-legends)

## Técnica
Para implementação do modelo preditivo, será utilizada um modelo LSTM com uma única saída, baseado em séries multivariadas. Dados de série temporal multivariada significam que o modelo deverá observar, para cada intervalo de tempo, mais de uma varíavel. O que se encaixa perfeitamente na proposta elaborada.

Um modelo LSTM precisa de contexto suficiente para aprender um mapeamento de uma sequência de entrada para um valor de saída. Os LSTMs podem suportar séries temporais de entrada paralela como variáveis ou recursos separados. Portanto, precisamos dividir os dados em amostras, mantendo a ordem das observações nas duas sequências de entrada. Sendo assim, o dataset foi tratado para mapear uma sequência conforme selecionado pelo usuário. Entretanto, apesar do dataset fornecer 61 variáveis, escolhemos utilizar apenas 8 delas, sendo:

```
gameDuration	firstBlood	firstTower	firstInhibitor	firstBaron	firstDragon	firstRiftHerald		winner
```

Após escolher quais seriam os inputs com as características para o treinamento do modelo, obtivemos o seguinte output:

![image](https://user-images.githubusercontent.com/39662856/130373471-5fe6465e-8511-4ca1-81c3-81ac404ec54f.png)

Uma vez que os dados estão prontos para serem tratados, podemos então definir uma função chamada *split_sequences()* que pegará um conjunto de dados como o definimos com linhas para intervalos de tempo e colunas para séries paralelas e amostras de retorno de entrada/saída. Ou seja, transformamos os dados em um array com o tamanho das features escolhidas (representando o x) e o vencedor da partida (y). O número de passos escolhido para cada intervalo de tempo foi de **n_steps = 3**, onde a cada três inputs, o output é informado. O resultado obtido foi o seguinte:

```
[[1 2 1 2 2 0]
 [2 1 1 0 1 0]
 [2 1 1 0 2 0]] 1
```

Os dados foram então tratados, utilizando do método train_test_split da biblioteca sklearn, permitindo obter uma amostra de mesmo tamanho para fornecer ao modelo. As varíaveis carregadas foram X_Train, X_test, y_train e y_test, o que posteriormente também nos permite obter a acurácia do modelo e visualizar os dados.

````  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state=5)
````

Com os dados devidamente ajustados, optamos por utilizar um Vanilla LSTM onde o número de passos de tempo e séries paralelas (recursos) são especificados para a camada de entrada por meio do argumento input_shape. Após alguns testes, a quantidade de neurônios escolhidos para a primeira camada LSTM foi de 50. A função de ativação adotada foi a ReLu, uma função de ativação não linear usada em redes neurais multicamadas ou redes neurais profundas, tendo como saída um valor máximo entre zero e o valor de entrada. Para o otimizador foi escolhido o Adam (utilizado para atualizar os pesos da rede iterativos com base nos dados de treinamento). Por fim, a função de perda aplicada foi a *Mean Square Error (MSE)*, que é representada pela soma das distâncias quadradas entre nossa variável-alvo e os valores previstos.

```
# Modelo utilizado
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
```

Finalmente o modelo pode então ser treinado e testado. A quantidade de épocas utilizada para treinar o modelo foi de 200, uma vez que permitiram obter uma acurácia alta em um período de tempo para treinamento relativamente curto.

```
# Fit
model.fit(X_train, y_train, epochs=100, verbose=0)

# Exemplo de predição
x_input = array(X_test)
yhat = model.predict(x_input)
```

## Resultados obtidos
Para a obtenção dos resultados, foram realizados os seguintes experimentos:
 - Alterações nas variáveis de entrada: foram utilizadas duas configurações de variáveis de entrada. 
 - - FirstBaron e FirstInhibitor; 
 - - FirstBlood, FirstTower e First Dragon
 - Alterações na quantidade de épocas do modelo: foram utilizadas diferentes quantidades de épocas para o treinamento (50, 100, 300, 500), observando qual resultaria na maior acurácia.
 - Alterações no _nsteps_ do modelo (2, 3, 5), número que define a cada quantas entradas o modelo tenta predizer o resultado, observando qual resultaria na maior acurácia.

![image](https://user-images.githubusercontent.com/39662856/130400804-78386645-a06f-4865-9e68-22af7b7c94b2.png)

Analisando o gráfico, podemos observar que a melhor acurácia obtida pelo modelo foi de 0,88 (88%) em 50 épocas, com a configuração de entradas de _FirstBaron_ e _FirstInhibitor_. Podemos notar também que, para ambas as configurações de entradas, quanto maior o número de épocas pior a acurácia do modelo. O caso mais extremo alcançou 0,69 (69%) com 500 épocas na segunda configurações de entradas. 

Na busca dos melhores resultados para o modelo, a análise da acurácia com diferentes _nsteps_ foi também realizada, onde o cenário com a menor quantidade de steps (2) alcançou o melhor resultado (87%). Ao utilizar 3 steps a acurácia obtida foi de aproximadamente 85%, enquanto o invervalo de 5 steps resultou em uma acurácia de 83%.

<p align="center">
  <img width="460" height="300" src="https://user-images.githubusercontent.com/39662856/130401298-4fb74d70-e0a3-4820-a0e2-f9a7ad85855b.png">
</p> 

Em um aspecto geral os resultados foram satisfatórios. A acurácia do modelo ficou acima de 80% em alguns dos cenários testados, enquanto seu menor valor foi de 69%. Cabe ressaltar que o modelo terá acurácias diferentes destas dependendo das entradas que forem selecionadas. Alguns ajustes poderiam ser feitos para maximizar o poder de previsão do modelo, como por exemplo testar outras funções de ativação como _tanh_ ou até mesmo a _softmax_.

Os dados de acurácias exibidos foram obtidos ao fazer o experimento 5 vezes em cada configuração, e depois calculando a média das 5 acurácias obtidas em cada configuração.

## Instruções de uso
Para utilizar do sistema elaborado é necessário apenas executar o arquivo lolstm.exe localizado na pasta src. Ao executá-lo será possível, através da interface elaborada, escolher quais são os fatores de influência obtidos durante a partida para que seja possível mapear as chances de vitória de uma equipe. Por fim, ao executar o algoritmo, a acurácia do modelo é atualizada para permitir ver a efiência dele e um gráfico é apresentado, mostrando os dados obtidos com relação as colunas selecionadas.

## Vídeo
O vídeo com a demonstração da aplicação realizada se encontra em: 
