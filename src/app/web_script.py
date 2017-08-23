import requests, cPickle, shutil, time

all = {}
outfile = open("players.data.pickle", "w")

url = "http://fantasy.premierleague.com/drf/bootstrap-static"

r = requests.get(url)

all = r.json()

cPickle.dump(all,outfile)
