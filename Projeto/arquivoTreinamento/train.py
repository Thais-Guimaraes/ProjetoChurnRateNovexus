import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn import set_config
from imblearn.over_sampling import SMOTE

# Salvando o diretório atual e apontando para cada diretório (dados, modelos e pipeline)
project_directory = os.path.dirname(__file__)
dados_directory = os.path.join(project_directory, '../dados')
modelos_directory = os.path.join(project_directory, '../modelos')
pipeline_directory = os.path.join(project_directory, '../pipeline')

# Função para treinar o modelo, recebe o dataframe (que será o arquivo csv salvo na Parte 1 e os hiperparâmetros do modelo)
def train(df, hyperparameters):
    dados = df.drop(['CustomerID', 'Total', 'Gender','PhoneService'],axis =1) # retirando as colunas que não são primordiais e que não foram usadas no treino
    
    var_cat = [colname for colname, coltype in dados.dtypes.items() if dados[colname].dtype == object] # Salvando os nomes das colunas categóricas
    
    binarizar = dados[var_cat].loc[:,dados.nunique()<3].columns # Salvando as colunas que possuem 2 opções nas categorias (No/Yes)
    
    dados[binarizar] = np.where(dados[binarizar] == 'No', 0, 1) # O que for No = 0, Yes = 1
    
    smote = SMOTE(random_state=42) # Criando o objeto do smote
    
    # Criando o Pipeline com StandardScaler e One Hot Encoder
    set_config(transform_output="pandas") 
    numeric_features = ["Tenure","Monthly"]
    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    categorical_features = ['InternetService', 'Contract', 'PaymentMethod']
    categorical_transformer = Pipeline(
        steps=[
            ("encoder", OneHotEncoder(sparse_output=False, handle_unknown="ignore", dtype = np.int64))
            ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ], remainder= 'passthrough'
    )

    pipeline = Pipeline(
    steps=[("preprocessor", preprocessor)]
    )
    
    # Aplicando o pipeline
    dados_processados = pipeline.fit_transform(dados)
    
    # Salvando os valores de X
    dados_processados = dados_processados.drop('remainder__Churn', axis = 1)
    
    # Atribuindo para variáveis com as nomenclaturas mais representativas
    X = dados_processados
    y = dados['Churn']
    
    # Aplicar o SMOTE no conjunto de dados
    X_preprocessed,y = smote.fit_resample(X,y)
    
    # Criando o objeto do modelo      
    model = RandomForestClassifier(**hyperparameters)
    # Aplicando o X e y para treinar o modelo
    model.fit(X_preprocessed, y)
    
     
    # Salvando o pipeline para utilizar posteriormente no app.py
    pipeline_path = os.path.join(pipeline_directory, 'trained_pipeline.pkl')
    
    
    with open(pipeline_path, 'wb') as file:
        pickle.dump(pipeline, file) 
    
 
    return model
  
# Função para salvar o modelo 
def save_model(model, filename):
    model_path = os.path.join(modelos_directory, filename)

    try:
        with open(model_path, 'wb') as file:
            try:
                pickle.dump(model, file)
                print(f"Model saved to {model_path}")
            except AttributeError:
                file.close()
                file = open(model_path, 'wb')
                pickle.dump(model, file)
                print(f"Model saved to {model_path}")
    except Exception as e:
        print(f"An error occurred while saving the model: (str{e}")
  
# Chamada das funções main e save_model               
if __name__ == '__main__':
    df = pd.read_csv(os.path.join(dados_directory, 'DadosFinalPt1.csv'), index_col=0)
    hyperparameters = {'bootstrap': True, 
                       'criterion': 'gini',
                       'max_depth': 6, 
                       'min_samples_leaf': 3,
                       'min_samples_split': 4, 
                       'n_estimators': 100}
    
    svm_model = train(df, hyperparameters)
    
    save_model(svm_model, 'model_final.pkl')  
   