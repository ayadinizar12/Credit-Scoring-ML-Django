from django.http import HttpResponse
from django.shortcuts import render
import joblib


def result(request):

    ET_Model = joblib.load('final_model_br.sav')
    lis=[]


    capitaux_propres=request.GET['capitaux_propres']
    total_des_actifs=request.GET['total_des_actifs']
    total_des_actifs_courant=request.GET['total_des_actifs_courant']
    total_des_actifs_non_courant=request.GET['total_des_actifs_non_courant']
    total_des_passifs_courants=request.GET['total_des_passifs_courants']
    total_des_passifs_non_courants=request.GET['total_des_passifs_non_courants']
    fournisseurs_et_comptes_rattachés=request.GET['fournisseurs_et_comptes_rattachés']
    liquidités=request.GET['liquidités']
    résultat_net=request.GET['résultat_net']
    total_des_produits_exploitation=request.GET['total_des_produits_exploitation']
    dotations_aux_amortissements_et_aux_provisions=request.GET['dotations_aux_amortissements_et_aux_provisions']

    RAF1=float(capitaux_propres)/float(total_des_actifs)
    RAF2=float(capitaux_propres)/float(total_des_passifs_non_courants)
    RFD=(float(total_des_passifs_courants)+float(total_des_passifs_courants))/float(total_des_actifs)
    RLG=float(total_des_actifs_courant)/float(total_des_passifs_courants)
    RLR=(float(fournisseurs_et_comptes_rattachés)+float(liquidités))/float(total_des_passifs_courants)
    RFI=(float(capitaux_propres)+float(total_des_passifs_non_courants))/float(total_des_actifs_non_courant)
    DPC=(float(fournisseurs_et_comptes_rattachés)/float(total_des_produits_exploitation))*365
    RCP=(float(résultat_net)/float(capitaux_propres))
    TRN=(float(résultat_net)/float(total_des_produits_exploitation))


    #scoring
    Fonds_de_roulement=float(capitaux_propres)+float(total_des_passifs_courants)-float(total_des_actifs_non_courant)
    charges_exploitation=float(total_des_produits_exploitation)-float(résultat_net)
    EBIT=float(total_des_produits_exploitation)-float(charges_exploitation)-float(dotations_aux_amortissements_et_aux_provisions)
    total_des_passifs=float(total_des_passifs_courants)+float(total_des_passifs_non_courants)   
    A=float(Fonds_de_roulement)/float(total_des_actifs)
    B=float(résultat_net)/float(total_des_actifs)

    C=float(EBIT)/float(total_des_actifs)
    D=float(capitaux_propres)/float(total_des_passifs)
    E=float(total_des_produits_exploitation)/float(total_des_actifs)
    scoring=1.2*float(A)+1.4*float(B)+3.3*float(C)+0.6*float(D)+1.0*float(E)








    lis.append(RAF1)
    lis.append(RAF2)
    lis.append(RFD)
    lis.append(RLG)
    lis.append(RLR)
    lis.append(RFI)
    lis.append(DPC)
    lis.append(RCP)
    lis.append(TRN)
    print(lis)

    ans=ET_Model.predict([lis])
    print(ans)
    
    if ans == 1 :
        rep = "Your Client doesn't represent any risk"

    else :
        rep = "Your Client represents a risk "
        
    
    if scoring < 1.81 : 
       score = 'Your score is ', float(scoring) ,'the company might be headed for bankruptcy , the request  is denied'
       
    elif  1.81 <= scoring < 2.99:  
        score = 'Your score is', float(scoring) ,'the risk is present without being very important, the request  is accepted'
        
    else : 

        score = "Your score is :", str(scoring) , "the company is in solid financial positioning , the request  is accepted"
        




    


    return render(request,'result.html',{'approval':rep,'score':score,'scoring':scoring,'lis':lis,'capitaux_propres':capitaux_propres,'total_des_actifs':total_des_actifs,
    'total_des_actifs_courant': total_des_actifs_courant,'total_des_actifs_non_courant':total_des_actifs_non_courant,
    'total_des_passifs_courants':total_des_passifs_courants,'total_des_passifs_non_courants':total_des_passifs_non_courants,
    'liquidités':liquidités,'fournisseurs_et_comptes_rattachés':fournisseurs_et_comptes_rattachés,'résultat_net':résultat_net,
    'total_des_produits_exploitation':total_des_produits_exploitation,'RAF1':RAF1,'RAF2':RAF2,'RFD':RFD,'RLG':RLG,
    'RLR': RLR,'RFI':RFI,'DPC':DPC,'RCP':RCP,'TRN':TRN,'scoring':scoring})

   

    
    
    
        

 
    
