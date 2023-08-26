from akinator.async_aki import Akinator
import akinator
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

aki = Akinator()
cola = 0xF43D38

class Akin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="akinator", aliases=["akin"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def akinator(self, ctx):
        await ctx.send("loading...")
        q = await aki.start_game()
        def is_correct(m):
            return m.author == ctx.message.author
        while aki.progression <= 80:
            embed = discord.Embed(title="Akinator", description="Akinator is the web genie that essentially plays '20 Questions' with you and tries to guess what character you're thinking of.", color=cola)
            embed.add_field(name=q, value='Respond by sending "yes"/"y", "no"/"n", "i don\'t know"/"i", "probably"/"p", or "probably not"/"pn"', inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            a = msg.content
            if a == "b":
                try:
                    q = await aki.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = await aki.answer(a)
        await aki.win()
        if aki.first_guess['name'] != "Nothing":
            embed = discord.Embed(title="Akinator", description=f"I'm guessing it's {aki.first_guess['name']} ({aki.first_guess['description']})! Thanks for playing!!", color=cola)
            embed.set_thumbnail(url=aki.first_guess['absolute_picture_path'])
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        else:
            embed = discord.Embed(title="Akinator", description=f"It's {aki.first_guess['name']} (I can't think of anyone with the descriptions provided)! Thanks for playing though.", color=cola)
            embed.set_thumbnail(url=aki.first_guess['absolute_picture_path'])
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        await ctx.send(embed=embed)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(akinator())
        loop.close()

def setup(bot):
    bot.add_cog(Akin(bot))