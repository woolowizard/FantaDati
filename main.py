import json
import requests
import pandas as pd
import numpy as np

class FantaDati:

  def __init__(self):
    self.teams_url = None
  
  def get_urls(id_squadre):
    squadra_url = {}
    for squadra, id in id_squadre.items():
      url = "https://www.sofascore.com/api/v1/team/" + str(id) + "/players"
      squadra_url[squadra] = url
    return squadra_url
  
  def get_playes(squadra_url):
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
      
      return diz_finale
      
  
  def get_stats(diz_finale):
    c = 0
    tot = 22
    df = pd.DataFrame()
    for squadra in diz_finale:
      c += 1
      c = round(c/tot, 2)
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
      return df
    
  def csv(df):
    return df.to_csv('stats.csv', index=False)

####### SCRIPT #######

urls = FantaDati.get_urls(id_squadre)
players = FantaDati.get_playes(asd)
data = FantaDati.get_stats(players)
data_csv = csv(data)

