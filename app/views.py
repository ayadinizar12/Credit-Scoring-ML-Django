





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
import app.ocr as ocr
import os
import joblib

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'form'

    #html_template = loader.get_template( 'form.html' )
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. A
    # nd load that template.

        
    load_template      = request.path.split('/')[-1] 
    context['segment'] = load_template
        
    html_template = loader.get_template( load_template )
    return HttpResponse(html_template.render(context, request))


def upload (request):    
        
    return render(request, 'ui-typography.html')

def result_pdf (request):
    ET_Model = joblib.load('final_model.sav')
    if(request.method == 'POST'):
        uploaded_file = request.FILES['document']
        
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        
        pdf_file = os.getcwd()+"\core\media\\"+name
        
        #extraction des données du fichier pdf
        data_dict =  ocr.get_data(pdf_file)
        

        RAF1 = data_dict['capitaux_propres']/data_dict['total_des_actifs']
        RAF2 = data_dict['capitaux_propres']/data_dict['total_des_passifs_non_courants']
        RFD = (data_dict['total_des_passifs_courants']+data_dict['total_des_passifs_courants'])/data_dict['total_des_actifs']
        RLG = data_dict['total_des_actifs_courant']/data_dict['total_des_passifs_courants']
        RLR = data_dict['fournisseurs_et_comptes_rattachés']+data_dict['liquidités']/data_dict['total_des_passifs_courants']
        RFI = (data_dict['capitaux_propres']+data_dict['total_des_passifs_non_courants'])/data_dict['total_des_actifs_non_courant']
        DPC = data_dict['fournisseurs_et_comptes_rattachés']/data_dict['total_des_produits_exploitation']*365
        RCP = data_dict['résultat_net']/data_dict['capitaux_propres']
        TRN = data_dict['résultat_net']/data_dict['total_des_produits_exploitation']
       
        

         #scoring
        Fonds_de_roulement=data_dict['capitaux_propres']+data_dict['total_des_passifs_courants']-data_dict['total_des_actifs_non_courant']
        charges_exploitation=data_dict['total_des_produits_exploitation']-data_dict['résultat_net']
        EBIT=data_dict['total_des_produits_exploitation']-charges_exploitation-data_dict['dotations_aux_amortissements_et_aux_provisions']
        total_des_passifs=data_dict['total_des_passifs_courants']+data_dict['total_des_passifs_non_courants']   
        A=float(Fonds_de_roulement)/data_dict['total_des_actifs']
        B=data_dict['résultat_net']/data_dict['total_des_actifs']

        C=float(EBIT)/data_dict['total_des_actifs']
        D=data_dict['capitaux_propres']/float(total_des_passifs)
        E=data_dict['total_des_produits_exploitation']/data_dict['total_des_actifs']
        scoring=1.2*float(A)+1.4*float(B)+3.3*float(C)+0.6*float(D)+1.0*float(E)




        lis = []



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
        lis.remove(RLR)
        rep = ''
        
        if ans == 1 :
            rep = "Your Client doesn't represent any risk"

        else :
            rep = "Your Client represents a risk "
            
        
        if scoring < 1.81 : 
            score = 'Your score is ', float(scoring) ,'lentreprise pourrait se diriger vers la faillite, la demande est refusee'
        
        elif  1.81 <= scoring < 2.99:  
            score = 'Your score is', float(scoring) ,'le risque est présent sans être très important, la demande est acceptee'
            
        else : 

            score = "Your score is :", str(scoring) , "le risque est présent sans être très important, la demande est acceptée"

    data_dict['approval'] = rep
    data_dict['score'] = score
    data_dict['lis'] = lis
    data_dict['scoring'] = scoring

    data_dict['RAF1'] = RAF1
    data_dict['RAF2'] = RAF2
    data_dict['RFD'] = RFD
    data_dict['RLG'] = RLG
    data_dict['RLR'] = RLR
    data_dict['RFI'] = RFI
    data_dict['DPC'] = DPC
    data_dict['RCP'] = RCP
    data_dict['TRN'] = TRN

    return render(request, 'result_pdf.html',data_dict)
   
