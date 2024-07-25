# FantaDati

<h3> What is that? </h3>

FantaDati is a scraping algorithm. Basically, you just need to instantiate the FantaDati.get_csv('championship_name') method to obtain as output a csv containing 107 features for each player of the specified championship.
For example, if I want to get the statistics of Serie A players in the 2023/2024 season I just need to write this lines of code:
fd = FantaDati() # Instantiate the obj
fd.get_csv('seriea') # Take csv file with method get_csv(league_name')
