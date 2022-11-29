# ==============================================================================
# Requête de l’API Prochains Passages de source Ile-de-France Mobilités -
# unitaire
# coding: utf8
# ==============================================================================
import datetime
import locale

import secrets

locale.setlocale(locale.LC_TIME, '')

import dateutil.tz
from dateutil import tz, parser
from requests.auth import HTTPBasicAuth
import requests
from colorama import Back, Style, Fore
from dateutil import parser

# URL de l'API Prochains Passages de source IDFM - requête unitaire
url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring'
# Le header doit contenir la clé API : apikey, veuillez remplacer #VOTRE CLE API
# par votre clé API
headers = {'Accept': 'application/json', 'apikey': secrets.api}
# Envoi de la requête au serveur
req = requests.get(url, headers=headers, params={'MonitoringRef': 'STIF:StopPoint:Q:43114:'})
# Affichage du code réponse
print('Status:', req)
# Affichage du contenu de la réponse
# print(req.content)
req_json = req.json()
valz = req.json()['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
for x in valz:
    train_name = x['MonitoredVehicleJourney']['JourneyNote'][0]['value']
    dest_name = x['MonitoredVehicleJourney']['DestinationName'][0]['value']

    call_array = x['MonitoredVehicleJourney']['MonitoredCall']
    date_pass = dateutil.parser.parser().parse(timestr=call_array['ExpectedArrivalTime'],
                                               tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
        .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    time_diff = (date_pass - datetime.datetime.now(tz=dateutil.tz.gettz('Europe/Paris')))
    if time_diff.seconds // 60 < 60:
        if train_name == "UZEL":
            print(
                f"Le {Fore.LIGHTRED_EX}RER (A){Fore.RESET} à destination de Cergy passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')} (dans {time_diff.seconds // 60} minutes)")
        elif train_name == "MOCA":
            print(
                f"Le {Fore.LIGHTMAGENTA_EX}Transillien [L]{Fore.RESET} à destination de Mantes la Jolie passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')} (dans {time_diff.seconds // 60} minutes)")
        elif train_name == "PUCA":
            print(
                f"Le {Fore.LIGHTMAGENTA_EX}Transillien [L]{Fore.RESET} à destination de Paris-Saint-Lazare passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')} (dans {time_diff.seconds // 60} minutes)")
        elif train_name == "NANI":
            print(
                f"Le {Fore.LIGHTRED_EX}RER (A){Fore.RESET} à destination de Paris (Boissy, etc) passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')} (dans {time_diff.seconds // 60} minutes)")
        else:
            print(f"Le {Fore.LIGHTRED_EX}RER (A){Fore.RESET} à destination de Paris (Boissy, etc) passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')} (dans {time_diff.seconds // 60} minutes)")
# print((x for x in req.json()['Siri']))
# Ecriture de la réponse reçue sur un fichier
open('Reponse.json', 'wb').write(req.content)
