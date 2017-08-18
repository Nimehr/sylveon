import discord
from discord.ext import commands

class Mycog:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def rainbow(self, context, name):
		server = context.message.server
		author = context.message.author
		role = discord.utils.get(server.roles, name="Bot")
		violet = discord.Color(int("BE20FC", 16))
		indigo = discord.Color(int("4B0082", 16))
		blue = discord.Color(int("3785DA", 16))
		green = discord.Color(int("00FF00", 16))
		yellow = discord.Color(int("FFFF00", 16))
		orange = discord.Color(int("FF7F00", 16))
		red = discord.Color(int("FF0000", 16))
		await self.bot.say("Rainbowing")
		for role in server.roles:
			if role.name.lower() == name.lower():
				while True:
					await self.bot.edit_role(server, role, colour=violet)
					await self.bot.edit_role(server, role, colour=indigo)
					await self.bot.edit_role(server, role, colour=blue)
					await self.bot.edit_role(server, role, colour=green)
					await self.bot.edit_role(server, role, colour=yellow)
					await self.bot.edit_role(server, role, colour=orange)
					await self.bot.edit_role(server, role, colour=red)
					
def setup(bot):
	bot.add_cog(Mycog(bot))

