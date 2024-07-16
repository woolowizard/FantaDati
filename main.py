import json
import requests
import pandas as pd
import numpy as np

class FantaDati:

  def __init__(self):
    self.change_me = None
    
  # Metodo che prende gli id squadre dal campionato
  def get_teams_id(league):
    id_squadre = {}
    leagues_id1 = {'pl': 17, 'seriea': 23, 'laliga': 8}
    leagues_id2 = {'pl': 52186, 'seriea': 52760, 'laliga': 52376}
    url = f'https://www.sofascore.com/api/v1/unique-tournament/{leagues_id1[league]}/season/{leagues_id2[league]}/standings/total'
    response = requests.get(url)
    if response.status_code == 200:
      # Ottieni i dati in formato JSON
      risp = response.json()
      data = risp['standings'][0]
      data = data['rows']
      for i in data:
        id_squadre[i.get('team').get('name')] = i.get('team').get('id', None)
      return id_squadre
    else:
      return 'Errore nella chiamata HTTP'

  # Metodo che prende gli url dei giocatori per poi utilizzarli nel metodo get_player
  def get_urls(id_squadre):
    squadra_url = {}
    for squadra, id in id_squadre.items():
      url = "https://www.sofascore.com/api/v1/team/" + str(id) + "/players"
      squadra_url[squadra] = url
    return squadra_url
  
  # Metodo che prende gli id dei giocatori
  def get_players(squadra_url):
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
    
  # Metodo che prende le statistiche dei giocatori
  def get_stats(diz_finale):
    c = 0
    tot = 22
    df = pd.DataFrame()
    for squadra in diz_finale:
      c += 1
      rounded = round(c/tot, 2)
      print(f"Importazione dati di {squadra}. ", f"Importazione completata al {rounded * 100} %")
      for player in diz_finale[squadra]:
          team = squadra
          giocatore = player
          id = diz_finale[squadra][player]
          url = "https://www.sofascore.com/api/v1/player/" + str(id) + "/unique-tournament/23/season/52760/statistics/overall"
          response = requests.get(url)
          if response.status_code == 200:
            # Ottieni i dati in formato JSON
            risp = response.json()
            stats = risp['statistics']
            stats = {'player': giocatore, **stats}
            temp = pd.DataFrame([stats])
            df = pd.concat([df, temp], ignore_index=True)
    return df
    
  # Metodo che converte il dataframe in un csv pronto per l'analisi dati
  def csv(df):
    return df.to_csv('dati_fantacalcio.csv', index=False)
    
  # Metodo che in un colpo solo restituisce il csv del campionato desiderato
  def get_csv(campionato):
    id_squadre = FantaDati.get_teams_id(campionato)
    urls = FantaDati.get_urls(id_squadre)
    players = FantaDati.get_players(urls)
    data = FantaDati.get_stats(players)
    data_csv = FantaDati.csv(data)
    return data_csv
