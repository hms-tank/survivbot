import discord
from discord.ext import commands

class InternetStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # I will refactor this later using httpx instead because I can't
    # find a nice way to make requests async (I don't understand
    # grequests)
    @commands.command()
    async def serverstatus(self, ctx):
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

async def setup(bot):
    await bot.add_cog(InternetStuff(bot))