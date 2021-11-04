from twitchio.ext import commands
import config
import utils

bot = commands.Bot(
    token=config.PASS,
    client_id=config.SECRET,
    nick=config.NICK,
    prefix='!',
    initial_channels=config.CHAN
)

in_duel = False
duel_login = ''


@bot.command(name='дуэль')
async def duel1(ctx):
    global in_duel, duel_login
    login = utils.get_login(ctx)
    if duel_login == login:
        await ctx.send(f"@{login} вызов уже брошен! Ожидайте оппонента!")
    elif in_duel:
        txt, log = utils.get_random_duel([login, duel_login])
        in_duel = False
        duel_login = ''
        print(log)
        await ctx.send(txt)
    else:
        duel_login = login
        in_duel = True
        await ctx.send(f"@{login} объявил дуэль на орехомётах. Напиши !дуэль чтобы принять его вызов")


@bot.command(name='кусь')
async def bite(ctx):
    txt, log = utils.random_bite(ctx)
    print(log)
    await ctx.send(txt)


if __name__ == "__main__":
    bot.run()
