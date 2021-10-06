import camelot
import re
import numpy as np
import pandas as pd
import pdfplumber
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge


def get_page(pdf_path):  
    with pdfplumber.open(pdf_path) as pdf:    
        for pdf_page in pdf.pages:
            text=pdf_page.extract_text()
                #print(x)
            if text is None:
                continue
            else:
                #detecte les mots immobilisation /incorporelles / corporelles/stock
                if 'IMMOBILISATIONS' in text.upper() and 'INCORPORELLES' in text.upper() and 'CORPORELLES'in text.upper() and 'STOCK' in text.upper():
                    print(pdf_page.page_number)
                    return pdf_page.page_number
                else:
                    continue
    print("page not found")
    return -1


def get_indiceColonne(df_bilan):   
    nb_lignes = df_bilan.shape[0]
    nb_colonnes = df_bilan.shape[1]
    for i in np.arange(0,nb_lignes):   
        for j in np.arange(0,nb_colonnes):
            string = df_bilan.loc[i,j]
            
            if(len(string)>4):
                #remplace les characteres non ascii par ''
                string = ''.join(char for char in string if ord(char) < 128)
                string = string.replace(" ","")
                string = string.replace(",",".")

                try:
                    float(string)
                    
                    return j
                except ValueError:
                    
                    continue
    return 0
def get_Variable(df_bilan,Nom_variable):
    #appel de la fonction get_indiceColonne
    col = get_indiceColonne(df_bilan)
    #print(col)
    
    nb_lignes = df_bilan.shape[0]
    nb_colonnes = df_bilan.shape[1]
    #iteration sur les cellules du documents
    for i in np.arange(0,nb_lignes):
        for j in np.arange(0,nb_colonnes):
            variable = 0
            #print(i)
            cell = df_bilan.loc[i,j]
            if(chr(160) in df_bilan.loc[i,j]):
                #print('Danger')
                cell = df_bilan.loc[i,j].replace(chr(160),' ')
            
            #verifie la variable a chercher avec l'expression reguliere
            if(re.search(Nom_variable,cell,re.IGNORECASE)):
                #print("col : {}".format(col))
                variable = df_bilan.loc[i,col]
                #print(variable)
                if(variable == '' and i+1 < nb_lignes):

                    variable = df_bilan.loc[i+1,col]

                else :
                    return variable
    return 0

def prepare_data(liste):
    new_list = []
    spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–"]

    for element in liste:
        for char in spec_chars:
            element = str(element).replace(char,'')
            element = str(element).replace(" ","")
            
        new_list.append(element)
        
    
    new_list = list(map(float,new_list))
    return new_list
            

def get_data(pdf_path):

    

    var_Actifs = ["total.*actifs$",'total.*actifs courants$',
                    "liquidit[eé]s.*liquidit[eé]s","^stock.*",
                    "clients Et comptes Rattach[ée]s"]

    var_Passifs = ["^total.*capitaux.*propre.*","total.*passifs courants",
                    "total.*passifs non courants",
                    "fournisseurs et comptes rattach[eé]s"]


    var_Resultat = ["r[eé]sultat.*net","total.*produits d'exploitation","achats.*",
                            ".*amorti.*provisions",
                            "charges financi[èe]res nettes",'r[ée]sultat.*exploitation']


    var_CashFlow = ["flux de trésorerie.*[provenant|liée].*exploitation"]


    pagenbr = get_page(pdf_path)
    
    

    row = []
    page_actif =str(pagenbr)
    page_passif = str(pagenbr+1)
    page_res = str(pagenbr+2)
    page_cashFlow = str(pagenbr+3)
    all_pages = page_actif +','+ page_passif+',' + page_res+ ','+ page_cashFlow
    print(all_pages)
    tablesBilan2 = camelot.read_pdf(pdf_path,pages =all_pages ,flavor = "stream",edge_tol=2)
    
    #extrait les variable de la pages des actifs dans un dictionaire
    try : 
        
        for variable in var_Actifs:
            row.append(get_Variable(tablesBilan2[0].df,variable)) 
        #extrait les vairable de la page des passifs
        for variable in var_Passifs: 
            row.append(get_Variable(tablesBilan2[1].df,variable))
         #extrait les vairable de la page des resultats  
        for variable in var_Resultat: 
                row.append(get_Variable(tablesBilan2[2].df,variable))
            
        #extrait les vairable de la page des passifs    
        for variable in var_CashFlow: 
            row.append(get_Variable(tablesBilan2[3].df,variable))
        
    except Exception as e:
        print(e)
    
    #formatte les données
    row = prepare_data(row)

    #ajout les actifs non courants
    row.append(row[0] - row[1])

    imp_Bayes = IterativeImputer(max_iter=15, random_state=0,estimator = BayesianRidge())
    row = imp_Bayes.fit_transform([row])

    labels = ['total_des_actifs',
                'total_des_actifs_courant',
                'liquidités',
                'stocks',
                'clients Et comptes Rattachés',
                'capitaux_propres',
                'total_des_passifs_courants',
                'total_des_passifs_non_courants',
                'fournisseurs_et_comptes_rattachés',
                'résultat_net',
                'total_des_produits_exploitation',
                'dotations_aux_amortissements_et_aux_provisions',
                'charges financières nettes',
                'total des flux de trésorerie liés aux opérations exploitation',
                'total_des_actifs_non_courant'

                ]
    
    i = 0
    
    data = {}
    print(row)
    for label in labels :
            
        data[label] = row[0,i] 
            
        i += 1

    
    
        
    return data