import datetime
import time
import itertools
from time import strftime

# now = {
# 	"day" : strftime("%a"),
# 	"hour" : strftime("%H"),
# 	"minute" : strftime("%M"),
# 	"hourInt" : int(strftime("%H"))-2
# }

# def opAuto():
# 	mmo = ("black desert online","PUBG","World of Warcraft")
# 	fps = ["overwatch","payday 2","Counter-Strike: Global Offensive"]
# 	moba = ["League of Legends","Heroes of the Storm"]
# 	milsim = ["Arma III", "Arma 3","Squad"]
# 	strategy = ["Hearts of Iron IV"]
# 	for gamesMMO, gamesFPS, gamesMOBA, gamesMilSim, gamesStrategy in itertools.izip_longest(mmo, fps, moba, milsim, strategy):
# 		print(gamesMMO, gamesFPS, gamesMOBA, gamesMilSim, gamesStrategy)

# def emote():
# 	baseEmote = "\":regional_indicator_"
# 	abc = "abcdefghijklmnopqrstuvwxyz"
# 	for char in abc:
# 		print "\"" + char.upper() + "\"" + " : " + baseEmote + char + ":\"," 

def listDif():
	import re

	myString = "This is my tweet check it out http://tinyurl.com/blah"

	testero = re.search("(?P<url>https?://[^\s]+)", myString).group("url")

	print(testero)

listDif()
#emote()
# utc_datetime = datetime.datetime.utcnow()

# opAuto()