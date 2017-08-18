import discord
import os
from discord.ext import commands
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class perms:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def p(self, ctx):
		overwrite = discord.PermissionOverwrite()
		overwrite.read_messages = True
		overwrite.ban_members = False
		await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.author, overwrite)

def setup(bot):
	bot.add_cog(perms(bot))
