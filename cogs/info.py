import discord
import datetime
import re
from cogs.utils.checks import embed_perms, cmd_prefix_len
from pyshorteners import Shortener
from discord.ext import commands
from cogs.utils import checks

class info:
	"""My custom cog that does stuff!"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def avatar(self, ctx, txt: str = None):
		"""View bigger version of user's avatar. Ex: >info avi @user"""
		if txt:
			try:
				user = ctx.message.mentions[0]
			except:
				user = ctx.message.server.get_member_named(txt)
			if not user:
				user = ctx.message.server.get_member(txt)
			if not user:
				await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'Could not find user.')
				return
		else:
			user = ctx.message.author

		if user.avatar_url[54:].startswith('a_'):
			avi = 'https://images.discordapp.net/avatars/' + user.avatar_url[35:-10]
		else:
			avi = user.avatar_url
		try:
			check = message.author.permissions_in(message.channel).embed_links
		except:
			check = True
			em = discord.Embed(colour=0x708DD0)
			em.set_image(url=avi)
			await self.bot.send_message(ctx.message.channel, embed=em)
		else:
			await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + avi)
		await self.bot.delete_message(ctx.message)

	@commands.command(pass_context=True)
	async def colour(self, ctx):
		author = ctx.message.author
		roles = author.roles
		for role in roles:
			if role.name == "@everyone":
				continue
			name = role.name
			colour = role.colour
			await self.bot.say(role.name + " : " + str(role.colour))

	@commands.command(pass_context=True)
	async def channelinfo(self, ctx):
		channel = ctx.message.channel
		server = ctx.message.server
		name = channel.name
		topic = channel.topic
		if topic == "":
			topic = "No channel topic"
		position = channel.position+1
		creation = channel.created_at.strftime("%d %b %Y %H:%M")
		channelID = channel.id
		e = discord.Embed(colour=discord.Colour.blue())
		e.add_field(name="Name", value=str(name))
		e.add_field(name="Topic", value=str(topic))
		e.add_field(name="Position", value=str(position))
		e.add_field(name="Created at", value=str(creation))
		e.set_footer(text="Channel ID: " + channelID)
		e.set_thumbnail(url=server.icon_url)
		try:
			await self.bot.say(embed=e)
		except discord.HTTPException:
			await self.bot.say("I need the \"Embed Links\" permission to send embed messages")

	@commands.command(pass_context=True, name="emotes")
	async def serveremotes(self, ctx):
		server = ctx.message.server
		emotes  = server.emojis
		msg = " "
		# await self.bot.say(emotes)
		for emote in emotes:
			msg += str(emote)
		await self.bot.say(msg)

	@checks.admin_or_permissions(manage_messages=True)
	@commands.command(pass_context=True)
	async def react(self, ctx, msg, *, reactions:str):
		emotes = {
		"A" : "\U0001f1e6",
		"B": "\U0001f1e7",
		"C": "\U0001f1e8",
		"D": "\U0001f1e9",
		"E":  "\U0001f1ea",
		"F": "\U0001f1eb",
		"G": "\U0001f1ec",
		"H" : "\U0001f1ed",
		"I": "\U0001f1ee",
		"J": "\U0001f1ef",
		"K" : "\U0001f1f0",
		"L": "\U0001f1f1",
		"M" : "\U0001f1f2",
		"N" : "\U0001f1f3",
		"O" : "\U0001f1f4",
		"P" : "\U0001f1f5",
		"Q" : "\U0001f1f6",
		"R" : "\U0001f1f7",
		"S" : "\U0001f1f8",
		"T" : "\U0001f1f9",
		"U" : "\U0001f1fa",
		"V" : "\U0001f1fb",
		"W" : "\U0001f1fc",
		"X" : "\U0001f1fd",
		"Y" : "\U0001f1fe",
		"Z" : "\U0001f1ff"
		}
		channel = ctx.message.channel
		server = ctx.message.server
		messageObj = await self.bot.get_message(channel, msg)
		await self.bot.delete_message(ctx.message)
		for char in reactions:
			if char == " ":
				continue
			await self.bot.add_reaction(messageObj, emotes[char.upper()])

	async def on_message(self, message):
		server = message.server
		channel = message.channel
		if message.author.id == "195244363339530240" and server.id == "260523882983718924" and channel.id == "260523882983718924":
			await self.bot.delete_message(message)
			image = re.search("(?P<url>https?://[^\s]+)", str(message.attachments[0])).group("url")
			await self.bot.send_message(server.get_channel("331805748520681472"), message.content + "\n" + image.replace("',", ""))


def setup(bot):
	bot.add_cog(info(bot))