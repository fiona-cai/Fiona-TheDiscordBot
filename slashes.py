import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import random
from discord_slash.utils.manage_commands import create_option
from art import cola
from art import Clock
import datetime

class Slashes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="Pong!")

    @cog_ext.cog_slash(name='invite', description='Invite Fiona')
    async def invite(self, ctx: SlashContext):
        await ctx.send("Invite me by clicking here: https://discord.com/api/oauth2/authorize?client_id=736372330644897893&permissions=8&scope=bot%20applications.commands")

    @cog_ext.cog_slash(name='userinfo', description='Take a look at your online self or stalk someone else', options=[create_option(name='member', description='The user you wish to stalk', option_type=6, required=False)])
    async def userinfo(self, ctx: SlashContext, member: discord.Member = None):
        print(ctx)
        if not member:
            member = ctx.author
        embed = discord.Embed(description=str(member), color=cola, timestamp=datetime.datetime.utcnow(), title="User Information")
        embed.add_field(name="Displayed Name", value=str(member.display_name), inline=True)
        embed.add_field(name="Date Joined Discord (UTC)", value=str(member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")), inline=False)
        embed.add_field(name="Date Joined Server (UTC)", value=str(member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")), inline=False)
        embed.add_field(name="Top Role", value=str(member.top_role), inline=False)
        embed.add_field(name="Timezone", value="{}".format(Clock.get_time_user(member)), inline=False)		
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    cog_ext.cog_slash(name='fact', description='General information on this server')
    async def fact(self, ctx: SlashContext):
        lines = open("afile.txt").read().splitlines()
        myline = random.choice(lines)
        await ctx.send(myline)

    @cog_ext.cog_slash(name='serverinfo', description='General information on this server')
    async def serverinfo(self, ctx: SlashContext):
        server = ctx.guild
        embed = discord.Embed(description="%s " % (str(server)), title="Server Information", color=cola)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Owner", value=str(server.owner), inline=True)
        embed.add_field(name="Member Count", value="{} members".format (server.member_count), inline=True)
        embed.add_field(name="Categories", value="{} categories".format (len(server.categories)), inline=True)		
        try:
          embed.add_field(name="Timezone", value="{}".format(Clock.get_time_server(server)), inline=True)
        except Exception:
          pass	
        embed.add_field(name="Default Role", value=str(server.default_role), inline=True)
        embed.add_field(name="Date Created", value=(str(server.created_at).split(" ")[0]), inline=True)
        embed.add_field(name="Roles (%s)" % str(len([x.name for x in server.roles])), value=', '.join([str(x) for x in server.roles]), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slashes(bot))
