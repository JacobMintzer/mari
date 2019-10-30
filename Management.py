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
import mutagen
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from paste_bin import PasteBinApi
import sqlite3
import json
import pandas as pd

global config

data=json.load(open('pastebin.json'))
api=PasteBinApi(dev_key=data['key'])
user_key=api.user_key(username=data['username'],password=data['password'])

async def isMod(ctx):
	if ctx.author in discord.utils.find(lambda m: m.name=="Pretty Modder Head",ctx.guild.roles).members:
		return True
	return False

def isDimi(ctx):
	return ctx.author.id==config["dimiId"]

async def botOwner(ctx):
	return ctx.author.id==config["myId"]

class Management(commands.Cog):
	def __init__(self,bot):
		global config
		config=bot.config
		self.bot=bot
		self.config=bot.config
		self.enableFilter=True
		maricord=self.bot.get_guild(175176337185701888)
		for channel in maricord.channels:
			if "filing" in channel.name:
				self.filingCH=channel


	@commands.command(hidden=True)
	@commands.check(isMod)
	async def exportEmotes(self,ctx):
		conn=sqlite3.connect('emotes.db')
		c=conn.cursor()
		c.execute("SELECT * FROM emotes ORDER BY number DESC")
		results=c.fetchall()
		result=(pd.DataFrame(results).to_string())
		link=api.paste(user_key,title='emote usage',raw_code=result,private=None,expire_date=None)
		await ctx.send(link)

	@commands.command(hidden=True)
	@commands.check(isMod)
	async def disableSpam(self,ctx):
		self.enableFilter=False

	@commands.command(hidden=True)
	@commands.check(isMod)
	async def enableSpam(self,ctx):
		self.enableFilter=True


	@commands.command(no_pm=True)
	async def restartNow(self,ctx):
		"""Restarts Mari, only use this if she isn't working right"""
		sys.exit(0)
	@commands.command()
	async def asar(self,ctx):
		await ctx.send("commands are !iam and !iamn to add and remove roles respectively. Assignable roles are: pure, squad, ponytail, suwa, he, she, they")

	@commands.command()
	async def am(self,ctx):
		await ctx.send("you forgot the i (!iam)")

	@commands.command()
	async def amn(self,ctx):
		await ctx.send("you forgot the i (!iamn)")

	@commands.command(no_pm=True)
	async def iam(self,ctx,*,role):
		"""Self assign roles (!asar for full list)"""
		if "pure" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
			await ctx.message.author.add_roles(Role)
		elif "squad" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
			await ctx.message.author.add_roles(Role)
		elif "ponytail" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Gay for Ponytail Dia")
			await ctx.message.author.add_roles(Role)
		elif "she" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="she/her")
			await ctx.message.author.add_roles(Role)
		elif "they" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="they/them")
			await ctx.message.author.add_roles(Role)
		elif "he" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="he/him")
			await ctx.message.author.add_roles(Role)
		elif "suwa"  in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Blessed by Suwa")
			await ctx.message.author.add_roles(Role)
		elif "anyc" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="ANYC Meetup")
			await ctx.message.author.add_roles(Role)
		elif "mod" in role.lower():
			await ctx.send("<:mariJoke:395760980577091585>")
		else:
			return 0
		await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))

	@commands.command(no_pm=True)
	async def iamn(self,ctx,*,role):
		"""Remove self assign roles (!asar for full list)"""
		if "pure" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
			await ctx.message.author.remove_roles(Role)
		elif "squad" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
			await ctx.message.author.remove_roles(Role)
		elif "ponytail" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Gay for Ponytail Dia")
			await ctx.message.author.remove_roles(Role)
		elif "she" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="she/her")
			await ctx.message.author.remove_roles(Role)
		elif "they" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="they/them")
			await ctx.message.author.remove_roles(Role)
		elif "he" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="he/him")
			await ctx.message.author.remove_roles(Role)
		elif "suwa"  in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Blessed by Suwa")
			await ctx.message.author.remove_roles(Role)
		else:
			return 0
		await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))


	@commands.command(hidden=True)
	@commands.check(botOwner)
	async def updateEmojis(self,ctx):
		conn=sqlite3.connect('emotes.db')
		c=conn.cursor()
		c.execute("DROP TABLE emotes")
		c.execute("""CREATE TABLE emotes(
				name text,
				number integer
				)""")
		conn.commit()
		emoteList=ctx.guild.emojis
		for emote in emoteList:
			c.execute("INSERT INTO emotes (name, number) VALUES (?,0)",(emote.name,))
			conn.commit()
		conn.close()


	def get_vc(self,ctx,channel):
		for ch in ctx.guild.voice_channels:
			if ch.id==channel:
				return ch

	async def Mute(self,spammer,guild,minutes):
		global filingCH
		global resetSafe
		resetSafe+=1
		if discord.utils.get(guild.roles,name="Muted") in spammer.roles:
			return (1)
		if minutes==-1:
			await spammer.send("looks like you are not being SHINY right now, you have been temporarily muted, and the mods have been notified. You will automatically be unmuted Please do not ask to be unmuted, and avoid spamming in the future")
			minutes=10
		Roles=spammer.roles
		Roles.pop(0)
		await spammer.edit(roles=[])
		roleList=""
		for role in Roles:
			roleList=roleList+role.name+", "
		await filingCH.send("{0} has been muted for {2} minutes, and will automatically be unmuted in 10 minutes. They had the following roles{1}".format(spammer.name,roleList,minutes))
		await spammer.add_roles(discord.utils.get(guild.roles,name="Muted"))
		await asyncio.sleep(minutes*60)
		await spammer.edit(roles=Roles)
		await spammer.remove_roles(discord.utils.get(guild.roles,name="Muted"))
		resetSafe-=1
		await filingCH.send("{0} has been unmuted. They have been given their roles back".format(spammer.name))

def setup(bot):
	bot.add_cog(Management(bot))
