import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
import datetime
from random import shuffle
import sys
from paste_bin import PasteBinApi
import sqlite3
import json
import pandas as pd
girls=["You","Kanan","Riko","Chika","Dia","Ruby","Hanamaru","Yoshiko","Harem"]


event=0

def getRoles(message):
	gRoles=[]
	for g in girls:
		Role=discord.utils.get(message.guild.roles,name="Mari"+g)
		if Role==None:
			Role=discord.utils.get(message.guild.roles,name=g+"Mari")
		gRoles.append(Role)
	return gRoles

async def removeRoles(gRoles,author):
	for rol in gRoles:
		if rol!=None:
			await author.remove_roles(rol)

async def handleNormal(message,config):
	if (("PREGARIO" in message.content or "PREGIGI" in message.content) and (message.channel.name != "kimoi-memes")):
		await message.delete()
		await message.channel.send("#kimoi-memes")
	if ("joke" in message.content.lower() or "it\'s joke" in message.content.lower()) and message.channel.id!=395743189283241995:
		await message.add_reaction(discord.utils.get(message.guild.emojis, name="mariJoke"))
	if "thanks maribot" in message.content.lower():
		await message.channel.send("no problem {}".format(message.author.mention))
	if "nep" == message.content.lower():
		await message.channel.send("nep nep")
	if "nep nep nep" == message.content.lower():
		await message.channel.send("https://www.youtube.com/watch?v=EKxio8HZiNA")
	if "!ban holo"==message.content.lower():
		await message.channel.send("no")
	elif "maribot" in message.content.lower() and ("ily" in message.content.lower() or "i love you" in message.content.lower()):
		if config["myId"] == message.author.id:
			await message.channel.send( "ily too dad")
		elif config["dimiId"] != message.author.id:
			await message.channel.send("Sorry, Dimi is my one true love, but I think you're great!")
	if message.channel.id==config["eventCh"] and event==1:
		gRoles=getRoles(message)
		#if len(message.attachments)>0 or ".png" in message.content or ".jpg" in message.content or "twitter.com/" in message.content.lower():
		if "!marix" in message.content.lower():
			girl=message.content.lower().replace("!marix","").strip()
			if girl.lower()=="aqours" or girl.lower()=="everyone" or girl.lower()=="harem":
				Role=discord.utils.get(message.guild.roles,name="MariHarem")
			else:
				Role=discord.utils.get(message.guild.roles,name="Mari"+girl.title().strip())
				if Role==None:
					Role=discord.utils.get(message.guild.roles,name=girl.title().strip()+"Mari")
			if Role!=None:
				await removeRoles(gRoles,message.author)
				await message.author.add_roles(Role)
	if "goodnight" in message.content.lower() and "maribot" in message.content.lower():
		await message.channel.send("goodnight {}".format(message.author.mention))


async def handleDimi(message,config):
	if "ily" in message.content.lower() or "i love you" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(2,3))
			await message.add_reaction(discord.utils.get(message.guild.emojis, name="mariSuteki"))
			await asyncio.sleep(random.randint(3,5))
			await message.channel.send("I love you too Dimi <a:AnchanDance:111459540679024640>")
	elif "let me " in message.content.lower() or "can i " in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(5,8))
			await message.channel.send("Shouldn't this be in DMs Dimi? "+config["suteki"])
	elif "send " in message.content.lower():
		if "thigh" in message.content.lower():
			await message.channel.send("i'll send them in DMs "+config["suteki"])
			async with message.author.typing():
				await message.author.send("one seccond")
				await asyncio.sleep(random.randint(6,15))
				await message.author.send("ok, here they are https://imgur.com/a/5hk7tOU")
				await asyncio.sleep(random.randint(1,5))
				await message.author.send("sorry if they're not thicc enough for you 😳")
		if "nudes" in message.content.lower() or "noods" in message.content.lower():
			async with message.channel.typing():
				await asyncio.sleep(random.randint(4,6))
				await message.channel.send("you first "+config["gasm"])
	elif "step on" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(3,7))
			await message.channel.send("I didn't know pets could talk "+config["suteki"])
	elif "execute order 66" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(2,4))
			await message.channel.send("working on it")
			await asyncio.sleep(random.randint(60*3,60*5))
			await message.channel.send("preparations complete")
			await asyncio.sleep(random.randint(5,7))
			await message.channel.send(config["smug"])
			spamch=discord.utils.get(message.guild.text_channels,name="lets-emoji-spam")
		async with spamch.typing():
			await message.channel.send("{0}".format(spamch.mention))
			await asyncio.sleep(2)
			await spamch.send("<:McMari:398559387377205248> {0}".format(message.author.mention))
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:zuradance:440368129105985547>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:youdance:440537076317028352>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:mariDance:397596749101006868>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:yohadance:439193900461326347>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:rikodance:440537108159922186>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:kanandance:439925504137494539>")
	elif "night marib" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(5)
			await message.channel.send("sleep tite dimi")
