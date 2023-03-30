import discord
from discord.ext import commands
import aiofiles
import asyncio
import random
import time

class xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard = dict()
        self.leaderboard_load_event = asyncio.Event()
        self.syncboards_lock = asyncio.Lock()
    
    async def cog_check(self, ctx):
        if not self.leaderboard_load_event.is_set():
            await ctx.reply('Please wait for the leaderboard to load.')
        await self.leaderboard_load_event.wait()
        return True
    
    async def cog_load(self):
        print('Loading XP data')
        async with aiofiles.open('board.txt') as f:
            content = await file.read()
            leaderboard = [int(i.strip()) for i in content.splitlines()]
        async with aiofiles.open('xp.txt') as f:
            content = await file.read()
            xp = [int(i.strip()) for i in content.splitlines()]
        async with aiofiles.open('time.txt') as f:
            content = await file.read()
            timestamps = [int(i.strip()) for i in content.splitlines()]
        assert len(leaderboard) == len(xp) == len(timestamps)
        for i in range(len(leaderboard)):
            self.leaderboard[leaderboard[i]] = {xp: xp[i], time: timestamps[i]}
        self.leaderboard_load_event.set()
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Time is starts set to 0 instead of the time they joined like
        # previously, because they haven't actually sent any messages
        # and shouldn't need to wait 30 seconds before getting xp.
        self.leaderboard[member.id] = {'xp': 0, 'time': 0}
        await self.syncboards()

    @commands.command()
    @commands.is_owner()
    async def awardxp(self, ctx, user, amount: int):
        self.leaderboard[user.id]['xp'] += amount
        await self.syncboards()
        await ctx.send(f"<@!{user.id}> has been awarded {amount} XP!")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.id not in self.leaderboard:
                # Instead of not giving them xp if they're somehow not
                # on the leaderboard, we add them to the leaderboard and
                # give them the xp. The log that they weren't on the
                # leaderboard shouldn't be necessary anymore, but I'll
                # keep it here as a sort of debug log, just in case
                # something happens.
                self.leaderboard[message.author.id] = {'xp': 0, 'time': 0}
                print(f"User ID {message.author.id} was not on leaderboard.")
            leaderboard_user = self.leaderboard[message.author.id]
            if (round(time.time()) - leaderboard_user['time'] >= 30):
                leaderboard_user['xp'] += random.randrange(5, 10)
                #print("old timestamp: {time}".format(time=round(time.time())))
                leaderboard_user['time'] = round(time.time())
                    #print("new timestamp: {time}".format(time=round(time.time())))
                    #print("User ID {userid} gained {xpamount}".format(userid=id,xpamount=incXP))
            await self.syncboards()
        except:
            print(f"Failed to award xp for user {message.author.id}")
    
    @commands.command()
    async def getxp(self, ctx, user: discord.User = None): 
        user = user or ctx.author
        if user.id in self.leaderboard:
            await ctx.send(
                f"<@{user.id}> has {self.leaderboard[user.id]['xp']} XP!"
            ) 
        else:
            await ctx.send(
                f"Error! <@{user.id}> is not on the leaderboard. :/"
            )

    @commands.command()
    async def getleaderboard(self, ctx):
        embed = discord.Embed(
            title='\n'.join([
                (
                    f'#{i+1}: {await client.fetch_user(user_id)} has '
                    f'{self.leaderboard[user_id]["xp"]} points!'
                ) for i, user_id in (enumerate(sorted(
                    self.leaderboard.keys(),
                    key=lambda x: self.leaderboard[x]['xp'],
                    reverse=True
                ))[:6])
            ]),
            description='Top 6 XP counts!',
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    
    async def syncboards(self):
        await self.leaderboard_load_event.wait()
        # The lock is to try to prevent concurrent file writing,
        # although it probably shouldn't matter. All the syncboards
        # requests will stack up and once one is done, the next one will
        # start writing. Using a database will drastically reduce
        # complexity. I suggest using the motor library for MongoDB.
        if self.syncboards_lock.locked():
            # I assume that the file writing is less than the speed of
            # people sending new messages, so instead of having an ever
            # increasing number of syncboards writes, we will discard
            # the call to syncboards. We actually probably shouldn't be
            # calling syncboards this often, as it's not necessary to
            # constantly keep the files updated. This could actually
            # slow down the computer this is running on. I think it
            # might be better to put this into a task that runs every
            # once in a while to "back up" the leaderboard and also run
            # this on bot stop instead of whenever we make a change to
            # the leaderboard. The current solution will prevent some
            # calls to syncboards from actually writing to the files,
            # but this should not matter too much as there are
            # frequently calls to syncboards. If this is a concern, it
            # is possible to make a task that runs this every once in a
            # while. We will also probably make it run on cog unload to
            # make sure the leaderboard is saved when the bot stops.
            # Again, we can alleviate the concerns for concurrent file
            # writing by using a database instead.
            return
        await self.syncboards_lock.acquire()
        async with aiofiles.open("board.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x) for x in self.leaderboard.keys()]
                )
            )
            await f.write('\n')
        async with aiofiles.open("xp.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x['xp']) for x in self.leaderboard.values()]
                )
            )
            await f.write('\n')
        async with aiofiles.open("time.txt", 'w') as f:
            await f.write(
                '\n'.join(
                    [str(x['time']) for x in self.leaderboard.values()]
                )
            )
            await f.write('\n')
        self.syncboards_lock.release()

async def setup(bot):
    await bot.add_cog(xp(bot))