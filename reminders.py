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

cola = 0xF43D38

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()

    @commands.command(name="set_timezone", aliases=["timezone", "set_tz", "tzuser", "tz", "usertz"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set_timezone(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        try:
            embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Timezone", value="Head over to [Time-Zone-Picker(Map)](https://fiona-cai.github.io/Time-Zone-Picker/) or [Time-Zone-Picker(List)](https://fiona-cai.github.io/Time-Zone-Picker/list)  to determine your timezone. Copy it and send it in this channel after.", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            first = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            try:
                tz = msg.content
                if tz not in pytz.all_timezones:
                    raise TypeError
            except Exception:
                raise TypeError
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.message.author)), description="Step 1",color=cola)
            embed.add_field(name="Timezone", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        except TypeError:
            embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Invalid Timezone", value="Head over to [Time-Zone-Picker(Map)](https://fiona-cai.github.io/Time-Zone-Picker/) or [Time-Zone-Picker(List)](https://fiona-cai.github.io/Time-Zone-Picker/list)  to determine your timezone. Copy it and try running this command again.", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        Clock.set_time_user(ctx.message.author, tz)
        embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.message.author)), description="All set!", color=cola)
        embed.add_field(name="Current Time In {}".format(tz), value="{}".format(datetime.now(pytz.timezone(tz)).strftime("%I:%M:%S %p")), inline=True)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        await ctx.send(embed=embed)

    @commands.command(name="server_set_timezone", aliases=["server_tz", "server_timezone", "servertz", "setservertz", "tzserver"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_set_timezone(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        if ctx.message.author.guild_permissions.manage_guild:
            try:
                embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.guild)), description="Step 1", color=cola)
                embed.add_field(name="Timezone", value="Head over to [Time-Zone-Picker(Map)](https://fiona-cai.github.io/Time-Zone-Picker/) or [Time-Zone-Picker(List)](https://fiona-cai.github.io/Time-Zone-Picker/list)  to determine your timezone. Copy it and send it in this channel after.", inline=True)
                embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                first = await ctx.send(embed=embed)
                msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
                try:
                    tz = msg.content
                    if tz not in pytz.all_timezones:
                        raise TypeError
                except Exception:
                    raise TypeError
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.guild)), description="Step 1", color=cola)
                embed.add_field(name="Timezone", value="Timed out, try running this command again", inline=True)
                embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                await first.edit(embed=embed)
                return
            except TypeError:
                embed = discord.Embed(title="Setting Timezone: {}".format(str(ctx.guild)), description="Step 1", color=cola)
                embed.add_field(name="Invalid Timezone", value="Head over to [Time-Zone-Picker(Map)](https://fiona-cai.github.io/Time-Zone-Picker/) or [Time-Zone-Picker(List)](https://fiona-cai.github.io/Time-Zone-Picker/list)  to determine your timezone. Copy it and try running this command again.", inline=True)
                embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                await first.edit(embed=embed)
                return
            Clock.set_time_server(ctx.guild, tz)
            print(str(ctx.guild))
            embed = discord.Embed(title="Set Timezone", description="All set!", color=cola)
            embed.add_field(name="Current Time In {}".format(tz), value="{}".format(datetime.now(pytz.timezone(tz)).strftime("%I:%M:%S %p")), inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await ctx.send(embed=embed)
        else:
            await need_perms(ctx, cola)

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        date = datetime.now().astimezone(pytz.timezone("UTC")).strftime("%d/%m/%Y %I:%M %p")
        if date == "22/08/2021 03:59 AM":
          await Bot.get_user(self.bot, int(641381968805888001)).send("HAPPY BIRTHDAYYYYYYYY")
        if date == "22/08/2021 04:00 AM":
          await Bot.get_user(self.bot, int(641381968805888001)).send("14 tho, welcome to the cool club")
        if date == "22/08/2021 01:30 AM":
          await (Bot.get_user(self.bot, 840403892735180800)).send("im testing somf sorry")
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        for k in profiles:
            try:
                reminders = profiles[k]["reminders"]
                for r in reminders:
                    if r["date"] == date:
                        print(r)
                        await Reminders.message_user_reminder(self, k, r)
            except Exception:
                pass
            print("--")
        print(date)

    async def message_user_reminder(self, user, info):
        print(user)
        user = Bot.get_user(self.bot, int(user))
        print(user)
        embed = discord.Embed(title=info["name"], description=info["details"], color=cola)
        embed.set_footer(text="Reminder requested by {0}".format(user))
        await user.send(embed=embed)
    
    @commands.command(name="user_reminder", aliases=["reminder", "new_reminder"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def user_reminder(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Name", value="Send the name of this reminder\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            first = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            name = msg.content
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Name", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Name", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Send some details you want to include for this reminder\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            second = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            details = msg.content
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await second.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await second.edit(embed=embed)
            return
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="Send the date and time you want this reminder in this format: `dd/mm/yyyy hh:mm <am/pm>`. \nFor example, `09/02/2023 12:00 am`. This means that the reminder will be posted on February 9th, 2023 at midnight\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            third = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            date = msg.content
            if Clock.new_reminder_user(ctx.message.author, name, details, date) == False:
                raise TypeError
        except TypeError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="No timezone set yet. Use command `fi tz` to set your timezone. Then, run this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Details", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), color=cola)
        embed.add_field(name="Done!", value="You will recieve the notification in our DM. Go to Your Settings > Privacy and Security and make sure that you allow direct messages from server members!".format(str(date)), inline=True)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        await ctx.send(embed=embed)

    @commands.command(name="server_reminder")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server_reminder(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Name", value="Send the name of this reminder\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            first = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            name = msg.content
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 1", color=cola)
            embed.add_field(name="Name", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Name", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Send some details you want to include for this reminder\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            second = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            details = msg.content
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await second.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 2", color=cola)
            embed.add_field(name="Details", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await second.edit(embed=embed)
            return
        try:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="Send the date and time you want this reminder in this format: `dd/mm/yyyy hh:mm <am/pm>`. \nFor example, `09/02/2023 12:00 am`. This means that the reminder will be posted on February 9th, 2023 at midnight\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            third = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            date = msg.content
            if Clock.new_reminder_server(ctx.guild, name, details, date) == False:
                raise TypeError
        except TypeError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="No timezone set yet. Use command `fi tz` to set your timezone. Then, run this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), description="Step 3", color=cola)
            embed.add_field(name="Date and Time", value="Something went wrong... try again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await third.edit(embed=embed)
            return
        embed = discord.Embed(title="New Reminder: {}".format(str(ctx.message.author)), color=cola)
        embed.add_field(name="Done!", value="The reminder will be posted in this channel when the time comes!".format(str(date)), inline=True)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author))
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Reminders(bot))