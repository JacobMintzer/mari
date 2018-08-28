import os
import sys
import mutagen
import re

songList=os.listdir("./music")
for song in songList:
	data=mutagen.File("./music/"+song)
	artist=""
	if "TXXX:artist_en" in data.keys():
		artist=str(data["TXXX:artist_en"])
	elif "TPE1" in data.keys():
		artist=str(data["TPE1"])
	elif "TXXX:artist_jp" in data.keys():
		artist=str(data["TXXX:artist_jp"])
	with open("./playlists/"+artist+".txt","a+") as FILe:
		FILe.write(song+"\n")

