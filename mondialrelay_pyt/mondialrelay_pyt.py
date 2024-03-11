#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
#
#    mondialrelaiy_pyt
#    (Mondial Relay Python)
#
#    Copyright (C) 2012 Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""

    mondialrelay_pyt is a Python library made to interact with
    the Mondial Relay's Web Service API : WSI2_CreationEtiquette
    (http://www.mondialrelay.fr/webservice/WSI2_CreationEtiquette)

    It takes a dictionnary of values required and the format of label wanted
    and gives the tracking number, and the url to donwload the label in pdf.

"""

__author__ = "Sébastien BEAU / Aymeric LECOMTE"
__version__ = "0.1.0"
__date__ = "2012-12-06"

from unidecode import unidecode # Debian package python-unidecode


#-----------------------------------------#
#               LIBRARIES                 #
#-----------------------------------------#

from lxml import etree, objectify
from hashlib import md5
from requests.auth import HTTPBasicAuth
import requests
import re
import collections


#-----------------------------------------#
#               CONSTANTS                 #
#-----------------------------------------#

HOST= 'api.mondialrelay.com'
ENCODE = b'<?xml version="1.0" encoding="utf-8"?>'

#TODO add error code after the regex to use it in the raise
#('Enseigne',{"^[0-9A-Z]{2}[0-9A-Z]{6}$" : 30}),
MR_KEYS = collections.OrderedDict([
    ('Enseigne',"^[0-9A-Z]{2}[0-9A-Z]{6}$"),
    ('ModeCol',"^(CCC|CDR|CDS|REL)$"),
    ('ModeLiv',"^(LCC|LD1|LDS|24R|ESP|DRI)$"),
    ('NDossier',"^(|[0-9A-Z_ -]{0,15})$"),
    ('NClient',"^(|[0-9A-Z]{0,9})$"),
    ('Expe_Langage',"^[A-Z]{2}$"),
    ('Expe_Ad1',"^.{2,32}$"),
    ('Expe_Ad2',"^.{0,32}$"),
    ('Expe_Ad3',"^.{2,32}$"),
    ('Expe_Ad4',"^.{0,32}$"),
    ('Expe_Ville',"^[A-Z_\-' ]{2,26}$"),
    ('Expe_CP',"^[0-9]{5}$"),
    ('Expe_Pays',"^[A-Z]{2}$"),
    ('Expe_Tel1',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Expe_Tel2',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Expe_Mail',"^[\w\-\.\@_]{7,70}$"),
    ('Dest_Langage',"^[A-Z]{2}$"),
    ('Dest_Ad1',"^.{2,32}$"),
    ('Dest_Ad2',"^.{0,32}$"),
    ('Dest_Ad3',"^.{2,32}$"),
    ('Dest_Ad4',"^.{0,32}$"),
    ('Dest_Ville',"^[0-9A-Z_\-'., /]{0,32}$"),
    ('Dest_CP',"^[0-9]{5}$"),
    ('Dest_Pays',"^[A-Z]{2}$"),
    ('Dest_Tel1',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Dest_Tel2',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Dest_Mail',"^[\w\-\.\@_]{7,70}$"),
    ('Poids',"^[0-9]{3,7}$"),
    ('Longueur',"^[0-9]{0,3}$"),
    ('Taille',"^{0}$"),
    ('NbColis',"^[0-9]{1,2}$"),
    ('CRT_Valeur',"^[0-9]{1,7}$"),
    ('CRT_Devise',"^(|EUR)$"),
    ('EXP_Valeur',"^[0-9]{0,7}$"),
    ('EXP_Devise',"^(|EUR)$"),
    ('COL_Rel_Pays',"^[A-Z]{2}$"),
    ('COL_Rel',"^(|[0-9]{6})$"),
    ('LIV_Rel_Pays',"^[A-Z]{2}$"),
    ('LIV_Rel',"^(|[0-9]{6})$"),
    ('TAvisage',"^(|O|N)$"),
    ('TReprise',"^(|O|N)$"),
    ('Montage',"^(|[0-9]{1,3})$"),
    ('TRDV',"^(|O|N)$"),
    ('Assurance',"^(|[0-9A-Z]{1})$"),
    ('Instructions',"^[0-9A-Z_\-'., /]{0,31}"),
    ('Texte',"^([^<>&']{3,30})(\(cr\)[^<>&']{0,30})")
    ])

API_ERRORS_MESSAGE = {
    1 : u"Enseigne invalide",
    2 : u"Numéro d'enseigne vide ou inexistant",
    3 : u"Numéro de compte enseigne invalide",
    5 : u"Numéro de dossier enseigne invalide",
    7 : u"Numéro de client enseigne invalide",
    8 : u"Mot de passe ou hachage invalide",
    9 : u"Ville non reconnu ou non unique",
    10 : u"Type de collecte invalide",
    11 : u"Numéro de Relais de Collecte invalide",
    12 : u"Pays de Relais de collecte invalide",
    13 : u"Type de livraison invalide",
    14 : u"Numéro de Relais de livraison invalide",
    15 : u"Pays de Relais de livraison invalide",
    20 : u"Poids du colis invalide",
    21 : u"Taille (Longueur + Hauteur) du colis invalide",
    22 : u"Taille du Colis invalide",
    24 : u"Numéro d'expédition ou de suivi invalide",
    26 : u"Temps de montage invalide",
    27 : u"Mode de collecte ou de livraison invalide",
    28 : u"Mode de collecte invalide",
    29 : u"Mode de livraison invalide",
    30 : u"Adresse (L1) invalide",
    31 : u"Adresse (L2) invalide",
    33 : u"Adresse (L3) invalide",
    34 : u"Adresse (L4) invalide",
    35 : u"Ville invalide",
    36 : u"Code postal invalide",
    37 : u"Pays invalide",
    38 : u"Numéro de téléphone invalide, modifier le numéro sur l'adresse de l'expédition (il peut manquer un '+')",
    39 : u"Adresse e-mail invalide",
    40 : u"Paramètres manquants",
    42 : u"Montant CRT invalide",
    43 : u"Devise CRT invalide",
    44 : u"Valeur du colis invalide",
    45 : u"Devise de la valeur du colis invalide",
    46 : u"Plage de numéro d'expédition épuisée",
    47 : u"Nombre de colis invalide",
    48 : u"Multi-Colis Relais Interdit",
    49 : u"Action invalide",
    60 : u"Champ texte libre invalide (Ce code erreur n'est pas invalidant)",
    61 : u"Top avisage invalide",
    62 : u"Instruction de livraison invalide",
    63 : u"Assurance invalide",
    64 : u"Temps de montage invalide",
    65 : u"Top rendez-vous invalide",
    66 : u"Top reprise invalide",
    67 : u"Latitude invalide",
    68 : u"Longitude invalide",
    69 : u"Code Enseigne invalide",
    70 : u"Numéro de Point Relais invalide",
    71 : u"Nature de point de vente non valide",
    74 : u"Langue invalide",
    78 : u"Pays de Collecte invalide",
    79 : u"Pays de Livraison invalide",
    80 : u"Code tracing : Colis enregistré",
    81 : u"Code tracing : Colis en traitement chez Mondial Relay",
    82 : u"Code tracing : Colis livré",
    83 : u"Code tracing : Anomalie",
    84 : u"(Réservé Code Tracing)",
    85 : u"(Réservé Code Tracing)",
    86 : u"(Réservé Code Tracing)",
    87 : u"(Réservé Code Tracing)",
    88 : u"(Réservé Code Tracing)",
    89 : u"(Réservé Code Tracing)",
    93 : u"Aucun élément retourné par le plan de tri Si vous effectuez une "
        u"collecte ou une livraison en Point Relais, vérifiez que les Point "
        u"Relaissont bien disponibles. Si vous effectuez une livraison à domicile, "
        u"il est probable que le codepostal que vous avez indiquez n'existe pas.",
    94 : u"Colis Inexistant",
    95 : u"Compte Enseigne non activé",
    96 : u"Type d'enseigne incorrect en Base",
    97 : u"Clé de sécurité invalide Cf. : § « Génération de la clé de sécurité »",
    98 : u"Erreur générique (Paramètres invalides) Cette erreur masque une autre "
        u"erreur de la liste et ne peut se produire que dans le cas où le "
        u"compte utilisé est en mode « Production »."
        u" Cf. : § « Fonctionnement normal et debugage »",
    99 : u"Erreur générique du service Cette erreur peut être dû à un problème "
        u"technique du service. Veuillez notifier cette erreur à Mondial Relay en "
        u"précisant la date et l'heure de la requête ainsi que les paramètres "
        u"envoyés afin d'effectuer une vérification.",
}

#------------------------------------------#
#       Mondial Relay WEBService           #
#        WSI2_CreationEtiquette            #
#------------------------------------------#

class MRWebService(object):

    def __init__(self, security_key):
        self.security_key = security_key

    def valid_dict(self, dico):
        ''' Get a dictionnary, check if all required fields are provided,
        and if the values correpond to the required format.'''

        mandatory = [
            'Enseigne',
            'ModeCol',
            'ModeLiv',
            'Expe_Langage',
            'Expe_Ad1',
            'Expe_Ad3',
            'Expe_Ville',
            'Expe_CP',
            'Expe_Pays',
            'Expe_Tel1',
            'Dest_Langage',
            'Dest_Ad1',
            'Dest_Ad3',
            'Dest_Ville',
            'Dest_CP',
            'Dest_Pays',
            'Poids',
            'NbColis',
            'CRT_Valeur',
            ]


        if ('ModeLiv' or 'ModeCol') not in dico:
            raise Exception('The given dictionnary is not valid.')

        for element in dico:
            if element not in MR_KEYS:
                raise Exception('Key %s not valid in given dictionnary' %element)
            formt = MR_KEYS[element]
            #if dico[element] and re.match(formt, dico[element].upper()) == None:
            #    raise Exception('Value %s not valid in given dictionary, key %s, expected format %s' %(dico[element],element, MR_KEYS[element]))

        if dico['ModeLiv'] == "24R":
            mandatory.insert(19,'LIV_Rel')
            mandatory.insert(19,'LIV_Rel_Pays')
        if dico['ModeCol'] == "REL":
            mandatory.insert(19,'COL_Rel')
            mandatory.insert(19,'COL_Rel_Pays')
        if dico['ModeLiv'] == "LDS":
            mandatory.insert(16,'Dest_Tel1')

        for mandatkey in mandatory:
            if mandatkey not in dico:
                raise Exception('Mandatory key %s not given in the dictionnary' %mandatkey)

        return True

    #------------------------------------#
    #      functions to clean the xml    #
    #------------------------------------#

    def clean_xmlrequest(self, xml_string):
        ''' [XML REQUEST]
        Ugly hardcode to get ride of specifics headers declarations or namespaces instances.
        Used in the xml before sending the request.
        See http://lxml.de/tutorial.html#namespaces or http://effbot.org/zone/element-namespaces.htm
        to improve the library and manage namespaces properly '''

        env=b'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'+b' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'+b' xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        wsietiq=b'<WSI2_CreationEtiquette xmlns="http://www.mondialrelay.fr/webservice/">'

        str1 = xml_string.replace(b'soapBody',b'soap:Body').replace(b'soapEnvelope',b'soap:Envelope')
        str2 = str1.replace(b'<soap:Envelope>',env)
        str3 = str2.replace(b'<WSI2_CreationEtiquette>',wsietiq)

        return str3

    def clean_xmlresponse(self, xml_string):
        ''' [XML RESPONSE]
        Ugly hardcode to get ride of specifics headers declarations or namespaces instances.
        Used in the xml after receiving the response.
        See http://lxml.de/tutorial.html#namespaces or http://effbot.org/zone/element-namespaces.htm
        to improve the library and manage namespaces properly '''

        head = b' xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
        env = b'soap:Envelope'
        body= b'soap:Body'
        xmlns=b' xmlns="http://www.mondialrelay.fr/webservice/"'

        str1 = xml_string.replace(head,b'').replace(env,b'soapEnvelope').replace(body,b'soapBody').replace(xmlns,b'')
        str2 = str1.replace(ENCODE,b'')

        return str2

    #------------------------------------#
    #    functions to manage the xml     #
    #------------------------------------#

    def create_xmlrequest(self, vals):
        '''[XML REQUEST]
        Creates an xml tree fitted to the soap request to WSI2_CreationEtiquette,
        from the given dictionnary. All dictionnary's keys must correspond to a field to pass.

        IN = Dictionnary
        OUT = XML (as an utf-8 encoded string) ready to send a request '''

        #check if the given dictionnary is correct to make an xml
        mandat_dic = MRWebService.valid_dict(self, vals)

        #initialisation of future md5key
        security = ""

        # beginning of the xml tree, to be modified later with soapclean_xml()
        envl = etree.Element('soapEnvelope')
        body = etree.SubElement(envl, 'soapBody')
        wsi2_crea = etree.SubElement(body,'WSI2_CreationEtiquette')

        # xml elements creation
        for key in MR_KEYS:
           if key != 'Texte':
                xml_element = etree.SubElement(wsi2_crea,key)
                xml_element.text = vals.get(key, '')
                security += vals.get(key,'')

        # generates <Security/> xml element
        security+=self.security_key
        md5secu = md5(security.encode('utf-8')).hexdigest().upper()

        xml_security = etree.SubElement(wsi2_crea, "Security" )
        xml_security.text = md5secu

        # add <Text/> last xml element if present, not included in security key
        if 'Texte' in vals:
            xml_element = etree.SubElement(wsi2_crea,"Texte")
            xml_element.text = vals['Texte']

        # generates and modifies the xml tree to obtain an apropriate xml soap string
        xmltostring = etree.tostring(envl, encoding='utf-8', pretty_print=True)
        xmlrequest = MRWebService.clean_xmlrequest(self,xmltostring)
        return xmlrequest

    def sendsoaprequest(self, xml_string, store):
        ''' Send the POST request to the Web Service.
        IN = proper xml-string
        OUT = response from the Web Service, in an xml-string utf-8'''

        header = {
            'POST': '/Web_Services.asmx',
            'Host': HOST,
            'Content-Type': 'text/xml',
            'charset': 'utf-8',
            'Content-Lenght': 'Lenght',
            'SOAPAction': 'http://www.mondialrelay.fr/webservice/WSI2_CreationEtiquette',
        }
        
        url="https://api.mondialrelay.com/Web_Services.asmx"
        response=requests.post(url,headers=header, data=xml_string, auth=(store,self.security_key))

        return response.content

    def parsexmlresponse(self,soap_response):
        ''' Parse the response given by the WebService.
        Extract and returns all fields' datas.
        IN = xml-string utf-8 returned by Mondial Relay
        OUT : Dictionnary or Error'''

        strresp = soap_response
        strresp = strresp.replace(ENCODE,b'')
        tree= etree.fromstring(strresp)
        string = etree.tostring(tree, pretty_print=True, encoding='utf-8')

        response =  MRWebService.clean_xmlresponse(self, soap_response)
        soapEnvelope = objectify.fromstring(response)

        #---------------Parsing---------------#
        stat = soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.STAT

        if stat == 0:
            NumExpe = soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.ExpeditionNum
            urlpdf = 'http://'+HOST+str(soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.URL_Etiquette)
            resultat={'STAT':stat,'ExpeditionNum':NumExpe,'URL_Etiquette':urlpdf}
        else:
            resultat={'STAT':stat}
            explanation = API_ERRORS_MESSAGE.get(stat)
            raise Exception('The server returned %s . The mondial relay documentation says %s' % (stat,explanation))

        return resultat
        #TOFIX ?
        return True

    #------------------------------------#
    #       FUNCTION TO CALL             #
    #------------------------------------#
    def make_shipping_label(self, dictionnary, labelformat="A4"):
        ''' FUNCTION TO CALL TO GET DATAS WANTED FROM THE WEB SERVICE
        IN = Dictionnary with corresponding keys (see MR_Keys or Mondial Relay's Documentation)
        OUT = Raise an error with indications (see MR Doc for numbers correspondances)
        or Expedition Number and URL to PDF'''

        #MondialRelay api required only ascii in uppercase
        for key in dictionnary:
            dictionnary[key] = unidecode(dictionnary[key]).upper()

        xmlstring = MRWebService.create_xmlrequest(self, dictionnary)

        storename=dictionnary['Enseigne']
        resp = MRWebService.sendsoaprequest(self,xmlstring, storename)

        print (resp)

        result = MRWebService.parsexmlresponse(self,resp)
        url = result['URL_Etiquette']

        #switch url if default format is not A4
        if labelformat == 'A5':
            url = url.replace('format=A4','format=A5')
        if labelformat == '10x15':
            url = url.replace('format=A4','format=10x15')

        final = {
                'ExpeditionNum': result['ExpeditionNum'],
                'URL_Etiquette': url,
                'format':labelformat,
                }

        return final

