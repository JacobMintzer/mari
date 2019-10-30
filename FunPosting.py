import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
import datetime
import pytz
from random import shuffle
import sys
from paste_bin import PasteBinApi
import sqlite3
import json
import pandas as pd
from saucenao import SauceNao
import requests

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

class FunPosting(commands.Cog):

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


	@commands.command()
	async def sauce(self, ctx, url:str=""):
		try:
			if (len(ctx.message.attachments)>0):
				url=ctx.message.attachments[0].url
			request=requests.get(url,allow_redirects=True)
			file="image."+url.split('.')[-1]
			open(file,'wb').write(request.content)
		except Exception as e:
			print (e)
			await ctx.send("error downloading file")
			return
		output=SauceNao(directory='./', api_key=config["sauce"])
		result=output.check_file(file_name=file)
		if (len(result)<1):
			await ctx.send("no source found")
			return
		if "Pixiv ID" in result[0]["data"]["content"][0]:
			await ctx.send("I believe the source is:\nhttps://www.pixiv.net/en/artworks/"+result[0]["data"]["content"][0].split("Pixiv ID: ")[1].split("\n")[0])
		elif "Source: Pixiv" in result[0]["data"]["content"][0]:
			stuff=result[0]["data"]["content"][0].split("\n")[0]
			id=stuff.split("Source: Pixiv #")[1]
			await ctx.send("I believe the source is:\nhttps://www.pixiv.net/en/artworks/"+id)
		elif "dA ID" in result[0]["data"]["content"][0]:
			await ctx.send("I believe the source is:\nhttps://deviantart.com/view/"+result[0]["data"]["content"][0].split("dA ID: ")[1].split("\n")[0])
		elif len(result[0]["data"]["ext_urls"])>0:
			await ctx.send("I couldn't find the exact link, but this might help you find it:\n"+"\n".join(result[0]["data"]["ext_urls"]))
		os.remove(file)

	@commands.command()
	async def genLog(member, what):
		embd=discord.Embed()
		embd.title=member.display_name
		embd.description=what
		embd=embd.set_thumbnail (url=member.avatar_url)
		embd.type="rich"
		embd.timestamp=datetime.datetime.now(pytz.timezone('US/Eastern'))
		embd=embd.add_field(name = 'Discord Username', value = str(member))
		embd=embd.add_field(name = 'id', value = member.id)
		embd=embd.add_field(name = 'Joined', value = member.joined_at)
		embd=embd.add_field(name = 'Roles', value = ', '.join(map(lambda x: x.name, member.roles)))
		embd=embd.add_field(name = 'AccountCreated', value = member.created_at)
		return mbd

	@commands.command()
	async def info(self, ctx, member: discord.Member=None):
		"""!info for information on yourself, or !info name for info on another person"""
		if member == None:
			await ctx.send(embed=self.genLog(ctx.message.author, "Info on {0}".format(ctx.message.author.display_name)))
		else:
			await ctx.send(embed=self.genLog(member, "info on {0}".format(member.display_name)))

	@commands.command()
	async def sinfo(self, ctx):
		"""!sinfo if you want me to tell you information about this server"""
		embd=discord.Embed()
		embd.title=ctx.guild.name
		embd.description="information on "+ctx.guild.name
		embd=embd.set_thumbnail (url=ctx.guild.icon_url)
		embd.type="rich"
		embd.timestamp=datetime.datetime.now(pytz.timezone('US/Eastern'))
		dt = ctx.guild.created_at
		embd=embd.add_field(name = 'Date Created', value = str(dt.date())+" at "+str(dt.time().isoformat('minutes')))
		embd=embd.add_field(name = 'ID', value = ctx.guild.id)
		embd=embd.add_field(name = 'Owner', value = str(ctx.guild.owner))
		embd=embd.add_field(name = 'Total Boosters', value = ctx.guild.premium_subscription_count)
		embd=embd.add_field(name = 'Total Channels', value = len(ctx.guild.channels))
		embd=embd.add_field(name = 'Total Members', value = ctx.guild.member_count)
		await ctx.send(embed=embd)

def setup(bot):
	bot.add_cog(FunPosting(bot))
