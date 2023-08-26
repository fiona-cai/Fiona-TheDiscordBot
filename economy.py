import discord
from discord.ext import commands
from art import Points
from misc import display_time

cola = 0xF43D38


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lb", "leaders"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        board = []
        for user in ctx.guild.members:
            if len(board) < 11:
                try:
                    board.append((str(user), Points.get_points(user)))
                except Exception:
                    pass
        board.sort(key = lambda x: x[1], reverse=True)
        embed = discord.Embed(title="Leaderboard", color=cola)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        print(board)
        for user in board:
            embed.add_field(name="{}".format(user[0]), value="{} points".format(user[1]), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        embed = discord.Embed(title="Daily Points", description="{} points were added to your account!".format(Points.generate_daily(ctx.author)), color=cola)
        embed.set_footer(text="Streak: {}".format(Points.get_streak_out(ctx.author)))
        try:
            await ctx.send(embed=embed)
        except Exception:
            print("UH")
            

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="C H I L L", color=cola)
            if error.retry_after == '0' or error.retry_after == '1':
                embed.add_field(name="Command is on cooldown, you should cooldown too :)", value="Try again in ... less than a second :)", inline=True)
            else:
                embed.add_field(name="Command is on cooldown, you should cooldown too :)", value="Try again in {}".format(display_time(int(error.retry_after), 3)), inline=True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
