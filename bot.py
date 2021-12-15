from twitchio.ext import commands
from utils import Utils
import config

bot = commands.Bot(
    token=config.PASS,
    client_id=config.SECRET,
    nick=config.NICK,
    prefix='!',
    initial_channels=config.CHAN
)


class MyCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='кусь')
    async def bite(self, ctx: commands.Context):
        txt = utils.bite(ctx)
        await ctx.send(txt)

    @commands.command(name='дуэль')
    async def duel(self, ctx):
        txt = utils.duel_crossroads(ctx)
        await ctx.send(txt)

    @commands.Cog.event()
    async def event_message(self, message):
        if message.echo:
            return
        print(f'{message.author.name}: {message.content}')
        if message.author.name not in utils.users_list:
            utils.users_list.append(message.author.name)


if __name__ == "__main__":
    bot.add_cog(MyCog(bot))
    utils = Utils(config.CHAN[0])
    bot.run()
