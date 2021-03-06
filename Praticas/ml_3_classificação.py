# -*- coding: utf-8 -*-
"""ML_3_Classificação.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BX3L47gfW4v6yw7jV1FVI2T4brVbds6T

# Especialização em Ciência de Dados - PUC-Rio
# Machine Learning
## Problemas de Classificação

# Importação dos dados

Usaremos a mesma base de dados que trabalhamos anteriormente, o dataset Pima Indians Diabetes. O trecho de código a seguir é idêntico ao que fizemos no laboratório passado e serve apenas para importar os dados e separá-los em entradas (X) e saídas (Y).
"""

# Carrega arquivo csv usando Pandas usando uma URL

# Importa todo o pacote Pandas
import pandas as pd

# Importa a função datasets
from sklearn import datasets

# Informa a URL de importação do dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

# Informa o cabeçalho das colunas
colunas = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

# Lê o arquivo utilizando as colunas informadas
dataset = pd.read_csv(url, names=colunas, skiprows=0, delimiter=',')

# Pega apenas os dados do dataset e guardando em um array
array = dataset.values

# Separa o array em variáveis preditoras (X) e variável target (Y)
X = array[:,0:8]
Y = array[:,8]

"""O trecho de código a seguir ilustra como importar um dos datasets que já vem junto com o scikit-learn. São eles:

* load_boston([return_X_y])	- **boston house-prices** (regressão).
* load_iris([return_X_y])	- **iris** (classificação).
* load_diabetes([return_X_y])	- **diabetes** (regressão).
* load_digits([n_class, return_X_y]) - **digits** (classificação).
* load_linnerud([return_X_y])	- **linnerud** (regressão multivariada).
* load_wine([return_X_y])	- **wine** (classificação).
* load_breast_cancer([return_X_y]) - **breast cancer wisconsin** (classificação).
"""

# NÃO EXECUTAR PARA O LABORATÓRIO!

# Datasets do scikit-learn: https://scikit-learn.org/stable/datasets/index.html

# Importação de pacotes
import pandas as pd
import numpy as np
from sklearn import datasets

# Carrega o dataset iris
iris = datasets.load_iris()

# Converte para dataframe
dataframe = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])

# Mostra as 5 primeiras linhas do dataset
dataframe.head(5)

# Extraindo os 2 primeiros atributos para variáveis preditoras (x) e variável target (y)
x_iris = iris.data[:, :2] 
y_iris = iris.target

"""# Resampling: Particionamento do dataset

## Particionamento em Conjuntos de Treino e Teste

https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
"""

# Import dos pacotes
from sklearn.model_selection import train_test_split

# Definição do tamanho do conjunto de teste para 33%
teste_size = 0.33

# A semente (seed) pode ser qualquer número, e garante que os resultados possam ser reproduzidos de forma idêntica toda vez que o script for rodado. 
# Isto é muito importante quando trabalhamos com modelos ou métodos que utilizam de algum tipo de aleatoriedade.
seed = 7

# Criando os conjuntos de dados de treino e de teste
X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size = teste_size, random_state = seed)

"""## Validação Cruzada (K-fold Cross-Validation)

https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html
"""

# Avaliação usando Cross Validation

# Import dos pacotes
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

# Definição dos valores para os folds e seed
num_folds = 10
seed = 7

# Separando os dados em folds
kfold = KFold(num_folds, True, random_state = seed)

"""# Métricas de Avaliação para Problemas de Classificação

http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.cross_val_score.html

http://scikit-learn.org/stable/modules/model_evaluation.html

Para ilustrar as métricas, precisaremos criar um modelo qualquer. Vamos usar a Regressão Logística.
"""

from sklearn.linear_model import LogisticRegression
modelo = LogisticRegression(solver='liblinear')

"""## Acurácia

**Acurácia = número de previsões corretas/todas as previsões**

É a métrica de avaliação mais comum para problemas de classificação, mas é também a mais mal utilizada. Ela só é adequada quando as classes são equilibradasm e que todos os erros de previsão são igualmente importantes, o que geralmente não é o caso.
"""

### 1. Usando validação cruzada

# Calculando a acurácia usando o modelo criado anteriormente
resultado = cross_val_score(modelo, X, Y, cv = kfold, scoring = 'accuracy')

# Print dos resultados
print("Acurácia: %.3f" % (resultado.mean() * 100))

### 2. Usando conjuntos de treino e teste

# Treinamento do modelo criado anteriormente
modeloTreinado = modelo.fit(X_treino, Y_treino)

# Previsões
Y_pred = modeloTreinado.predict(X_teste)

# Resultados
corretas = (Y_teste == Y_pred).sum()
total = Y_teste.shape[0]

# Print dos resultados
print("Acurácia com particionamento treino-teste: %.2f%%" % (corretas / total * 100))

"""## Área sobre a curva ROC (AUC)

Métrica de performance para classificação binária, em que podemos definir as classes em positiavs e negativas. Estes problemas são um *trade-off* entre Sensitivity (Sensibilidade) e Specifity (Especificidade).
* Sensitivity: a taxa de verdadeiros positivos (TP). Número de instâncias positivas da primeira classe que foram previstas corretamente.
* Specifity: a taxa de verdadeiros negativos (TN). Número de instâncias da segunda classe que foram previstas corretamente.

Valores acima de 0.5 indicam uma boa taxa de previsão.
"""

# Calculando a AUC usando a validação cruzada e o modelo criado anteriormente
resultado = cross_val_score(modelo, X, Y, cv = kfold, scoring = 'roc_auc')

# Print do resultado
print("AUC: %.2f%%" % (resultado.mean() * 100))

"""## Combinando métricas

Com a biblioteca cross_validate é possível exibir diversas métricas, incluindo as métricas de treino e teste. Veja mais em: 
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html

A lista de métricas suportadas está disponível em: 
https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
"""

# Import da função
from sklearn.model_selection import cross_validate

# Calculando a acurácia e a AUC usando a validação cruzada e o modelo criado anteriormente
resultado = cross_validate(modelo, X, Y, cv = kfold,
                        scoring=('accuracy', 'roc_auc'),
                        return_train_score=True)
   
print("train_accuracy: %.2f%%" % ((resultado['train_accuracy'].mean()) * 100) )
print("test_accuracy: %.2f%%" % ((resultado['test_accuracy'].mean()) * 100) )
print("train_roc_auc: %.2f%%" % ((resultado['train_roc_auc'].mean()) * 100) )
print("test_roc_auc: %.2f%%" % ((resultado['test_roc_auc'].mean()) * 100) )

"""## Matriz de Confusão

Como a matriz de confusão não é uma métrica única, ela não é suportada pelas funções *cross_val_score* e *cross_validate*. É mais fácil gerá-la usando o particionamento em conjuntos de treino e teste.
"""

# Matriz de Confusão

# Import da função
from sklearn.metrics import confusion_matrix

# Resultado do modelo nos dados de teste 
previsoes = modelo.predict(X_teste)
matrix = confusion_matrix(Y_teste, previsoes) 
print(matrix)

"""## Relatório de Métricas de Classificação do scikit-learn

O scikit-learn também disponibiliza uma função que gera um relatório de métricas, a *classification_report*.
"""

# Import da função
from sklearn.metrics import classification_report

# Criação do relatório
report = classification_report(Y_teste, previsoes) 
print(report)

"""# Algoritmos de Classificação

Vamos criar uma função de treinamento e avaliação que será usada em todos os modelos, para evitar duplicação de código.
"""

from sklearn import metrics

### Treinamento e avaliação do modelo

def treinarAvaliarModelo (modelo):

    ## 1. Usando validação cruzada

    print("=== Usando validação cruzada ===")

    # Aplicação do modelo e cálculo dos resultados
    resultado = cross_validate(modelo, X, Y, cv = kfold,
                            scoring=('accuracy', 'roc_auc'),
                            return_train_score=True)

    print("Acurácia de treino: %.2f%%" % ((resultado['train_accuracy'].mean()) * 100) )
    print("Acurácia de teste: %.2f%%" % ((resultado['test_accuracy'].mean()) * 100) )
    print("AUC de treino: %.2f%%" % ((resultado['train_roc_auc'].mean()) * 100) )
    print("AUC de teste: %.2f%%" % ((resultado['test_roc_auc'].mean()) * 100) )
    print("\n")

    ## 2. Usando conjuntos de treino e teste em vez de validação cruzada

    # Treinamento
    modeloTreinado = modelo.fit(X_treino, Y_treino)

    # Previsões
    Y_pred = modeloTreinado.predict(X_teste)

    # Resultados
    corretas = (Y_teste == Y_pred).sum()
    total = Y_teste.shape[0]

    # Print dos resultados
    
    print("=== Usando particionamento treino-teste ===")
    print("Acurácia de teste: %.2f%%" % (corretas / total * 100))
    print("\n")
    print(metrics.classification_report(Y_teste, Y_pred))
    print(metrics.confusion_matrix(Y_teste, Y_pred))
    
    return;

"""Relembrando...
<ul>
<li>Precision: Será que o que eu recuperei tem qualidade?</li>
<li>Recall: Será que eu recuperei tudo que deveria recuperar ?</li>
<li>F1-score: Faz uma media harmonica entre os dois</li>
<li>Support: Qtd de registros do conjunto que se enquadram na classificação</li>
</ul>

## Árvores de Decisão

Os modelos de árvores de decisão constroem uma árvore binária a partir dos dados de treinamento. Os pontos de divisão são escolhidos através da avaliação dos dados de treinamento, com base na contribuição de cada atributo para minimizar uma função de custo (como, por exemplo, o índice Gini, usado para medir a probabilidade de dois itens aleatórios pertencerem à mesma classe). Para construir um modelo do tipo CART (Classification and Regression Trees), podemos usar a classe DecisionTreeClassifier.

http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

**OBS:**
Quais são os vários algoritmos da árvore de decisão e como eles diferem um do outro? Qual é implementado no scikit-learn?

* ID3 (Iterative Dichotomiser 3) foi desenvolvido em 1986 por Ross Quinlan. O algoritmo cria uma árvore de múltiplas vias, encontrando para cada nó (isto é, de maneira gulosa) o recurso categórico que produzirá o maior ganho de informação para os alvos categóricos. As árvores crescem no tamanho máximo e, em seguida, geralmente é aplicada uma etapa de poda para melhorar a capacidade da árvore de generalizar para dados não vistos.

* C4.5 é o sucessor do ID3 e removeu a restrição de que os recursos devem ser categóricos, definindo dinamicamente um atributo discreto (com base em variáveis numéricas) que particiona o valor do atributo contínuo em um conjunto discreto de intervalos. C4.5 converte as árvores treinadas (ou seja, a saída do algoritmo ID3) em conjuntos de regras if-then. Essa precisão de cada regra é então avaliada para determinar a ordem em que elas devem ser aplicadas. A poda é feita removendo a pré-condição de uma regra se a precisão da regra melhorar sem ela.

* C5.0 é o lançamento de uma versão mais recente da C4.5 sob uma licença proprietária. Ele usa menos memória e cria conjuntos de regras menores que o C4.5, sendo mais preciso.

* CART (Classification and Regression Trees) é muito semelhante ao C4.5, mas difere no fato de suportar variáveis de saída numéricas (problemas de regressão) e não computar conjuntos de regras. O CART constrói árvores binárias usando os atributos que produzem o maior ganho de informação em cada nó.

**O scikit-learn usa uma versão otimizada do algoritmo CART; no entanto, a implementação do scikit-learn não suporta variáveis categóricas por enquanto.**
"""

# Árvore de Classificação CART

# Import da função
from sklearn.tree import DecisionTreeClassifier

# Escolhendo o modelo
modelo = DecisionTreeClassifier()

# Print dos parâmetros do modelo
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

"""Também é possível especificar valores para os parâmetros da árvore de classificação:"""

# Criando o modelo já com os parâmetros desejados
modelo = DecisionTreeClassifier(max_depth = None, 
                             max_features = None, 
                             criterion = 'entropy', 
                             min_samples_leaf = 1, 
                             min_samples_split = 2)
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

"""É possível plotar a árvore gerada usando a função **plot_tree**. Vamos ilustrar com o dataset Iris, que é menor."""

from sklearn.datasets import load_iris
from sklearn import tree
iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)
tree.plot_tree(clf.fit(iris.data, iris.target))

"""## KNN
O algoritmo KNN usa uma métrica de distância para encontrar as k instâncias mais semelhantes nos dados de treinamento para uma nova instância e considera o resultado médio dos vizinhos como a previsão. Podemos construir um modelo KNN usando a classe KNeighborsClassifier.

http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
"""

# KNN

# Import da função
from sklearn.neighbors import KNeighborsClassifier

# Escolhendo o modelo
modelo = KNeighborsClassifier()

# Print dos parâmetros do modelo
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

"""Vamos agora experimentar variar alguns dos parâmetros do modelo."""

# Criação de outro modelo alterando o tipo de distância
modelo = KNeighborsClassifier(metric = 'euclidean')
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

print("\n")

# Criação de outro modelo alterando o valor de k
modelo = KNeighborsClassifier(n_neighbors = 7)
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

"""## Naive Bayes
O algoritmo Naive Bayes calcula a probabilidade de cada classe e a probabilidade condicional de cada classe, considerando cada valor de entrada. Essas probabilidades são estimadas para novos dados e multiplicadas juntas, assumindo que sejam todas independentes (uma suposição simples ou ingênua). Ao trabalhar com dados com valores reais, supõe-se que eles seguem uma distribuição Gaussiana. Podemos construir um modelo Naive Bayes usando a classe GaussianNB.

http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
"""

# Naive Bayes

# Import da função
from sklearn.naive_bayes import GaussianNB

# Escolhendo o modelo
modelo = GaussianNB()

# Print dos parâmetros do modelo
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

"""## Support Vector Machines
O SVM busca uma linha que melhor separa duas classes. As instâncias de dados mais próximas desta linha são chamadas vetores de suporte e influenciam onde a linha é colocada. O SVM foi estendido para suportar várias classes e é possível utilizar diferentes funções kernel. Por padrão, é usada e função de base radial. Vamos construir um modelo SVM usando a classe SVC.

http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

http://scikit-learn.org/stable/modules/svm.html
"""

# SVM com kernel linear

# Import da função
from sklearn.svm import SVC

# Escolhendo o modelo
modelo = SVC(gamma='auto',kernel = 'linear')

# Print dos parâmetros do modelo
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

# Imprimindo os vetores de suporte
print("\n")
print (modelo.support_)

# SVM com kernel RBF (funciona bem para dados não linearmente separáveis, mas pode aprender demais sobre os dados - overfitting)

# Import da função e do pacote metrics
from sklearn.svm import SVC
from sklearn import metrics

# Escolhendo o modelo
modelo = SVC(gamma='auto', kernel = 'rbf')

# Print dos parâmetros do modelo
print(modelo.get_params)
print("\n")

# Treinamento e avaliação do modelo
treinarAvaliarModelo(modelo)

# Imprimindo os vetores de suporte
print("\n")
print (modelo.support_)

"""# Tuning Automático de Hiperparâmetros
Podemos avaliar de forma fácil diversas variações de parâmetros de algoritmos usando a função *GridSearchCV*. Para tal, vamos criar uma função de tuning que recebe um modelo, um conjunto de parâmetros, a métrica de avaliação e o número de folds. Esta função irá imprimir o modelo com o melhor resultado.

https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

https://scikit-learn.org/stable/modules/grid_search.html
"""

def tuningHiperparametros (modelo, param_grid, scoring, kfold):
  
  # Avaliação de todas as combinações
  grid = GridSearchCV(estimator=modelo, param_grid=param_grid, scoring=scoring, cv=kfold,
      iid=True)
  grid_result = grid.fit(X_treino_padronizado, Y_treino)

  # Imprime o modelo com o melhor resultado
  print("Melhor: %f com %s" % (grid_result.best_score_, grid_result.best_params_)) 

  # Imprime todos os resultados
  means = grid_result.cv_results_['mean_test_score']
  stds = grid_result.cv_results_['std_test_score']
  params = grid_result.cv_results_['params']
  for mean, stdev, param in zip(means, stds, params):
      print("%f (%f) com: %r" % (mean, stdev, param))
  return;

"""Vamos padronizar os dados de treinamento e trabalhar com validação cruzada 10-fold. Iremos variar os hiperparâmetros dos modelos: Árvore de Decisão, KNN e SVM. No NaiveBayes não há muito que variar."""

# Import das funções
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

# Padronização dos dados de treinamento
scaler = StandardScaler().fit(X_treino)
X_treino_padronizado = scaler.transform(X_treino)

# Definição dos valores para os folds e seed
num_folds = 10
seed = 7

# Separando os dados em folds
kfold = KFold(n_splits=num_folds, random_state=seed)

"""## Árvores de Decisão
Vamos testar os critérios gini e entropia e variar o tamanho máximo da árvore e o mínimo de exemplos em cada nó folha.
"""

# Definição dos possíveis valores de hiperparâmetros
criterios = ['gini', 'entropy']
max_depth = [3,5,10,20,30,40,50]
min_samples_leaf = [3,5,10,20,30,40,50]
param_grid = dict(criterion=criterios, min_samples_leaf=min_samples_leaf, max_depth=max_depth)

# Escolha do modelo
modelo = DecisionTreeClassifier()

# Definição da métrica de avaliação
scoring = 'accuracy'
#scoring = 'roc_auc'

# Avaliação de todas as combinações e impressão dos resultados
tuningHiperparametros(modelo, param_grid, scoring, kfold)

"""## KNN
O número padrão de vizinhos (k) para o KNN é 7. Vamos testar todos os valores ímpares entre 1 a 21 para k, cobrindo o valor padrão de 7 e 3 diferentes medidas de distância.
"""

# Definição dos possíveis valores de hiperparâmetros
k = [1,3,5,7,9,11,13,15,17,19,21]
distancias = ["euclidean", "manhattan", "minkowski"]
param_grid = dict(n_neighbors=k, metric=distancias)

# Escolha do modelo
modelo = KNeighborsClassifier()

# Definição da métrica de avaliação
scoring = 'accuracy'
#scoring = 'roc_auc'

# Avaliação de todas as combinações e impressão dos resultados
tuningHiperparametros(modelo, param_grid, scoring, kfold)

"""## SVM
Podemos ajustar dois parâmetros principais do algoritmo SVM, o valor de C (o quanto flexibilizar a margem) e o tipo de kernel. O padrão para o SVM (classe SVC) é usar o kernel da Função Base Base Radial (RBF) com um valor C definido como 1.0. Vamos testar vários tipos de kernel e valores C com menos viés e mais viés (menor que e maior que 1,0, respectivamente).
"""

# Definição dos possíveis valores de hiperparâmetros
c_values = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.3, 1.5, 1.7, 2.0]
kernel_values = ['linear', 'poly', 'rbf', 'sigmoid']
param_grid = dict(C=c_values, kernel=kernel_values)

# Escolha do modelo
modelo = SVC(gamma='auto')

# Definição da métrica de avaliação
scoring = 'accuracy'
#scoring = 'roc_auc'

# Avaliação de todas as combinações e impressão dos resultados
tuningHiperparametros(modelo, param_grid, scoring, kfold)

"""# Comparação gráfica de algoritmos

Quando trabalhamos em projetos de Machine Learning, geralmente temos vários bons modelos para escolher. Cada modelo terá características de desempenho diferentes. É importante usar várias métricas diferentes para avaliar os algoritmos.

Para que seja feita uma comparação justa, é preciso garantir que cada algoritmo seja avaliado da mesma maneira nos mesmos dados. É importante usar a mesma semente aleatória para garantir que as mesmas divisões nos dados de treinamento sejam executadas e que cada algoritmo seja avaliado precisamente da mesma maneira.

Neste exemplo, iremos avaliar diversos modelos usando uma representação gráfica.
"""

# Comparação de Algortimos

# Import da função
from matplotlib import pyplot

# Lista de modelos a avaliar
modelos = []
# Aqui, poderíamos criar o modelo já parametrizado com os melhores hiperparâmetros da seção anterior
modelos.append(('CART', DecisionTreeClassifier()))
modelos.append(('KNN', KNeighborsClassifier()))
modelos.append(('NB', GaussianNB()))
modelos.append(('SVM', SVC(gamma='auto')))

# Treinamento e avaliação de cada modelo
results = []
names = []
scoring = 'accuracy'
for name, model in modelos:
  kfold = KFold(n_splits=10, random_state=7)
  cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
  results.append(cv_results)
  names.append(name)
  msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
  print(msg)
  
# Comparação dos algoritmos em boxplot
fig = pyplot.figure() 
fig.suptitle('Comparação dos algoritmos') 
ax = fig.add_subplot(111) 
pyplot.boxplot(results) 
ax.set_xticklabels(names) 
pyplot.show()