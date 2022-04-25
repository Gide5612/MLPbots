import sys
from asyncio import sleep
from os import execl
from traceback import format_exc

from discord import Embed, utils
from discord.ext.commands import Cog, command
from discord.ext.tasks import loop

from mlpbots import JWR, DB, FOOTERNANE, FOOTERURL

ROLES = DB.server.rainbow.find_one({"_id": "Роли"})["Радуга"]


class Rainbow(Cog):
    def __init__(self, bot):
        self.BOT = bot
        self.members = []
        for mem in DB.server.rainbow.find_one({"_id": "Пользователи"}):
            if str(mem) == "_id":
                continue
            member = self.BOT.get_guild(798851582800035841).get_member(int(mem))
            self.members.append(member)
        self.rainbow.start()

    def cog_unload(self):
        self.rainbow.cancel()

    async def messages(self, name, value):
        try:
            await self.BOT.get_user(JWR).send(embed=Embed(
                title="Сообщение!", color=0x008000).add_field(name=name, value=value))
        except Exception:
            print(format_exc())

    async def alerts(self, name, value):
        try:
            await self.BOT.get_user(JWR).send(embed=Embed(
                title="Уведомление!", color=0xFFA500).add_field(name=name, value=value))
        except Exception:
            print(format_exc())

    async def errors(self, name, value, reset=0):
        try:
            await self.BOT.get_user(JWR).send(embed=Embed(
                title="Ошибка!", color=0xFF0000).add_field(name=name, value=value))
            if reset == 1:
                execl(sys.executable, "python", "mlpbots.py", *sys.argv[1:])
        except Exception:
            print(format_exc())

    @loop()
    async def rainbow(self):
        try:
            a, b = 1, 0
            while True:
                for member in self.members:
                    await member.add_roles(utils.get(self.BOT.get_guild(798851582800035841).roles, id=ROLES[a]))
                    await member.remove_roles(utils.get(self.BOT.get_guild(798851582800035841).roles, id=ROLES[b]))
                a += 1
                b += 1
                if a == 6:
                    a = 0
                if b == 6:
                    b = 0
                await sleep(3)
        except Exception:
            await self.errors("Радуга:", format_exc())

    @command(description="1", name="rainbow", help="Сделать себе радужный ник", brief="Включить/Отключить: on/off",
             usage="rainbow on")
    async def rainbowcommand(self, ctx, trigger: str = "on"):
        try:
            if trigger == "on" or trigger == "off":
                e = None
                if trigger == "on":
                    DB.server.rainbow.update_one(
                        {"_id": "Пользователи"}, {"$set": {str(ctx.author.id): str(ctx.author.name)}})
                    e = Embed(title="Радужная роль:", color=ctx.author.color,
                              description="Вы включили себе радужный ник!")
                if trigger == "off":
                    DB.server.rainbow.update_one(
                        {"_id": "Пользователи"}, {"$unset": {str(ctx.author.id): 1}})
                    e = Embed(title="Радужная роль:", color=ctx.author.color,
                              description="Вы отключили себе радужный ник!")
                e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
                await ctx.send(embed=e, delete_after=60)
                await ctx.send("!cogs cjlkzrwuqxcnaznzsx")
        except Exception:
            await self.errors(f"Команда {ctx.command.name}:", format_exc())


def setup(bot):
    bot.add_cog(Rainbow(bot))
