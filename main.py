import discord
from discord.ext import commands, tasks
import os
import requests
import signal
import random
import time
from string import digits
digits = frozenset(digits) # we don't need to change digits, and this should make things ever-so-slightly faster
bottoken = open("token.txt","r").readline()
membercount=0
totalmessages=0 # total number of messages since bot turned on
import httplist
import glob

class TimeoutException(Exception):   # Custom exception class
    print("bot timed out")

def timeout_handler(signum, frame):   # Custom signal handler (this is where OSdev IDT knowledge is relatable :p)
    raise TimeoutException

# Change the behavior of SIGALRM to call the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)



# key=os.getenv('key')
# wkey=os.getenv('wkey')

class SurvivBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self):
        for extension in glob.iglob(f'extensions{os.sep}*{os.extsep}py'):
            extension = extension.replace(os.sep, '.')[:-len(os.extsep) - 2]
            try:
                await self.load_extension(extension)
                self.logger.info(f'Loaded extension {extension}')
            except Exception as e:
                self.logger.info(f'Failed to load extension {extension}')
        

intents = discord.Intents.default()
intents.members = True

client = SurvivBot(
    command_prefix='$',
    intents=intents,
    help_command=None,
    owner_ids=[401849772157435905, 876488885419520020]
)

# https://discord.com/api/oauth2/authorize?client_id=1079242361491693658&permissions=8&scope=applications.commands%20bot



@client.event
async def on_ready():
    print("========")
    print("current UNIX time is {time}.".format(time=int(time.time())))
    print("========")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('========')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply('You can\'t do that here.')
    else:
        await ctx.reply('An unknown error occurred.')
        print(error)


@client.command()
async def shell(ctx,cmd):
    if(ctx.message.author.id in owners):
       out = os.popen(str(cmd))
       try:
           await ctx.send(str(out.read()))
       except:
          os.system(cmd)
    else:
        await ctx.send("hey, wait a minute, you're not the owner! you can't do that! >:(")
        

    
    
  
@client.command()
async def links(ctx):
    embed = discord.Embed(title="Links", description="", color=0xFF0000)
    embed.add_field(name="Test Server", value="https://test.resurviv.io")
    embed.add_field(name="Play Stable Version", value="https://resurviv.io")
    embed.add_field(name="Discord Perma Invite", value="https://discord.resurviv.io")
    embed.add_field(name="Subreddit", value="https://reddit.com/r/survivreloaded")
    embed.add_field(name="Github (Organization)", value="https://github.com/SurvivReloaded")
    embed.add_field(name="GitLab (deprecated)", value="https://gitlab.com/hasanger/survivreloaded")
    embed.add_field(name="Bot GitHub", value="https://github.com/Killaship/survivbot")
    await ctx.send(embed=embed)


# Killaship told me that this command is deprecated.
# @client.command()
# async def initleaderboard(ctx, debug="chicken_nuggets"):
#     global leaderboardfailsafe
#     if(leaderboardfailsafe != 0):
#         await ctx.send("Leaderboard failsafe value = {val}. It should equal zero. This means that the leaderboard is still in progress of initalizing. Wait until it's done!".format(val=leaderboardfailsafe))
#         return
#     leaderboardfailsafe = 1
#     if(ctx.message.author.id in owners):
#         global leaderboard
#         global xp
#         global timestamps

#         await ctx.send("Initializing leaderboard, this may take a while, especially if dumping IDs is enabled!")
#         time.sleep(0.5)
#         await ctx.send("Counting Members     {timestamp}".format(timestamp=round(time.time())))
#         global membercount
#         members = ctx.message.guild.members
#         i = 0
#         for member in members:
#             i += 1
#             if(debug == "dump"):
#                 await ctx.send("{id}    ({count}  {timestamp})".format(id=member.id, count=str(i), timestamp=round(time.time())))
#             leaderboard.append(member.id)
#             xp.append(0)
#             time.sleep(.1)
#         i = 0
#         await ctx.send("Member counting finished")
#         for member in members:
#             timestamps.append(str(round(time.time())))
#         file = open("board.txt", 'w+') 
#         file.truncate(0) # overwrite file
#         for i in range(len(leaderboard)):
#             file.write(str(leaderboard[i]) + "\n")
#         file.close()
#         await ctx.send("Leaderboard exported to board.txt")

#         file = open("xp.txt", 'w+') 
#         file.truncate(0) # overwrite file
#         for i in range(len(xp)):
#             file.write(str(xp[i]) + "\n")
#         file.close()
#         await ctx.send("XP counts exported to xp.txt")

#         file = open("time.txt", 'w+') 
#         file.truncate(0) # overwrite file
#         for i in range(len(timestamps)):
#             file.write(str(timestamps[i]) + "\n")
#         file.close()
#         await ctx.send("Timestamps set in time.txt")
#         await ctx.send("Leaderboard Initialized! ({timestamp})".format(timestamp=round(time.time())))
#         leaderboardfailsafe = 0
#     else:
#         await ctx.send("hey, wait a minute, you're not the owner! you can't do that! >:(")
#         leaderboardfailsafe = 0
#         return






    





@client.command()
async def help(ctx):
   
  

    embed = discord.Embed(title="help", description="", color=0xFF0000)#Declaring the help command is an embed.

    

    embed.add_field(name="$explain", value="Explains this server and lists FAQ.")

    embed.add_field(name="$links", value="Lists various links related to the project.")

    embed.add_field(name="$serverstatus", value="Checks whether the game server (or at least website) is up. It checks all websites on which the game is hosted. Not too reliable, might return 502 errors.")

    embed.add_field(name="$getxp", value="This command shows the amount of XP the sender has.")
    
    embed.add_field(name="$getleaderboard", value="This command lists the 5 members of the server with the most XP!. (6 including bot)")

    embed.add_field(name="$checkurl", value="Checks the connectivity of any URL.")

    embed.add_field(name="$help", value="This command.")

    embed.add_field(name="Bot GitHub", value="https://github.com/Killaship/survivbot")

    await ctx.send(embed=embed)#sends the embed.


@client.command()
async def serverstatus(ctx):
    text = []
    text.append("Checking 3 site(s)\n") # todo: make this into a for loop that reads from an array
    text.append("Note: This may or may not be accurate. Do not trust these results.\n")
    text.append("*https://taskjourney.org:449*\n")
    code = urlcheck("https://taskjourney.org:449/")
    if(code != 200):
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")
        code = urlcheck("https://survivreloaded.com/")
    text.append("*https://survivreloaded.com/*\n")
    code = urlcheck("https://survivreloaded.com/")
    if(code != 200):
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")  
    code = urlcheck("https://resurviv.io/")
    text.append("*https://resurviv.io/*\n")
    if(code != 200):
        text.append("The server sent an abnormal response. If it's 301 or 302, the server redirected the bot. If it's not those, the server might be down. The HTTP code sent was: {http}. ({phrase})\n".format(http=str(code), phrase=httplist[code]))
    else:
        text.append("The server is currently up. (It sent a response code of 200 OK)\n")
        text.append("If your game is frozen, it's most likely that the client froze or crashed. The game is still relatively unstable, you'll have to reload the game.\n")
    embed = discord.Embed(title="Surviv Reloaded Status", description=''.join(text), color=0x00FF00)
    await ctx.send(embed=embed)


@client.command()
async def checkurl(ctx,site):
    code = urlcheck(site)
    if(code != 200):
        await ctx.send("The server is currently down or unresponsive. The HTTP code sent was: {http}. ({phrase})".format(http=str(code), phrase=httplist[code]))
    else:
        await ctx.send("The server is currently up. (It sent a response code of 200 OK)")

@client.command()
async def resetbot(ctx):
    if(ctx.message.author.id in owners):
        await ctx.send("Bot is reloading, please wait a few seconds before sending commands.")
        exit()
    else:
        await ctx.send("hey, wait a minute, you're not the owner! you can't do that! >:(")        

@client.command()
async def ownersonly(ctx):
    if(ctx.message.author.id in owners):
        await ctx.send("You are the owner of this application.")
        exit()
    else:
        await ctx.send("You're not the owner of this application.")         
        
        
def urlcheck(url):
    signal.alarm(TIMEOUT)    
    try:
        r = requests.head(url, timeout=3)
        return r.status_code
    except TimeoutException:
        return 999
        signal.alarm(0)
        
#runs the bot token.
client.run(bottoken.strip())
