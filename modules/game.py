import sys
from os import execl
from re import findall
from traceback import format_exc

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.tasks import loop
from discord_components import Button, ButtonStyle
from pymongo import DESCENDING

from mlpbots import DB, JWR, FOOTERNANE, FOOTERURL

CHANNELS = DB.server.game.find_one({"_id": "Каналы"})
POSTS = DB.server.game.find_one({"_id": "Посты"})
PAGES = DB.server.game.find_one({"_id": "Страницы"})


class Game(Cog):
    def __init__(self, bot):
        self.BOT = bot
        self.post.start()

    def cog_unload(self):
        self.post.cancel()

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

    async def p1(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp001.png")
            try:
                if len(set(DB.server.game.find_one({"_id": interaction.user.id})["Концовки"])) >= 17:
                    await interaction.send(embed=e, components=[[
                        Button(label="Идти за Твайлайт в библиотеку", id="p2"),
                        Button(label="Взять тележку и возвращатся на ферму", id="p6"),
                        Button(label="Навестить сестру", id="p50")]])
                else:
                    await interaction.send(embed=e, components=[[
                        Button(label="Идти за Твайлайт в библиотеку", id="p2"),
                        Button(label="Взять тележку и возвращатся на ферму", id="p6")]])
            except Exception:
                await interaction.send(embed=e, components=[[
                    Button(label="Идти за Твайлайт в библиотеку", id="p2"),
                    Button(label="Взять тележку и возвращатся на ферму", id="p6")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p1"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p2(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp002.png")
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p3")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p2"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p3(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Идти в \"Сахарный уголок\" за Пинки Пай", id="p4"),
                Button(label="Направится к домику Флаттершай", id="p11"),
                Button(label="Идти в бутик \"Карусель\" к Рэрити", id="p10"),
                Button(label="Отправится в хижину Зекоры, чтобы выяснить, что она знает", id="p20"),
                Button(label="Остаться и помочь Твайлайт с исследованиями", id="p16")], [
                Button(label="Оставить Твайлайт и направиться домой", id="p5")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p3"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p4(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p3")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p4"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p5(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p6")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p5"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p6(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Идти накрывать грядки с морковными ростками", id="p12"),
                Button(label="Зайти на кухню чего-нибудь пожевать", id="p7"),
                Button(label="Плюхнутся на диванчик и расслабится", id="p17")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p6"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p7(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="- Есть", id="p9"),
                                                         Button(label="- Нет", id="p8")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p7"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p8(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p8"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(1)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p9(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p12")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p9"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p10(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p3")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p10"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p11(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Не заходить в домик Флаттершай, и вернуться назад", id="p3"),
                Button(label="Зайти в дом и три раза сказать \"Дэннилтафт\"", id="p14")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p11"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p12(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            try:
                if len(set(DB.server.game.find_one({"_id": interaction.user.id})["Концовки"])) >= 17:
                    await interaction.send(embed=e, components=[[
                        Button(label="Бросится в погоню", id="p13"),
                        Button(label="Отправится к Твайлайт, чтобы расспросить её об этом существе", id="p15"),
                        Button(label="Уничтожить мир", id="p92")]])
                else:
                    await interaction.send(embed=e, components=[[
                        Button(label="Бросится в погоню", id="p13"),
                        Button(label="Отправится к Твайлайт, чтобы расспросить её об этом существе", id="p15")]])
            except Exception:
                await interaction.send(embed=e, components=[[
                    Button(label="Бросится в погоню", id="p13"),
                    Button(label="Отправится к Твайлайт, чтобы расспросить её об этом существе", id="p15")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p12"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p13(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p13"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(2)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p14(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Сознатся, что о нём тебе рассказала Флаттершай", id="p21"),
                Button(label="Отказатся сказать, откуда знаешь его имя", id="p19"),
                Button(label="Решить что-нибудь соврать", id="p18")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p14"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p15(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp002.png")
            await interaction.send(embed=e, components=[[
                Button(label="Идти в \"Сахарный уголок\" за Пинки Пай", id="p91"),
                Button(label="Направится к домику Флаттершай", id="p93"),
                Button(label="Идти в бутик \"Карусель\" к Рэрити", id="p89"),
                Button(label="Отправится в хижину Зекоры, чтобы выяснить, что она знает", id="p20"),
                Button(label="Остаться и помочь Твайлайт с исследованиями", id="p16")], [
                Button(label="Уйти искать Эплджек и остальных", id="p32")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p15"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p16(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Остатся с Твайлайт", id="p22"),
                                                         Button(label="Бросится в погоню за кобольдом", id="p25")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p16"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p17(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p17"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(3)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p18(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp018.png")
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p3")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p18"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p19(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Признаться, что узнала его имя от Флаттершай", id="p21"),
                Button(label="Решить что-нибудь соврать", id="p18")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p19"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p20(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Идти с Зекорой к её дому", id="p34"),
                                                         Button(label="Помчаться спасать Эплблум", id="p27")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p20"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p21(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Попросить Дэннилтафта созвать Брууни-Мот", id="p35"),
                Button(label="Попросить его отвести тебя к кобольдам", id="p53"),
                Button(label="Попросить его рассказать, где окопались кобольды", id="p24")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p21"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p22(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p23")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p22"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p23(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Оставить Твайлайт и пытаться найти пещеру кобольдов", id="p38"),
                Button(label="Остаться и защищать подругу", id="p49")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p23"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p24(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Отправиться прямо к Эй-Джей и остальным и рассказать, где прячутся кобольды", id="p32"),
                Button(label="Сперва зайти за Твайлайт,", id="p28")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p24"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p25(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Согласится на сделку", id="p26"),
                                                         Button(label="Вернуть кобольда к Твайлайт", id="p29")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p25"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p26(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Решить собрать Твайлайт и остальных", id="p28"),
                                                         Button(label="Идти к пещерам в одиночку", id="p88")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p26"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p27(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Да", id="p33"), Button(label="Нет", id="p30")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p27"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p28(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p39")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p28"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p29(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p31")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p29"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p30(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p30"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(4)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p31(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Согласиться помочь кобольду стать кентигерном", id="p57"),
                Button(label="Решить самостоятельно искать лагерь кобольдов", id="p36")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p31"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p32(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="")
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p41")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p32"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p33(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p34")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p33"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p34(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p37")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p34"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p35(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p44")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p35"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p36(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p37")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p36"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p37(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Да", id="p56"), Button(label="Нет", id="p67")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p37"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p38(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Зайти в левую пещеру", id="p54"),
                                                         Button(label="Выбрать центральную", id="p52"),
                                                         Button(label="Или правую", id="p59")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p38"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p39(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p40")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p39"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p40(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Присоидениться к плану Твайлайт", id="p42"),
                Button(label="Пока Твайлайт говорит, уйти в левую пещеру", id="p54")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p40"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p41(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Зайти в левую пещеру", id="p54"),
                                                         Button(label="Выбрать центральную", id="p87"),
                                                         Button(label="Или правую", id="p90")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p41"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p42(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p43")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p42"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p43(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p43"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(5)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p44(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Рассказать Твайлайт о Брууни-Мот", id="p45"),
                                                         Button(label="Выдумать, почему такая рассеянная", id="p46")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p44"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p45(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p47")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p45"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p46(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p47")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p46"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p47(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p48")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p47"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p48(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Обещать брауни хранить секрет", id="p69"),
                Button(label="Сказать, что не сможешь сохранить секрет", id="p55"),
                Button(label="Сознаться, что уже рассказывала Твайлайт о Брууни-Мот", id="p64"),
                Button(label="Ты уже рассказывала Твайлайт, но не признаваться в этом", id="p61")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p48"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p49(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p49"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(6)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p50(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp050.png")
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p50"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(7)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p51(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p68")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p51"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p52(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p52"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(8)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p53(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p97")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p53"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p54(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Сдаться и позволить кобольдам взять тебя в плен", id="p72"),
                Button(label="Драться", id="p65")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p54"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p55(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p63")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p55"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p56(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p71")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p56"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p57(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p58")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p57"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p58(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Проглотить оскорбление и попробовать торговаться с новым кентигерном", id="p83"),
                Button(label="Решить, что пора поставить обнаглевшего кобольда на место", id="p66")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p58"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p59(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p59"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(9)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p60(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p68")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p60"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p61(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p62")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p61"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p62(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p62"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(10)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p63(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p63"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(11)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p64(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p63")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p64"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p65(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p65"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(12)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p66(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p71")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p66"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p67(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p68")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p67"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p68(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Зайти в левую пещеру", id="p54"),
                                                         Button(label="Выбрать центральную", id="p51"),
                                                         Button(label="Или правую", id="p60")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p68"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p69(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p70")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p69"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p70(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p70"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(13)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p71(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p71"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(14)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p72(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p73")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p72"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p73(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Предложить кентигерну великие сокровища", id="p77"),
                Button(label="Предложить кентигерну морковку со своей фермы", id="p76"),
                Button(label="Вызвать кентигерна на поединок", id="p82"),
                Button(label="Вызвать кентигерна на игру в загадки", id="p84"),
                Button(label="Предложить сделать кентигерна неуязвимым", id="p74")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p73"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p74(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p75")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p74"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p75(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p71")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p75"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p76(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p76"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(15)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p77(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Да", id="p78"), Button(label="Нет", id="p80")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p77"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p78(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p79")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p78"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p79(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p86")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p79"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p80(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p81")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p80"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p81(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p81"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(16)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p82(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p82"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(17)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p83(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[Button(label="Да", id="p78"), Button(label="Нет", id="p80")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p83"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p84(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p85")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p84"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p85(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p71")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p85"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p86(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p86"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(18)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p87(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p41")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p87"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p88(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Продолжить", id="p38")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p88"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p89(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p15")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p89"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p90(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p41")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p90"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p91(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p15")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p91"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p92(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[Button(label="Начать новую игру", id="p1")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p92"}})
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$push": {"Концовки": int(19)}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p93(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Не заходить в домик Флаттершай, и вернуться назад", id="p15"),
                Button(label="Зайти в дом и три раза сказать \"Дэннилтафт\"", id="p95")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p93"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p94(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Признаться, что узнала его имя от Флаттершай", id="p21"),
                Button(label="Решить что-нибудь соврать", id="p96")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p94"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p95(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Сознатся, что о нём тебе рассказала Флаттершай", id="p21"),
                Button(label="Отказатся сказать, откуда знаешь его имя", id="p94"),
                Button(label="Решить что-нибудь соврать", id="p96")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p95"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p96(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0xFF8C00, description=PAGES[interaction.component.id])
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp018.png")
            await interaction.send(embed=e, components=[
                Button(label="Вернуться назад и сделать другой выбор", id="p15")])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p96"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    async def p97(self, interaction):
        try:
            e = Embed(title="Похищенная пони", color=0x0000FF, description=PAGES[interaction.component.id])
            await interaction.send(embed=e, components=[[
                Button(label="Предложить кентигерну великие сокровища", id="p77"),
                Button(label="Предложить кентигерну морковку со своей фермы", id="p76"),
                Button(label="Вызвать кентигерна на поединок", id="p82")]])
            DB.server.game.update_one({"_id": int(interaction.user.id)}, {"$set": {"Имя": interaction.user.name,
                                                                                   "Страница": "p97"}})
        except Exception:
            await self.errors(f"Страница {interaction.component.id}:", format_exc())

    @loop(count=1)
    async def post(self):
        try:
            try:
                game = await self.BOT.get_channel(
                    int(CHANNELS["Похищенная пони"])).fetch_message(int(POSTS["Похищенная пони"]))
                await game.delete()
            except Exception:
                pass
            e = Embed(title="Похищенная пони: интерактивная игра-новелла", color=0xFF8C00,
                      description="Привет! Если ты первый раз сталкиваешься с такой игрой, обязательно прочита"
                                  "й этот раздел. Ну а если тебе не впервой, то можешь сразу начинать игру и о"
                                  "тправляться в путешествие!\n\nТо, как будет развиваться сюжет игры, зависит"
                                  " только от тебя. В этой истории тебе предстоит посмотреть на мир глазами Кэ"
                                  "ррот Топ, молодой земной пони, живущей на окраине Понивилля. По мере чтения"
                                  " тебе придётся время от времени принимать решения.\n\nИногда мелкие, иногда"
                                  " - важные, все они, так или иначе, повлияют на сюжет. Каждый раз в момент в"
                                  "ыбора тебе будет предложено два или больше вариантов. Просто щёлкай по кноп"
                                  "ке и читай, что случилось дальше. В книге есть 19 различных концовок, некот"
                                  "орые - счастливые, некоторые - не очень, но каждая уникальна. Историю можно"
                                  " проходить несколько раз, и сюжет ни разу не повторится!\n\nТеперь, когда т"
                                  "ы знаешь, как играть, смело жми на кнопку \"Начать новую игру\" и начинай с"
                                  "вое приключение. Удачи!\n\nИгра сохраняется автоматически после каждого дей"
                                  "ствия!\n\n**Автор**: Chris **Перевод**: Многорукий Удав **Вычитка**: Orhide"
                                  "ous, Hariester, Haveglory **Оформление**: ponyPharmacist")
            e.set_image(url="https://projects.everypony.ru/purloined-pony/pics/pp000.png")
            e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            gameid = await self.BOT.get_channel(int(CHANNELS["Похищенная пони"])).send(
                embed=e, components=[[Button(label="Начать новую игру", style=ButtonStyle.green),
                                      Button(label="Продолжить игру", style=ButtonStyle.blue),
                                      Button(label="Статистика")]])
            DB.server.game.update_one({"_id": "Посты"}, {"$set": {"Похищенная пони": int(gameid.id)}})
        except Exception:
            await self.errors("Пост Игра:", format_exc())

    @Cog.listener()
    async def on_button_click(self, interaction):
        try:
            if interaction.component.label == "Начать новую игру":
                if DB.server.game.find_one({"_id": interaction.user.id}) is None:
                    DB.server.game.insert_one({"_id": int(interaction.user.id), "Имя": interaction.user.name,
                                               "Страница": "p1"})
                    await self.p1(interaction)
                else:
                    await interaction.send(
                        f"У вас обнаружена сохраненная игра! Хотите удалить ее и начать заново, или продолжить?",
                        components=[[Button(label="Продолжить игру", style=ButtonStyle.green),
                                     Button(label="Начать заново", id="p1", style=ButtonStyle.red)]])
        except Exception:
            await self.errors(f"Кнопка \"Начать новую игру\":", format_exc())
        try:
            if interaction.component.label == "Продолжить игру":
                if DB.server.game.find_one({"_id": interaction.user.id}) is not None:
                    await eval("self." + DB.server.game.find_one({"_id": interaction.user.id})["Страница"] +
                               "(interaction)")
                else:
                    await interaction.send(f"У вас нет сохраненной игры! Хотите начать новую?",
                                           components=[Button(label="Начать новую игру", style=ButtonStyle.green)])
        except Exception:
            await self.errors(f"Кнопка \"Продолжить игру\":", format_exc())
        try:
            if len(findall(r"p\d+", interaction.component.id)) != 0:
                await eval("self." + interaction.component.id + "(interaction)")
        except Exception:
            await self.errors(f"Кнопка {interaction.component.id}:", format_exc())
        try:
            if interaction.component.label == "Статистика":
                db = DB.server.game.find()
                for user in db:
                    if user["_id"] == "Каналы" or user["_id"] == "Посты":
                        continue
                    try:
                        old = set(user["Концовки"])
                        new = list(old)
                        DB.server.game.update_one({"_id": int(user["_id"])}, {"$set": {"Концовки": new}})
                    except Exception:
                        pass
                sts = []
                db = DB.server.game.find().sort("Концовки", DESCENDING)
                for user in db:
                    if user["_id"] == "Каналы" or user["_id"] == "Посты":
                        continue
                    ends = 0
                    try:
                        ends = len(set(user["Концовки"]))
                    except Exception:
                        ends = 0
                    sts.append(f"<@{user['_id']}>: Пройдено {ends} из 19 концовок.")
                e = Embed(title="Статистика прохождения:", color=interaction.user.color,
                          description="\n\n".join([x for x in sts]))
                e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
                await interaction.send(embed=e)
        except Exception:
            await self.errors(f"Кнопка {interaction.component.id}:", format_exc())


def setup(bot):
    bot.add_cog(Game(bot))
