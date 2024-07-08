import json
import requests
import pandas as pd
import numpy as np

id_squadre = {'milan': 2692, 'inter': 2697, 'juventus': 2687, 'atalanta': 2686, 'bologna': 2685, 'roma': 2702, 'lazio': 2699, 'fiorentina': 2693,
              'torino': 2696, 'napoli': 2714, 'genoa': 2713, 'monza': 2729, 'verona': 2701, 'lecce': 2689, 'udinese': 2695, 'cagliari': 2719, 'empoli': 2705,
              'frosinone': 2801, 'sassuolo': 2793, 'salernitana': 2710}

squadra_url = {}

for squadra, id in id_squadre.items():
  url = "https://www.sofascore.com/api/v1/team/" + str(id) + "/players"
  squadra_url[squadra] = url

diz_finale = {}

for squadra, url in squadra_url.items():
  response = requests.get(url)
  tpd = {}
  if response.status_code == 200:
    data = response.json()
    data = data['players']
    for player in data:
      nested = player.get('player')
      tpd[nested.get('slug')] = nested.get('id')

    diz_finale[squadra] = tpd

  else:
      print(f"Errore nella richiesta: {response.status_code}")

  df = pd.DataFrame()
c = 0
tot = 22

for squadra in diz_finale:
  c += 1
  print(f"Importazione dati di {squadra}. ", f"Importazione completata al {c/tot}%")
  for player in diz_finale[squadra]:
    team = squadra
    giocatore = player
    id = diz_finale[squadra][player]
    #print(team, giocatore, id)
    url = "https://www.sofascore.com/api/v1/player/" + str(id) + "/unique-tournament/23/season/52760/statistics/overall"
    response = requests.get(url)
    if response.status_code == 200:
      # Ottieni i dati in formato JSON
      risp = response.json()
      #stats = risp['statistics']
      stats = risp['statistics']
      stats = {'player': giocatore, **stats}
      temp = pd.DataFrame([stats])
      df = pd.concat([df, temp], ignore_index=True)
      #print('Statistiche per: ', giocatore, stats)

df.to_csv('stats.csv', index=False) # pandas df to csv
