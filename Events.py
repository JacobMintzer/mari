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


class Events:
	def __init__(self,bot,config):
		self.bot=bot
		self.config=config
		self.maricord=self.bot.get_guild(175176337185701888)
		self.emoteList=self.maricord.emojis

	@bot.event
	async def on_guild_emojis_update(guild,before,after):
		if "Shiny" in guild.name:
			for emote in after:
				if emote not in before:
					conn=sqlite3.connect('emotes.db')
					c=conn.cursor()
					c.execute ("INSERT INTO emotes (name, number) VALUES (?,?)",(emote.name,1))
					conn.commit()
					conn.close()

	@bot.event
	async def on_reaction_add(reaction, user):
		if "Shiny" in reaction.message.guild.name:
			try:
				if reaction.emoji in self.emoteList:
					conn=sqlite3.connect('emotes.db')
					c=conn.cursor()
					c.execute("SELECT number FROM emotes WHERE name=?",(reaction.emoji.name,))
					num=c.fetchone()[0]
					c.execute("UPDATE emotes SET number="+str(num+1)+" WHERE name=?",(reaction.emoji.name,))
					conn.commit()
					conn.close()
			except Exception as e:
				print("error on checking reaction "+str(e))

	@bot.event
	async def on_member_join(member):
		if "Shiny" in member.guild.name:
			for channel in member.guild.channels:
				if "welcome" in channel.name:
					welcomech=channel
				elif "awashima" in channel.name:
					defch=channel
			welcome=open("welcome.txt","r")
			welcomeMessage=welcome.read().format(member.mention,discord.utils.get(member.guild.emojis, name="itsjoke"),welcomech.mention)
			welcome.close()
			bot.loop.create_task(delayMessage(defch,welcomeMessage))
