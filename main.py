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
print(f"{Fore.LIGHTCYAN_EX}Queryring...", end=' ')
req = requests.get(url, headers=headers, params={'MonitoringRef': 'STIF:StopPoint:Q:43114:'})
print(f"Done.{Fore.RESET}")
# cfo : 43114
# cdg etoile rer A : 58759
# cdg etoile 22094 , 463043
# rer la def 473935 | 473936
# Affichage du code réponse
print('Status:', req)
# Affichage du contenu de la réponse
# print(req.content)
# Ecriture de la réponse reçue sur un fichier
open('Reponse.json', 'wb').write(req.content)
req_json = req.json()
valz = req.json()['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
# newlist = sorted(valz, key=lambda d: d['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'])
newlist = valz
if newlist == []:
    print("Aucun train n'est prévu à intervalle d'une heure.")
    exit(0)
for x in newlist:
    vehicle = x['MonitoredVehicleJourney']

    train_name = vehicle['JourneyNote'][0]['value']
    dest_name = vehicle['DestinationName'][0]['value']
    line_ref = vehicle['LineRef']['value']
    call_array = vehicle['MonitoredCall']
    try:
        date_dept = dateutil.parser.parser().parse(timestr=call_array['AimedDepartureTime'],
                                                   tzinfos={'Z': dateutil.tz.gettz('Europe/London')})\
                .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    except KeyError:
        try:
            date_dept = dateutil.parser.parser().parse(timestr=call_array['ExpectedDepartureTime'],
                                                       tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
                .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
        except KeyError:
            pass
    try:
        full_code = vehicle['VehicleJourneyName'][0]['value']
    except KeyError:
        try:
            full_code = vehicle['TrainNumbers']['TrainNumberRef'][0]['value']
        except KeyError:
            full_code = None

    try:
        date_pass = dateutil.parser.parser().parse(timestr=call_array['ExpectedArrivalTime'],
                                                   tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
            .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    except KeyError:
        try:
            date_pass = dateutil.parser.parser().parse(timestr=call_array['AimedArrivalTime'],
                                                   tzinfos={'Z': dateutil.tz.gettz('Europe/London')})\
                .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
        except KeyError:
            # date_pass = date_dept
            pass
    time_diff = (date_pass - datetime.datetime.now(tz=dateutil.tz.gettz('Europe/Paris')))

    if time_diff.seconds // 60 < 60 or (abs(time_diff.total_seconds()) < 60 and call_array['VehicleAtStop']):
        print(f"[{full_code}]", end=" ")
        # if train_name == "UZEL":
        #     print(
        #         f"Le {Fore.LIGHTRED_EX}{'RER (A)': <10}{Fore.RESET}",
        #         end=' ')
        if line_ref == "STIF:Line::C01742:":
            print(
                f"Le {Fore.LIGHTRED_EX}{'RER (A)': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01372:":
            print(
                f"Le {Fore.LIGHTGREEN_EX}{'Métro (2)': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01739:":
            print(
                f"La {Fore.LIGHTGREEN_EX}{'Ligne [J]': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01740:":
            print(
                f"La {Fore.LIGHTMAGENTA_EX}{'Ligne [L]': <10}{Fore.RESET}",
                end=' ')
        else:
            print(
                f"Le {Fore.LIGHTRED_EX}{'Train (non rec)': <10}{Fore.RESET}",
                end=' ')

        print(f" à destination de {Back.BLACK}{dest_name: <30}{Back.RESET}", end=' ')
        if date_pass:
            print(f"passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')}", end=' ')
        elif date_dept:
            print(f"partira en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')}", end=' ')

        # time
        if call_array['VehicleAtStop']:
            print(Fore.LIGHTCYAN_EX + "Train à quai" + Fore.RESET)
        elif time_diff.seconds < 60:
            print(f"{Fore.RED}(À l'approche...){Fore.RESET}")
        # elif time_diff.seconds > 60:
        else:
            if time_diff.seconds < 300:
                print(Style.BRIGHT + Fore.LIGHTRED_EX, end='')
            print(f"(dans {(time_diff.seconds // 3600) * 60 + (time_diff.seconds // 60) % 60} minutes)")
            print(Style.RESET_ALL, end='')
        # print(f"(dans {time_diff.seconds//3600, (time_diff.seconds//60)%60} minutes)")
# print((x for x in req.json()['Siri']))
