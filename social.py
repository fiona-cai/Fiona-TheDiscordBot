import discord
import asyncio
import json
from discord.ext import commands
from art import Posts
from misc import is_url_image
from misc import CustomEmbedPaginator

cola = 0xF43D38

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def post_everywhere(self, user):
        print("post everywhere")
        with open('data.json', 'r') as f:
            profiles = json.load(f)
            print(profiles)
            for follower in profiles["{}".format(user.id)]["followers"]:
                account = follower["account"]
                print(account)
                await self.bot.get_user(account).send(embed=Posts.generate_latest(user))

    @commands.command(name="post", aliases=["new"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def post(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        try:
            embed = discord.Embed(title="New Post", description="Step 1", color=cola)
            embed.add_field(name="Image", value="Send the image you want to post\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            first = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            try:
                url = msg.attachments[0].url
            except Exception:
                raise TypeError
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Post", description="Step 1", color=cola)
            embed.add_field(name="Image", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        except TypeError:
            embed = discord.Embed(title="New Post", description="Step 1", color=cola)
            embed.add_field(name="Image", value="Attach an IMAGE", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        try:
            embed = discord.Embed(title="New Post", description="Step 2", color=cola)
            embed.add_field(name="Caption", value="Send some text to go along with your post\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            second = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            caption = msg.content
            print("{}".format(ctx.message.author.id))
            await Posts.new_post(url, caption, ctx.message.author)
            await Social.post_everywhere(self, ctx.message.author)
            await Social.gallery(self, ctx, ctx.message.author, 1)
            return
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Post", description="Step 2", color=cola)
            embed.add_field(name="Caption", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await second.edit(embed=embed)
            return

    @commands.command(name="gallery", aliases=["user", "profile"])
    async def gallery(self, ctx, member: discord.Member=None, *num):
        print("oops")
        if num == ():
            num = (1,)
        paginator = CustomEmbedPaginator(ctx, int(num[0])-1)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        if not member:
            member = ctx.message.author
        if member == ctx.message.author:
            paginator.add_reaction('🗑️', "delete")
        await paginator.run(Posts.generate_profile(member), int(num[0])-1)
        
    @commands.command(name="follow", aliases=["updates"])
    async def follow(self, ctx, member: discord.Member=None, *args):
        x = True
        if not member:
            x = False
        print(args)
        if x == True and ctx.message.author != member:
            if args != ('server',):
                if Posts.new_follow(ctx.message.author, member) == True:
                    embed = discord.Embed(title="Thanks for following {}".format(str(member)), color=cola)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name="You will recieve updates in this DM every time they post", value="Consider giving them some coins every once in a while!")
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    await ctx.message.author.send(embed=embed)
                    await ctx.send("Check your DMs!")
                else:
                    embed = discord.Embed(title="Unfollowed {}".format(str(member)), color=cola)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name="You will not recieve updates in this DM every time they post anymore", value="Consider giving them some coins every once in a while!")
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    await ctx.message.author.send(embed=embed)
                    await ctx.send("Check your DMs!")
            else:
                def is_correct(m):
                    return m.author == ctx.message.author
                try:
                    embed = discord.Embed(title="New Post", description="Step 1", color=cola)
                    embed.add_field(name="Image", value="Send the image you want to post\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    first = await ctx.send(embed=embed)
                    msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
                    try:
                        if is_url_image(msg.attachments[0]) == True:
                            url = msg.attachments[0].url
                    except Exception:
                        raise TypeError
                except asyncio.TimeoutError:
                    embed = discord.Embed(title="New Post", description="Step 1", color=cola)
                    embed.add_field(name="Image", value="Timed out, try running this command again", inline=True)
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    await first.edit(embed=embed)
                    return
                except TypeError:
                    embed = discord.Embed(title="New Post", description="Step 1", color=cola)
                    embed.add_field(name="Image", value="Attach an IMAGE", inline=True)
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    await first.edit(embed=embed)
                    return
                try:
                    embed = discord.Embed(title="New Post", description="Step 2", color=cola)
                    embed.add_field(name="Caption", value="Send some text to go along with your post\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    second = await ctx.send(embed=embed)
                    msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
                    caption = msg.content
                    print("{}".format(ctx.message.author.id))
                    await Posts.new_post(url, caption, ctx.message.author)
                    await Social.gallery(self, ctx, ctx.message.author, 1)
                    await Social.post_everywhere(self, ctx.message.author)
                    return
                except asyncio.TimeoutError:
                    embed = discord.Embed(title="New Post", description="Step 2", color=cola)
                    embed.add_field(name="Caption", value="Timed out, try running this command again", inline=True)
                    embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                    await second.edit(embed=embed)
                embed = discord.Embed(title="Server is now following {}".format(str(member)), color=cola)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="You will recieve updates in this channel every time they post", value="Consider giving them some coins every once in a while!")
                embed.set_footer(text="Requested by {0}".format(ctx.message.author))
                await ctx.send(embed=embed)
        else:
            await ctx.send("Who are you gonna follow? The command is `fi follow <user>`. You cannot follow yourself")

    @commands.command(name="following", aliases=["myfollows"])
    async def following(self, ctx, *args):
        print(args)
        if args != ('server',):
            embed = discord.Embed(title="Following", description = "{}".format(ctx.message.author), color=cola)
            for follow in Posts.generate_followings(ctx.message.author):
                embed.add_field(name="{}".format(self.bot.get_user(follow["account"])), value="Since {}".format(follow["date"]))
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await ctx.send(embed=embed)
        else:
            await ctx.send("mmhm")

    @commands.command(name="followers", aliases=["myfollowers"])
    async def followers(self, ctx, *args):
        print(args)
        if args != ('server',):
            embed = discord.Embed(title="Followers", description = "{}".format(ctx.message.author), color=cola)
            for follow in Posts.generate_followers(ctx.message.author):
                embed.add_field(name="{}".format(self.bot.get_user(follow["account"])), value="Since {}".format(follow["date"]))
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await ctx.send(embed=embed)
        else:
            await ctx.send("mmhm")

    @commands.command(name="bio", aliases=["newbio"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def bio(self, ctx):
        def is_correct(m):
            return m.author == ctx.message.author
        try:
            embed = discord.Embed(title="New Bio", description="Step 1 (the one and only step!)", color=cola)
            embed.add_field(name="Text", value="Send the bio you want featured on your profile/gallery\nCommand will be cancelled after 10 minutes if nothing is sent", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            first = await ctx.send(embed=embed)
            msg = await self.bot.wait_for("message", check=is_correct, timeout=600)
            bio = msg.content
        except asyncio.TimeoutError:
            embed = discord.Embed(title="New Bio", description="Step 1 (the one and only step!)", color=cola)
            embed.add_field(name="Text", value="Timed out, try running this command again", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        except Exception:
            embed = discord.Embed(title="New Bio", description="Step 1 (the one and only step!)", color=cola)
            embed.add_field(name="Text", value="Something went wrong...", inline=True)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author))
            await first.edit(embed=embed)
            return
        Posts.new_bio(bio, ctx.message.author)
        await Social.gallery(self, ctx, ctx.message.author, 1)

def setup(bot):
    bot.add_cog(Social(bot))