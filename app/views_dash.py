from django.http import HttpResponse
from django.shortcuts import render
import joblib


def result(request):

    ET_Model = joblib.load('final_model.sav')
    lis=[]


    #=request.GET['capitaux_propres'] 
    # total_des_actifs=request.GET['total_des_actifs']
    # total_des_actifs_courant=request.GET['total_des_actifs_courant']
    # total_des_actifs_non_courant=request.GET['total_des_actifs_non_courant']
    # total_des_passifs_courants=request.GET['total_des_passifs_courants']
    # total_des_passifs_non_courants=request.GET['total_des_passifs_non_courants']
    # fournisseurs_et_comptes_rattachés=request.GET['fournisseurs_et_comptes_rattachés']
    # liquidités=request.GET['liquidités']
    # résultat_net=request.GET['résultat_net']
    # total_des_produits_exploitation=request.GET['total_des_produits_exploitation']
    # dotations_aux_amortissements_et_aux_provisions=request.GET['dotations_aux_amortissements_et_aux_provisions']



    fond_roulement=request.GET['fond_roulement'] 
    total_des_actifs=request.GET['total_des_actifs'] 
    Bénefices_non_repartis=request.GET['Bénefices_non_repartis'] 
    Bénéfice_avant_intérêts_impôts=request.GET['Bénéfice_avant_intérêts_impôts'] 
    Valeur_marchande_capitaux_propres_A1=request.GET['Valeur_marchande_capitaux_propres_A1'] 
    Valeur_marchande_capitaux_propres_A2=request.GET['Valeur_marchande_capitaux_propres_A2'] 

    Total_passifs=request.GET['Total_passifs'] 
    Ventes_nettes=request.GET['Ventes_nettes'] 
 








    # RAF1=float(capitaux_propres)/float(total_des_actifs)
    # RAF2=float(capitaux_propres)/float(total_des_passifs_non_courants)
    # RFD=(float(total_des_passifs_courants)+float(total_des_passifs_courants))/float(total_des_actifs)
    # RLG=float(total_des_actifs_courant)/float(total_des_passifs_courants)
    # RLR=(float(fournisseurs_et_comptes_rattachés)+float(liquidités))/float(total_des_passifs_courants)
    # RFI=(float(capitaux_propres)+float(total_des_passifs_non_courants))/float(total_des_actifs_non_courant)
    # DPC=(float(fournisseurs_et_comptes_rattachés)/float(total_des_produits_exploitation))*365
    # RCP=(float(résultat_net)/float(capitaux_propres))
    # TRN=(float(résultat_net)/float(total_des_produits_exploitation))


    #scoring
  
    Moyenne_valeur_marchande_capitaux_propres=(float(Valeur_marchande_capitaux_propres_A1)+float(Valeur_marchande_capitaux_propres_A2))/2

   
   
    A=float(fond_roulement)/float(total_des_actifs)
    B=float(Bénefices_non_repartis)/float(total_des_actifs)

    C=float(Bénéfice_avant_intérêts_impôts)/float(total_des_actifs)
    D=float(Moyenne_valeur_marchande_capitaux_propres)/float(Total_passifs)
    E=float(Ventes_nettes)/float(total_des_actifs)
    scoring=1.2*float(A)+1.4*float(B)+3.3*float(C)+0.6*float(D)+1.0*float(E)








    lis.append(A)
    lis.append(B)
    lis.append(C)
    lis.append(D)
    lis.append(E)
   
    print(lis)

    ans=ET_Model.predict([lis])
    print(ans)
    
    if ans == 1 :
        rep = "Your Client doesn't represent any risk"

    else :
        rep = "Your Client represents a risk "
        
    
    if scoring < 1.81 : 
       score = 'Your score is ', float(scoring) ,'lentreprise pourrait se diriger vers la faillite, la demande est refusee'
       rep1='lentreprise pourrait se diriger vers la faillite, la demande est refusee'
    elif  1.81 <= scoring < 2.99:  
        score = 'Your score is', float(scoring) ,'le risque est présent sans être très important, la demande est acceptée'
        rep1='le risque est présent sans être très important, la demande est acceptée'
    else : 

        score = "Your score is :", str(scoring) , "le risque est présent sans être très important, la demande est acceptée"
        rep1= "le risque est présent sans être très important, la demande est acceptée"



    


    return render(request,'result.html',{'default_val':rep1,'score':score,'scoring':scoring,'lis':lis,
    'cfond_roulement':fond_roulement,'total_des_actifs':total_des_actifs,
    'Bénefices_non_repartis': Bénefices_non_repartis,'Bénéfice_avant_intérêts_impôts':Bénéfice_avant_intérêts_impôts,
    'Valeur_marchande_capitaux_propres_A1':Valeur_marchande_capitaux_propres_A1,
    'Valeur_marchande_capitaux_propres_A2':Valeur_marchande_capitaux_propres_A2,
     'Moyenne_valeur_marchande_capitaux_propres': Moyenne_valeur_marchande_capitaux_propres,
    'Total_passifs':Total_passifs,'Ventes_nettes':Ventes_nettes,'A':A,'B':B,'C':C,'D':D,
    'E': E,'scoring':scoring})

    
        

 
    
