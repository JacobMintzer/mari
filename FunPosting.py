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


global config


def isDimi(ctx):
	global config
	return ctx.author.id==config["dimiId"]

def botOwner(ctx):
	global config
	return ctx.author.id==config["myId"]

def isMod(ctx):
	global config
	try:
		return ctx.author in discord.utils.find(lambda m: m.name=="Pretty Modder Head",ctx.guild.roles).members
	except:
		return False

class FunPosting:

	def __init__(self,bot):
		global config
		config=bot.config
		self.bot=bot
		self.config=bot.config

	@commands.command(hidden=True)
	@commands.check(isMod)
	async def say(self,ctx,msg):
		if ctx.author.id==self.config["dimiId"]:
			await ctx.send("that, but pretend i said it")
			return 0
		content=ctx.message.content.replace("!say ","")
		await ctx.message.delete()
		await ctx.send(content)

	@commands.command()
	async def love(self,ctx,*,msg):
		MSG=msg.strip().lower()
		f=open("love.json","r")
		loveNovel=json.loads(f.read())
		f.close()
		if MSG=="maribot":
			await ctx.send(ctx.message.guild.get_member(config["dimiId"]).avatar_url_as(format=None, static_format="png"))
		elif MSG in loveNovel.keys():
			await ctx.send(loveNovel[MSG])

	@commands.command()
	@commands.check(isMod)
	async def loveadd(self,ctx,person,content):
		f=open("love.json","r")
		loveNovel=json.loads(f.read())
		f.close()
		if person.lower() in loveNovel.keys():
			await ctx.send("I already know how {0} is loved".format(person))
		else:
			loveNovel[person.lower()]=content
			f=open("love.json","w")
			f.write(json.dumps(loveNovel))
			f.close()

	@commands.command()
	@commands.check(isMod)
	async def loveremove(self,ctx,person):
		f=open("love.json","r")
		loveNovel=json.loads(f.read())
		f.close()
		f=open("love.json","w")
		del loveNovel[person]
		f.write(json.dumps(loveNovel))
		f.close()


	@commands.command()
	async def smug(self,ctx):
		await ctx.send("<:mariJoke:395760980577091585>")

	@commands.command(hidden=True)
	async def ban(self,ctx,member : discord.User):
		global banCoolDown
		if member.id==self.config["dimiId"]:
			await ctx.send("I could never ban Dimi "+self.config["suteki"])
		else:
			if member.id==self.config["myId"]:
				await ctx.send("Sorry dad <:mariCry:397609045403369473>")
				await ctx.send("{0} is now BANNED".format(member.mention))
			elif "maribot" in member.name.lower():
				await ctx.send("{0} is now BANNED".format(ctx.message.author.mention))
			else:
				await ctx.send("{0} is now BANNED".format(member.mention))




def setup(bot):
	bot.add_cog(FunPosting(bot))
