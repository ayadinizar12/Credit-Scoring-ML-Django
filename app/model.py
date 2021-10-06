import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


import warnings
warnings.filterwarnings('ignore')

df=pd.read_excel('BayesianRidge_Data.xlsx')

df.drop('Unnamed: 0',axis=1,inplace=True)

import pandas as pd


liste=["RAF1","RAF2","RFD","RLG","RLR","RFI","DPC","RCP","TRN"]

for i in range(0,len(liste)):

    m = df.loc[df[liste[i]] != np.inf, liste[i] ].max()
    df[liste[i]].replace(np.inf,m,inplace=True)

for i in range(0,len(liste)):

    n = df.loc[df[liste[i]] != -np.inf, liste[i] ].min()
    df[liste[i]].replace(-np.inf,n,inplace=True)

#function to clean dataset
def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


#clean dataset
clean_dataset(df)


#sampling
Bankrupt_companies_number=len(df[df['Approval'] == 0])
Bankrupt_companies=(df[df['Approval'] == 0])
Non_Bankrupt_companies=(df[df['Approval'] == 1]).sample(n=Bankrupt_companies_number ,replace=True)
Final_Sampled_Data_BayesianRidge = Bankrupt_companies.append(Non_Bankrupt_companies)




print(df.head())
#features and target 
x = Final_Sampled_Data_BayesianRidge[['RAF1','RAF2','RFD','RLG','RLR','RFI','DPC','RCP','TRN']]
y = Final_Sampled_Data_BayesianRidge['Approval']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.3,random_state=10)


#Preparing Random Forest Classifie

ET_Model=RandomForestClassifier(n_estimators=116)


#Create a Gaussian Classifier


ET_Model.fit(x_train,y_train)


y_predict=ET_Model.predict(x_test)


import joblib
filename='final_model_br.sav'
joblib.dump(ET_Model,filename)