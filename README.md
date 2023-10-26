# ProjetoChurnRateNovexus
<<<<<<< HEAD

Este projeto faz parte do Challenge Alura Dados.

## Objetivo: :dart:

O objetivo é contribuir na tomada de decisão a respeito das estratégias que a Novexus irá tomar para reduzir a Taxa de Evasão de Clientes.
E para isso, o objetivo será criar um modelo de machine learning capaz de identificar a probabilidade do cliente cancelar a assinatura com a empresa.
Desta forma, possibilitará que a empresa tome açoes para impedir que isso ocorra.

## Visão macro das atividades: :eyeglasses:

### Notebook Parte 1 - Manipulação e Análise Exploratória dos Dados (pasta notebooks) :game_die: 
Definição do Problema de Negócio
Entendimento dos Dados
Verificar e corrigir inconsistências nos dados
Analisar a distribuição das variáveis
Analisar quais variáveis influenciam na Taxa de Churn
Analisar a variável alvo

### Notebook Parte 2 - Criação dos Modelos de Machine Learning (pasta notebooks) :computer:
Foi realizado o processo de pré-processamento de dados, treinamento de modelos de machine learning,
seleção de modelos e otimização de hiperparâmetros. 
A avaliação e a melhoria do modelo, incluindo a remoção de variáveis, demonstram uma abordagem abrangente para obter o 
melhor desempenho do modelo. 
O Random Forest se destacou como a escolha final para o problema.

### Treinamento do Modelo (pasta arquivoTreinamento) :train:

O arquivo train.py foi criado para treinar o modelo final, com o objetivo de tornar o código mais bem organizado ,
bem como viabilizar a reprodutibilidade e automatização.
Foi criado um pipeline com os processos de padronização e one hot encoder, este pipeline foi salvo para posteriormente ser usado
quando for prever com novos dados. 
A ideia seria utilizar o mesmo para manter a consistência, (utilizei para a padronização das variáveis categóricas.) 

### WebApp para que possibilite o cadastro de novos dados para a previsão (pasta app) :spider_web:
Neste arquivo criei a tela para inserir novos dados. Como os novos dados não teriam todas as opções nas categorias do One Hot Encoder, 
realizei algumas etapas para transformar os dados e gerar o One Hot Encoder manualmente, bem como a binarização das variáveis. 
Para a padronização dos dados numéricos utilizei o pipeline gerado no train.py.
E o modelo utilizado foi o modelo salvo no train.py
A ideia seria aplicar várias técnicas aprendidas até então, por isso, também utilizei expressões regulares na parte de transformação dos dados.


=======

>>>>>>> fdb0047b210c946f3503879a0324ff3f84d64465
