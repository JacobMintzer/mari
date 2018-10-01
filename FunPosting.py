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

class FunPosting:

	def __init__(self,bot,config):
		self.config=config
		self.bot=bot

	@commands.command(hidden=True)
	@commands.check(isMod)
	async def say(ctx,*,msg):
		if ctx.author.id==config["dimiId"]:
			await ctx.send("that, but pretend i said it")
			return 0
		content=ctx.message.content.replace("!say ","")
		await ctx.message.delete()
		await ctx.send(content)

	@commands.command()
	async def love(ctx,*,msg):
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
	async def loveadd(ctx,person,content):
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
	async def loveremove(ctx,person):
		f=open("love.json","r")
		loveNovel=json.loads(f.read())
		f.close()
		f=open("love.json","w")
		del loveNovel[person]
		f.write(json.dumps(loveNovel))
		f.close()


	@commands.command()
	async def smug(ctx):
		await ctx.send("<:mariJoke:395760980577091585>")

	@commands.command(hidden=True)
	async def ban(ctx,member : discord.User = self.bot.user):
		global banCoolDown
		if member.id==config["dimiId"]:
			await ctx.send("I could never ban Dimi "+config["suteki"])
		else:
			if member.id==config["nyId"]:
				await ctx.send("Sorry dad <:mariCry:397609045403369473>")
				await ctx.send("{0} is now BANNED".format(member.mention))
			elif "maribot" in member.name.lower():
				await ctx.send("{0} is now BANNED".format(ctx.message.author.mention))
			else:
				await ctx.send("{0} is now BANNED".format(member.mention))