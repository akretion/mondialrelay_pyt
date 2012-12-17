#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mondialrelay_pyt import MRWebService

connexion = MRWebService("MRT_2012")

dico = {
        'Enseigne':'BDTEST12',
        'ModeCol':'CCC',
        'ModeLiv':'LDS',
        'NDossier':'1234',
        'NClient':'123456789',
        'Expe_Langage':'FR',
        'Expe_Ad1':'M.KALIF',
        #'Expe_Ad2':,
        'Expe_Ad3':'rue dailleurs',
        #'Expe_Ad4':,
        'Expe_Ville':'hgzkh',
        'Expe_CP':'69100',
        'Expe_Pays':'FR',
        'Expe_Tel1':'0033445566778',
        #'Expe_Tel2':,
        #'Expe_Mail':,
        'Dest_Langage':'FR',
        'Dest_Ad1':'M.KALIF',
        ##'Dest_Ad2':,
        'Dest_Ad3':'414 BD DES CANUTS',
        #'Dest_Ad4':'etjebougeraipas',
        'Dest_Ville':'LYON',
        'Dest_CP':'69300',
        'Dest_Pays':'FR',
        'Dest_Tel1':'0033409887766',
        #'Dest_Tel2':,
        #'Dest_Mail':,
        'Poids':'30000',
        'Longueur':'145',
        #'Taille':,
        'NbColis':'1',
        'CRT_Valeur':'124',
        #'CRT_Devise':,
        #'EXP_Valeur':,
        #'EXP_Devise':,
        #'COL_Rel_Pays':,
        #'COL_Rel':,
        #'LIV_Rel_Pays':,
        #'LIV_Rel':,
        #'TAvisage':,
        #'TReprise':,
        #'Montage':,
        #'TRDV':,
        #'Assurance':,
        #'Instructions':,
        #'Texte':,
    }

#dico['ModeLiv'] = 'LDS'
#dico['ModeCol'] = 'CCC'

#print dico

response = '<?xml version="1.0" encoding="utf-8"?>\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"\
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
 xmlns:xsd="http://www.w3.org/2001/XMLSchema">\
<soap:Body><WSI2_CreationEtiquetteResponse\
 xmlns="http://www.mondialrelay.fr/webservice/">\
<WSI2_CreationEtiquetteResult><STAT>0</STAT>\
<ExpeditionNum>17193867</ExpeditionNum>\
<URL_Etiquette>/PDF/StickerMaker2.aspx?ens=BDTEST1211&amp;expedition=17193867&amp;lg=FR&amp;\
format=A4&amp;crc=9579B14BCF9FA5B894A27A952DD90CC7</URL_Etiquette>\
</WSI2_CreationEtiquetteResult></WSI2_CreationEtiquetteResponse></soap:Body></soap:Envelope>'



reqst = connexion.make_etiquette(dico)

