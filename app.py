import streamlit as st
import pickle
import pandas as pd 
from PIL import Image      
import os
import re

project_directory = os.path.dirname(__file__)
#project_directory = os.path.dirname(__file__)
modelos_directory = os.path.join(project_directory, 'Projeto/modelos')
pipeline_directory = os.path.join(project_directory, 'Projeto/pipeline')
imagens_directory = os.path.join(project_directory, 'Projeto/imagens')

# Options for each cell
SeniorCitizen_Options = ['No', 'Yes']
Partner_Options = ['No', 'Yes']
Dependents_Options = ['No', 'Yes']
MultipleLines_Options = ['No', 'Yes']
InternetService_Options = ['DSL', 'Fiber optic', 'No']
OnlineSecurity_Options = ['No', 'Yes']
OnlineBackup_Options = ['No', 'Yes']
DeviceProtection_Options = ['No', 'Yes']
TechSupport_Options = ['No', 'Yes']
StreamingTV_Options = ['No', 'Yes']
StreamingMovies_Options = ['No', 'Yes']
Contract_Options = ['One year', 'Month-to-month', 'Two year']
PaperlessBilling_Options = ['No', 'Yes']
PaymentMethod_Options = ['Mailed check', 'Electronic check', 'Credit card (automatic)', 'Bank transfer (automatic)']

# Função para salvar os inputs do usuário
def form_data():
    data = {"remainder__SeniorCitizen": None, "remainder__Partner": None, "remainder__Dependents": None, "Tenure": None, 
            "remainder__OnlineBackup": None, "remainder__StreamingMovies": None, "remainder__MultipleLines": None, 
            "remainder__DeviceProtection": None, "Contract": None, "InternetService": None, "remainder__TechSupport": None, 
            "remainder__PaperlessBilling": None, "remainder__OnlineSecurity": None, "remainder__StreamingTV": None, "PaymentMethod": None, "Monthly": None}
    
    with st.container():
        st.markdown('<h4>Personal data</h4>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
             data["remainder__SeniorCitizen"] = st.selectbox("Senior Citizen", SeniorCitizen_Options)
        with col2:
            data["remainder__Partner"] = st.selectbox("Partner", Partner_Options)
        with col3:
            data["remainder__Dependents"] = st.selectbox("Dependents", Dependents_Options)
       
    with st.container():
        st.markdown('<h4>Dados Contratuais</h4>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            data["Tenure"] = st.number_input("Tenure", min_value=1, max_value=10, value=5, step=1)
        with col2:
            data["Monthly"] = st.number_input("Monthly", min_value=0, max_value=100, value=18)
        with col3:
            data["Contract"] = st.selectbox("Contract", Contract_Options)
    
    with st.container():
        st.markdown('<h4>Seviços Assinados</h4>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            data["remainder__MultipleLines"] = st.selectbox("Multiple Lines", MultipleLines_Options)
            data["remainder__DeviceProtection"] = st.selectbox("Device Protection", DeviceProtection_Options)
            data["remainder__PaperlessBilling"] = st.selectbox("Paperless Billing", PaperlessBilling_Options)
            
        with col2:
            data["InternetService"] = st.selectbox("Internet Service", InternetService_Options)
            data["remainder__TechSupport"] = st.selectbox("Tech Support", TechSupport_Options)
            data["PaymentMethod"] = st.selectbox("Payment Method", PaymentMethod_Options)
          
        with col3:
            data["remainder__OnlineBackup"] = st.selectbox("Online Backup", OnlineBackup_Options)
            data["remainder__StreamingTV"] = st.selectbox("Streaming TV", StreamingTV_Options)
            
        with col4:
            data["remainder__OnlineSecurity"] = st.selectbox("Online Security", OnlineSecurity_Options)
            data["remainder__StreamingMovies"] = st.selectbox("Streaming Movies", StreamingMovies_Options)
           
    return data

# Função para fazer o merge de dicionários
def merge(dict1, dict2):
        res = {**dict1, **dict2}
        return res

# Função principal
def main():
    
    # Caminho do logo
    image_path = os.path.join(imagens_directory, "Logo (6).png")

    image = Image.open(image_path)
    st.image(image, use_column_width=True, width=900)
    st.markdown("<h3 style='text-align: center;'> Avaliar Chance de Churn</h3>", unsafe_allow_html=True)
    
    # Salvando em uma variável os inputs
    data = form_data()
    
    # Obtendo o modelo treinado
    #model_path = os.path.join(modelos_directory, 'model_final.pkl')
    model_path = os.path.join(os.path.abspath(modelos_directory), 'model_final.pkl')
    model = pickle.load(open(model_path, 'rb'))
    

    
    ## Realizar o processo de ONE HOT ENCODER manualmente, porque os novos dados não terão todas as categorias, o pipeline não funcionaria
    
    # Variáveis que precisam do One Hot Encoder
    ohe_features = ['InternetService', 'Contract', 'PaymentMethod']
           
    # Atualizando a nomenclatura das variáveis com cat__ + _
    list_features_input = []
        
    for feature, value in data.items():
        if type(value) == str and feature in ohe_features:
            list_features_input.append('cat__' + feature + '_' + value)
       
         
    # Nome das variáveis depois do pipeline no treinamento (essas são as variáveis que passaram pelo One Hot Encoder)
    columns_model_categorical = ['cat__InternetService_DSL',
                                'cat__InternetService_Fiber optic', 'cat__InternetService_No',
                                'cat__Contract_Month-to-month', 'cat__Contract_One year',
                                'cat__Contract_Two year',
                                'cat__PaymentMethod_Bank transfer (automatic)',
                                'cat__PaymentMethod_Credit card (automatic)',
                                'cat__PaymentMethod_Electronic check',
                                'cat__PaymentMethod_Mailed check']
                                
    # Para as variáveis que estão no input, vou marcar sim, exemplo , no processo anterior, foi ajustado o nome da variável
    # com o cat + feature + valor então, se alguem possui intenet service DSL, ficará assim: cat__InternetService_DSL
    # para estes que estão na lista do input será marcado o 1
    
    data_new = {}
    for i in list_features_input:
        for j in columns_model_categorical:
            if i == j:
                data_new[j] = 1
    
    # Para os que não estão na lista serão marcados o 0
    new_dict = {}
    for k, v in data_new.items():
        for i in range(len(columns_model_categorical)):
            if columns_model_categorical[i] not in data_new:
                new_dict[columns_model_categorical[i]] = 0
                
    
    # Unindo os dois anteriores  
    all_data = merge(new_dict, data_new)
    
    # Para as colunas numéricas apenas pegando o valor passado no input
    for k, v in data.items():
        if type(v) != str:
            all_data[k] = v
            
       
    # Expressão regular para encontrar chaves e valores que começam com "remainder__"
    pattern = re.compile(r'remainder__\w+')

    # Filtrar o dicionário usando a expressão regular
    filtered_data = {key: value for key, value in data.items() if pattern.match(key)}
   
    # Se o valor for No, será marcado com 0, se for Yes será marcado com 1
    # Usando dict comprehension
    filtered_data = {k: 0 if v == 'No' else 1 if v == "Yes" else v for k, v in filtered_data.items()}
    
    # Salvando tudo
    all_data_2 = merge(all_data, filtered_data)
    
    
    # Colunas esperadas pelo modelo 
    select_columns = ['Tenure', 'Monthly', 'cat__InternetService_DSL',
                      'cat__InternetService_Fiber optic', 'cat__InternetService_No',
                      'cat__Contract_Month-to-month', 'cat__Contract_One year',
                      'cat__Contract_Two year',
                      'cat__PaymentMethod_Bank transfer (automatic)',
                      'cat__PaymentMethod_Credit card (automatic)',
                      'cat__PaymentMethod_Electronic check',
                      'cat__PaymentMethod_Mailed check',
                      'remainder__SeniorCitizen', 'remainder__Partner',
                      'remainder__Dependents',
                      'remainder__MultipleLines', 'remainder__OnlineSecurity',
                      'remainder__OnlineBackup', 'remainder__DeviceProtection',
                      'remainder__TechSupport', 'remainder__StreamingTV',
                      'remainder__StreamingMovies', 'remainder__PaperlessBilling']
    
    final_table = pd.DataFrame([all_data_2], columns=select_columns, index=[0])
   
    # Colunas que passarão pelo processo de padronização usando o pipeline salvo no train.py      
    columns_scale = ['Tenure','Monthly']
    
    pipeline_path = os.path.join(pipeline_directory, 'trained_pipeline.pkl')
   
    loaded_pipeline = pickle.load(open(pipeline_path, 'rb'))
    
    # Acessando o scaler do pipeline
    scaler = loaded_pipeline.named_steps['preprocessor'].named_transformers_['num']
    
    # Aplicando o StandardScaler
    final_table[columns_scale] = scaler.transform(final_table[columns_scale])
    
    # A tabela final agora renomeando as colunas numéricas    
    final_table.rename(columns= {"Tenure": "num__Tenure", "Monthly": "num__Monthly" }, inplace = True)  
      
    #st.write(final_table.head())  # Print a final_table para testes 
    if st.button("Predict Churn"):
        try:
            prediction = model.predict_proba(final_table)
            churn_probability = prediction[0][1]  # Get the probability of churn
            st.write(f"Churn Probability: {churn_probability:.4f}")

            if churn_probability < 0.5:
                st.success("The client won't cancel the contract")
            else:
                st.success("The client will cancel the contract")
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
    
if __name__ == '__main__':
    main()
