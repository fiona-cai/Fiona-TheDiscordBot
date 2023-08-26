import discord
from discord.ext.commands import Bot
import json
from datetime import *
import pytz
from misc import *
import time

prefix = ("fi ", "fiona ", "FI ", "Fiona ", "Fi ")
token = "NzM1NTExNjY3MTY0ODQwMDY5.XxhUng.vvaEUfarpLsL4jWFw4cbTatdDEw"
intents = discord.Intents.default()
intents.members = True
me = [511025033976741889]
client = Bot(command_prefix=prefix, intents=intents)
red = 0xF43D38
redstr = "F43D38"
cola = red

def new_user(user):
    with open('data.json', 'r') as f:
        profiles = json.load(f)
        if "{}".format(user.id) in profiles:
            pass
        else:
            profiles.update({user.id: {"name": None, "bio": "No bio yet", "posts": [], "points": 0, "streaks": [0, 2000000000], "following": [], "followers": [], "timezone": None, "reminders":[]}})
        with open('data.json', 'w') as f:
            json.dump(profiles, f)

def new_server(server):
    with open('data2.json', 'r') as f:
        servers = json.load(f)
        if "{}".format(server.id) in servers:
            pass
        else:
            servers.update({server.id: {"timezone": None, "reminders":[], "count": [None, 0, None]}})
        with open('data2.json', 'w') as f:
            json.dump(servers, f)

class Posts():
    async def new_post(url, caption, user):
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                temp = profiles["{}".format(user.id)]["posts"]
                temp.insert(0, {"url": url, "caption": caption})
                profiles["{}".format(user.id)].update({"posts": temp})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
        except Exception:
            new_user(user)
            await Posts.new_post(url, caption, user)

    def delete_post(index, user):
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                temp = profiles["{}".format(user.id)]["posts"]
                temp.pop(index)
                profiles["{}".format(user.id)].update({"posts": temp})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
        except Exception:
            new_user(user)
            Posts.delete_post(index, user)

    def new_bio(bio, user):
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                profiles["{}".format(user.id)].update({"bio": bio})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
        except Exception:
            new_user(user)
            Posts.new_bio(bio, user)

    def new_name(name, user):
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                profiles["{}".format(user.id)].update({"name": name})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
        except Exception:
            new_user(user)
            Posts.new_name(name, user)

    def generate_profile(member):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        embeds = []
        try:
            bio = profiles["{}".format(member.id)]["bio"]
            posts = profiles["{}".format(member.id)]["posts"]
            count = 0
            if len(posts) > 0:
                for post in posts:
                    page = discord.Embed(title="{}".format(str(member.name)), description=bio, color=cola)
                    page.set_image(url=post["url"])
                    page.set_thumbnail(url=member.avatar_url)
                    page.add_field(name="\n{}:".format(str(member)), value=post["caption"])
                    page.set_footer(text="Page {} of {}".format(count+1, len(posts)))
                    embeds.append(page)
                    count += 1
            else:
                page = discord.Embed(title="{}".format(str(member.name)), description=bio, color=cola)
                page.set_thumbnail(url=member.avatar_url)
                page.set_footer(text="Page 1 of 1")
                embeds.append(page)
        except Exception:
            page = discord.Embed(title="{}".format(str(member.name)), description="To create a profile, you must have at least one post", color=cola)
            page.set_thumbnail(url=member.avatar_url)
            page.set_footer(text="Page 1 of 1")
            embeds.append(page)
        print(embeds)
        return embeds

    def generate_latest(member):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        posts = profiles["{}".format(member.id)]["posts"]
        post = posts[0]
        embed = discord.Embed(title="{}".format(str(member.name)), description=profiles["{}".format(member.id)]["bio"], color=cola)
        embed.set_image(url=post["url"])
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="\n{}:".format(str(member)), value=post["caption"])
        embed.set_footer(text="Updates for {}".format(str(member)))
        return embed
    
    def new_follow(user, account):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        try:
            temp = profiles["{}".format(user.id)]["following"]
            temp2 = profiles["{}".format(account.id)]["followers"]
            if not any(d["account"] == account.id for d in temp):
                temp.append({"account": account.id, "date": str(datetime.date.today())})
                temp2.append({"account": user.id, "date": str(datetime.date.today())})
                profiles["{}".format(user.id)].update({"following": temp})
                profiles["{}".format(account.id)].update({"followers": temp2})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
                return True
            else:
                temp.remove({"account": account.id, "date": str(datetime.date.today())})
                temp2.remove({"account": user.id, "date": str(datetime.date.today())})
                profiles["{}".format(user.id)].update({"following": temp})
                profiles["{}".format(account.id)].update({"followers": temp2})
                with open('data.json', 'w') as f:
                    json.dump(profiles, f)
                return False   
        except Exception:
            new_user(user)
            new_user(account)
            Posts.new_follow(user, account)
            return True

    def generate_followings(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        try:
            temp = profiles["{}".format(user.id)]["following"]
        except Exception:
            new_user(user)
            Posts.generate_followings(user)
        return temp
    
    def generate_followers(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        try:
            temp = profiles["{}".format(user.id)]["followers"]
        except Exception:
            new_user(user)
            Posts.generate_followers(user)
        return temp

class Points:
    def get_points(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        temp = profiles["{}".format(user.id)]["points"]
        return temp

    def get_streak_in(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        streaks = profiles["{}".format(user.id)]["streaks"]
        streak = profiles["{}".format(user.id)]["streaks"][0]
        old = profiles["{}".format(user.id)]["streaks"][1]
        if len(streaks) == 0:
            streak = 0
            old = time.time()
        if (time.time() - old) < 86400:
            print(time.time() - old)
            return streak
        else:
            return 0

    def get_streak_out(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        streak = profiles["{}".format(user.id)]["streaks"][0]
        return streak

    def generate_daily(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        streak = Points.get_streak_in(user)
        new = streak + 101
        old = Points.get_points(user)
        profiles["{}".format(user.id)].update({"points": old + new})
        profiles["{}".format(user.id)].update({"streaks": [streak+1, time.time()]})
        with open('data.json', 'w') as f:
            json.dump(profiles, f)
        return new

class Clock:
    def set_time_user(user, tzone):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        try:
            profiles["{}".format(user.id)].update({"timezone": tzone})
            with open('data.json', 'w') as f:
                json.dump(profiles, f)
        except Exception:
            new_user(user)
            Clock.set_time_user(user, tzone)

    def set_time_server(server, tzone):
        with open('data2.json', 'r') as f:
            servers = json.load(f)
        try:
            servers["{}".format(server.id)].update({"timezone": tzone})
            with open('data2.json', 'w') as f:
                json.dump(servers, f)
        except Exception:
            new_server(server)
            Clock.set_time_server(server, tzone)
    
    def get_time_server(server):
        with open('data2.json', 'r') as f:
            servers = json.load(f)
        try:
            return servers["{}".format(server.id)]["timezone"]
        except Exception:
            return None
    
    def get_time_user(user):
        with open('data.json', 'r') as f:
            profiles = json.load(f)
        try:
            return profiles["{}".format(user.id)]["timezone"]
        except Exception:
            return None

    def new_reminder_user(user, name, details, date):
        tzone = Clock.get_time_user(user)
        if tzone == None:
            return False
        date = datetime.datetime.strptime(date, '%d/%m/%Y %I:%M %p')
        date = pytz.timezone(tzone).localize(date)
        date = date.astimezone(pytz.timezone("UTC"))
        date = date.strftime("%d/%m/%Y %I:%M %p")
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                temp = profiles["{}".format(user.id)]["reminders"]
                temp.append({"name": name, "details": details, "date": str(date)})
                profiles["{}".format(user.id)].update({"reminders": temp})
            with open('data.json', 'w') as f:
                json.dump(profiles, f)
        except Exception:
            new_user(user)
            Clock.new_reminder_user(user, name, details, date)

    def new_reminder_server(server, name, details, date):
        tzone = Clock.get_time_user(server)
        if tzone == None:
            return False
        date = datetime.datetime.strptime(date, '%d/%m/%Y %I:%M %p')
        date = pytz.timezone(tzone).localize(date)
        date = date.astimezone(pytz.timezone("UTC"))
        date = date.strftime("%d/%m/%Y %I:%M %p")
        try:
            with open('data.json', 'r') as f:
                profiles = json.load(f)
                temp = profiles["{}".format(server.id)]["reminders"]
                temp.append({"name": name, "details": details, "date": str(date)})
                profiles["{}".format(server.id)].update({"reminders": temp})
            with open('data.json', 'w') as f:
                json.dump(profiles, f)
        except Exception:
            new_server(server)
            Clock.new_reminder_user(server, name, details, date)

class Server:
    def counting_channel(server, channel):
        try:
            with open('data2.json', 'r') as f:
                profiles = json.load(f)
                temp = profiles["{}".format(server.id)]["count"]
                temp[0] = "{}".format(channel.id)
                profiles["{}".format(server.id)].update({"count": temp})
            with open('data2.json', 'w') as f:
                json.dump(profiles, f)
        except Exception:
            new_server(server)
            Server.counting_channel(server, channel)

    def new_number(server, tf, author):
        with open('data2.json', 'r') as f:
            profiles = json.load(f)
            temp = profiles["{}".format(server.id)]["count"]
            if tf:
                temp[1] += 1
                temp[2] = "{}".format(author.id)
            else:
                temp[1] = 0
                temp[2] = None
            profiles["{}".format(server.id)].update({"count": temp})
        with open('data2.json', 'w') as f:
            json.dump(profiles, f)