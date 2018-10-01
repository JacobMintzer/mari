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


class Management:
	def __init__(self,bot,config):
		self.bot=bot
		self.config=config
		self.enableFilter=True
		maricord=self.bot.get_guild(175176337185701888)
		for channel in maricord.channels:
			if "filing" in channel.name:
				self.filingCH=channel


	@bot.command(hidden=True)
	@commands.check(isMod)
	async def exportEmotes(ctx):
		conn=sqlite3.connect('emotes.db')
		c=conn.cursor()
		c.execute("SELECT * FROM emotes ORDER BY number DESC")
		results=c.fetchall()
		result=(pd.DataFrame(results).to_string())
		link=api.paste(user_key,title='emote usage',raw_code=result,private=None,expire_date=None)
		await ctx.send(link)

	@bot.command(hidden=True)
	@commands.check(isMod)
	async def disableSpam(ctx):
		self.enableFilter=False

	@bot.command(hidden=True)
	@commands.check(isMod)
	async def enableSpam(ctx):
		self.enableFilter=True

	@bot.command(hidden=True)
	@commands.check(botOwner)
	async def restart(ctx):
		"""I will restart once I'm done with my work"""
		print ("attempting to restart")
		self.bot.loop.create_task(reset(ctx))


	@bot.command(no_pm=True)
	async def restartNow(ctx):
		"""Restarts Mari, only use this if she isn't working right"""
		sys.exit(0)

	@bot.command(no_pm=True)
	async def iam(ctx,*,role):
		"""Self assign roles (eg. !iam pure, !iam squad)"""
		if "pure" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
			await ctx.message.author.add_roles(Role)
		elif "squad" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
			await ctx.message.author.add_roles(Role)
		elif "mod" in role.lower():
			await ctx.send("<:mariJoke:395760980577091585>")

	@bot.command(no_pm=True)
	async def iamn(ctx,*,role):
		"""Remove self assign roles (eg. !iamn pure, !iamn squad)"""
		if "pure" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
			await ctx.message.author.remove_roles(Role)
		elif "squad" in role.lower():
			Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
			await ctx.message.author.remove_roles(Role)


	@bot.command(hidden=True)
	@commands.check(botOwner)
	async def updateEmojis(ctx):
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


	def get_vc(ctx,channel):
		for ch in ctx.guild.voice_channels:
			if ch.id==channel:
				return ch

	@bot.command(hidden=True)
	@commands.check(isMod)
	async def mute(ctx,member : discord.User = self.bot.user, minutes):
	"""format is !mute @user minutes to mute"""
		await Mute(ctx.guild.get_member(member.id),ctx.guild,minutes)

	async def Mute(spammer,guild,minutes):
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