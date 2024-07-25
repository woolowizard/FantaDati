import json
import requests
import pandas as pd
import numpy as np
from urllib.error import HTTPError

class FantaDati:

  def __init__(self):
    self.league = None # Commentalo
    self.urls = None # Commentalo
    self.players = None # Dictionary with {'player_name': id}
    self.data = None # Commentalo
    
  def get_teams_id(self, league):
    self.league = league
    id_squadre = {}
    leagues_id1 = {'pl': 17, 'seriea': 23, 'laliga': 8}
    leagues_id2 = {'pl': 52186, 'seriea': 52760, 'laliga': 52376}
    url = f'https://www.sofascore.com/api/v1/unique-tournament/{leagues_id1[self.league]}/season/{leagues_id2[self.league]}/standings/total'
    response = requests.get(url)
    if response.status_code == 200:
      risp = response.json()
      data = risp['standings'][0]['rows']
      for i in data:
        id_squadre[i.get('team').get('name')] = i.get('team').get('id', None)
      return id_squadre
    else:
      raise Exception('Errore nella chiamata HTTP') 

  def get_urls(self, id_squadre):
    self.urls = {squadra: f"https://www.sofascore.com/api/v1/team/{id}/players" for squadra, id in id_squadre.items()}
    #print(self.urls)
    return self.urls
      
  def get_players(self):
    if not self.urls:
        raise Exception('URLs not initialized. Need to run get_urls first.')

    diz_finale = {}
    for squadra, url in self.urls.items():
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
    self.players = diz_finale
    return self.players

  def get_stats(self):
    diz_finale = self.players
    df = pd.DataFrame()
    for squadra in diz_finale: # O(n^2)
      print(f"Importazione dati di {squadra}")
      for player in diz_finale[squadra]:
        id = diz_finale[squadra][player]
        url = "https://www.sofascore.com/api/v1/player/" + str(id) + "/unique-tournament/23/season/52760/statistics/overall"
        response = requests.get(url)
        if response.status_code == 200:
            risp = response.json()
            stats = risp['statistics']
            stats = {'player': player, **stats}
            temp = pd.DataFrame([stats])
            df = pd.concat([df, temp], ignore_index=True)
        elif response.status_code == 404: # Need this for new players that not have statistics in sofascore, so if player not have stats we get 404 error and we easy skip this player
            pass
        else:
            raise Exception(f'Error on http call during {squadra} {player} {id} import')

    self.data = df
    return self.data
    
  def csv(self):
    if self.data is None:
        raise Exception('DataFrame not initialized. Need to run get_stats first.')
    file_name = f'fanta_dati_{self.league}.csv'
    return self.data.to_csv(file_name, index=False)
    
  def get_csv(self, campionato):
        try:
            id_squadre = self.get_teams_id(campionato)
            print("ID delle squadre ottenuti.")
            self.get_urls(id_squadre)
            print("URL dei giocatori ottenuti.")
            self.get_players()
            print("ID dei giocatori ottenuti.")
            self.get_stats()
            print("Statistiche dei giocatori ottenute.")
            file_csv = self.csv()
            print(f"File CSV generato con successo")
            return file_csv
        except Exception as e:
            print(f"Errore durante il processo: {e}")
            return None
