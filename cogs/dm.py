import discord
import discord.utils
from discord.ext import commands
from cogs.utils import checks

class dm:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@checks.admin_or_permissions(manage_messages=True)
	async def msg(self,context,user,*,msg:str):
		server = context.message.server
		author = context.message.author
		members = server.members
		for member in members:
			if str(user) in str(member):
				if member.bot:
					await self.bot.say("You can't send messages to bots you fuckwit")
				else:
					await self.bot.send_message(member, msg)
					await self.bot.say("Sent Message")
			else:
				await self.bot.say("This user isn't in the guild")
				break

	@commands.command(pass_context=True)
	@checks.admin_or_permissions(manage_messages=True)
	async def massmsg(self, context, user, *, msg:str):
		server = context.message.server
		author = context.message.author
		member = server.members
		for member in members:
			if member.bot:
				await self.bot.say()

def setup(bot):
	bot.add_cog(dm(bot))



