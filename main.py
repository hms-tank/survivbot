import discord
from discord.ext import commands
import os
import time
# from string import digits
# digits = frozenset(digits) # we don't need to change digits, and this should make things ever-so-slightly faster
import glob



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
                print(f'Loaded extension {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}')
        

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
    if isinstance(error, commands.NotOwner):
        await ctx.reply('Only the bot\'s owner can use this command.')
    else:
        await ctx.reply('An unknown error occurred.')
        print(error)


# I recommend checking out jishaku instead of making these debug
# commmands yourself.
@client.command()
@commands.is_owner()
async def shell(ctx,cmd):
    out = os.popen(str(cmd))
    try:
        await ctx.send(str(out.read()))
    except:
        os.system(cmd)

    
    
  


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
@commands.is_owner()
async def resetbot(ctx):
    await ctx.send(
        "Bot is reloading, please wait a few seconds before sending commands."
    )
    exit()

@client.command()
@commands.is_owner()
async def ownersonly(ctx):
    await ctx.send("You are the owner of this application.")
    exit()
        
        
if __name__ == '__main__':
    with open("token.txt") as f:
        token = f.readline().strip()
    client.run(token)