import asyncio
import discord
import asyncio
import json
from discord.ext.commands.bot import Bot
from discord.ext import commands, tasks
import discord.embeds
from art import Clock
from datetime import datetime 
import pytz
from misc import need_perms
import random



cola = 0xF43D38
snipe_message_author = {}
snipe_message_content = {}
class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        await asyncio.sleep(60)
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]

    @commands.command(name = 'snipe')
    async def snipe(self, ctx):
        channel = ctx.channel
        try: #This piece of code is run if the bot finds anything in the dictionary
            em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
            em.set_footer(text = f"Sent by {snipe_message_author[channel.id]}")
            await ctx.send(embed = em)
        except: #This piece of code is run if the bot doesn't find anything in the dictionary
            await ctx.send(f"No recently deleted messages in #{channel.name}")


def setup(bot):
    bot.add_cog(Snipe(bot))