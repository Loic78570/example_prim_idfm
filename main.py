# ==============================================================================
# Requête de l’API Prochains Passages de source Ile-de-France Mobilités -
# unitaire
# coding: utf8
# ==============================================================================
import datetime
import locale

import secrets

locale.setlocale(locale.LC_ALL, 'fr_FR')

import dateutil.tz
from dateutil import parser
import requests
from colorama import Back, Style, Fore

CDG_RER_A = 'STIF:StopPoint:Q:58759:'
CDG_2 = 'STIF:StopPoint:Q:473923:'
CDG_ETOILE_METRO_2 = 'STIF:StopPoint:Q:22094:'
CDG_ETOILE_METRO_9 = 'STIF:StopPoint:Q:463043:'
CFO_RER_A = 'STIF:StopPoint:Q:471418:'
CONFLANS_FIN_D_OISE = 'STIF:StopPoint:Q:411350:'
LA_DEFENSE_RER_A = 'STIF:StopPoint:Q:473935:'
LA_DEFENSE_RER_A2 = 'STIF:StopPoint:Q:473936:'
LA_DEFENSE_RER_AX = 'STIF:StopPoint:Q:470549:'
LA_DEFENSE_METRO_1 = 'STIF:StopPoint:Q:473937:'
CDG_ETOILE_6 = 'STIF:StopPoint:Q:22095:'
CDG_RERB = 'STIF:StopPoint:Q:477638:'

# URL de l'API Prochains Passages de source IDFM - requête unitaire
url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring'
# Le header doit contenir la clé API : apikey, veuillez remplacer #VOTRE CLE API
# par votre clé API
headers = {'Accept': 'application/json', 'apikey': secrets.api}
# Envoi de la requête au serveur
print(f"{Fore.LIGHTCYAN_EX}Queryring...", end=' ')
req = requests.get(url, headers=headers, params={'MonitoringRef': CDG_2})
print(f"Done.{Fore.RESET}")

print('Status:', req)
open('reponse.json', 'wb').write(req.content)
req_json = req.json()
valz = req.json()['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
newlist = sorted(valz, key=lambda d: d['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime'])

# newlist = valz
if newlist == []:
    print("Aucun train n'est prévu à intervalle d'une heure.")
    exit(0)
for x in newlist:
    # print()
    vehicle = x['MonitoredVehicleJourney']
    # print(vehicle)

    try:
        datetrain = datetime.datetime.strptime(vehicle['MonitoredCall']['ExpectedArrivalTime'],
                                               "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    except KeyError:
        try:
            datetrain = datetime.datetime.strptime(vehicle['MonitoredCall']['AimedArrivalTime'],
                                                   "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        except KeyError:
            datetrain = datetime.datetime.strptime(vehicle['MonitoredCall']['AimedDepartureTime'],
                                                   "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    # print(datetrain)
    # print((datetrain > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)))

    # print("Hi!")

    if not (datetrain > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)):
        pass

    # print("test : ", vehicle['LineRef']['value'] in ("STIF:Line::C01739:", "STIF:Line::C01742:", "STIF:Line::C01740"))
    # if (vehicle['LineRef']['value'] not in (
    # "STIF:Line::C01739:", "STIF:Line::C01742:", "STIF:Line::C01740", "STIF:Line::C01376:")):
    #     continue
    # print("test2 : ", vehicle['LineRef']['value'] in ("STIF:Line::C01739:", "STIF:Line::C01742:", "STIF:Line::C01740"))
    # print(vehicle['JourneyNote'])

    try:
        train_name = vehicle['JourneyNote'][0]['value']

    except IndexError:
        train_name = None

    dest_name = vehicle['DestinationName'][0]['value']
    line_ref = vehicle['LineRef']['value']
    call_array = vehicle['MonitoredCall']

    # print("AllPassing")

    # try:
    date_dept = dateutil.parser.parser().parse(timestr=call_array['ExpectedDepartureTime'],
                                               tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
        .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    # except KeyError:
    #     try:
    #         date_dept = dateutil.parser.parser().parse(timestr=call_array['ExpectedDepartureTime'],
    #                                                    tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
    #             .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    #     except KeyError:
    #         pass
    try:
        full_code = vehicle['JourneyNote'][0]['value']
    except IndexError:
        try:
            full_code = vehicle['TrainNumbers']['TrainNumberRef'][0]['value']
        except IndexError:
            full_code = None

    try:
        date_pass = dateutil.parser.parser().parse(timestr=call_array['ExpectedArrivalTime'],
                                                   tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
            .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
    except KeyError:
        try:
            date_pass = dateutil.parser.parser().parse(timestr=call_array['AimedArrivalTime'],
                                                       tzinfos={'Z': dateutil.tz.gettz('Europe/London')}) \
                .astimezone(tz=dateutil.tz.gettz('Europe/Paris'))
        except KeyError:
            # date_pass = date_dept
            pass
    time_diff = (date_pass - datetime.datetime.now(tz=dateutil.tz.gettz('Europe/Paris')))

    #CanWeShowTheTrain
    if (not (date_pass > datetime.datetime.now(tz=dateutil.tz.gettz('Europe/Paris')))
            and not (date_dept > datetime.datetime.now(tz=dateutil.tz.gettz('Europe/Paris')))):
        continue

    # print("DatesPassing")

    if True:
        print(f"[{full_code}]", end=" ")
        # if train_name == "UZEL":
        #     print(
        #         f"Le {Fore.LIGHTRED_EX}{'RER (A)': <10}{Fore.RESET}",
        #         end=' ')
        if line_ref == "STIF:Line::C01742:": # RER A
            print(
                f"Le {Fore.LIGHTRED_EX}{'RER (A)': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01372:": # Métro 2
            print(
                f"Le {Fore.LIGHTGREEN_EX}{'Métro (2)': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01739:": # Ligne J
            print(
                f"La {Fore.LIGHTGREEN_EX}{'Ligne [J]': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01740:": # Ligne L
            print(
                f"La {Fore.LIGHTMAGENTA_EX}{'Ligne [L]': <10}{Fore.RESET}",
                end=' ')
        elif line_ref == "STIF:Line::C01376:": # Métro 6
            print(
                f"La {Fore.LIGHTGREEN_EX}{'Métro (6)': <10}{Fore.RESET}",
                end=' ')
        else:
            print(
                f"Le {Fore.LIGHTRED_EX}{'Train (non rec)': <10}{Fore.RESET}",
                end=' ')

        print(f" à destination de {Back.BLACK}{dest_name: <30}{Back.RESET}", end=' ')
        # if date_pass:
        #     print(f"passera en gare à {date_pass.strftime('%A %d/%m/%Y %H:%M:%S')}", end=' ')
        if date_dept:
            try:
                print(f"\n\t\t>>> Voie {call_array['ArrivalPlatformName']['value']}", end=' ')
            except KeyError:
                print(f"\n\t\t>>> Voie non renseignée", end=' ')
            print(f"\n\t\t>>> {Fore.CYAN}{date_pass.strftime('%A %d %B %Y à %H:%M').lower()}{Fore.RESET} >>", end=' ')

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


        req2 = requests.get("https://prim.iledefrance-mobilites.fr/marketplace/general-message",
                            headers={'Accept': 'application/json', 'apikey': secrets.api},
                            params={'LineRef': line_ref})
        errs = req2.json()['Siri']['ServiceDelivery']['GeneralMessageDelivery']
        # for err in errs:
        #     infoMessage = err['InfoMessage']
        #     try:
        #         for info in infoMessage:
        #             msgs = info['Content']['Message']
        #             for msg in msgs:
        #                 print(f"{Back.LIGHTYELLOW_EX}{Fore.BLACK} {msg['MessageType']} 📣 :{Back.RESET}{Fore.RESET}")
        #                 print(f"{Back.BLACK}{msg['MessageText']['value']}{Fore.RESET}")
        #         print()
        #     except AttributeError:
        #         pass
        # print(f"(dans {time_diff.seconds//3600, (time_diff.seconds//60)%60} minutes)")
# print((x for x in req.json()['Siri']))
