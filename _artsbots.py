import asyncio
import datetime
import os
import re
import sys
import threading
import traceback

import discord
import discord.ext
import discord_components
import pymongo
import pytz
import requests

BOT = discord.ext.commands.Bot(command_prefix=discord.ext.commands.when_mentioned_or("!"), help_command=None,
                               intents=discord.Intents.all())
DB = pymongo.MongoClient("")

JWR = 496139824500178964
IDN = 918687493577121884


def autores():
    try:
        threading.Timer(1, autores).start()
        atime = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H%M%S"))
        print(atime)
        if atime == 80000 or atime == 200000:
            os.execl(sys.executable, "python", "artssbots.py", *sys.argv[1:])
    except Exception:
        print(traceback.format_exc())


async def messages(name, value):
    try:
        await BOT.get_user(JWR).send(embed=discord.Embed(
            title="Сообщение!", color=0x008000).add_field(name=name, value=value))
    except Exception:
        print(traceback.format_exc())


async def alerts(name, value):
    try:
        await BOT.get_user(JWR).send(embed=discord.Embed(
            title="Уведомление!", color=0xFFA500).add_field(name=name, value=value))
    except Exception:
        print(traceback.format_exc())


async def errors(name, value):
    try:
        await BOT.get_user(JWR).send(embed=discord.Embed(
            title="Ошибка!", color=0xFF0000).add_field(name=name, value=value))
        os.execl(sys.executable, "python", "artssbots.py", *sys.argv[1:])
    except Exception:
        print(traceback.format_exc())


@BOT.event
async def on_connect():
    try:
        autores()
    except Exception:
        await errors("Таймер:", traceback.format_exc())


@BOT.event
async def on_ready():
    try:
        discord_components.DiscordComponents(BOT)
    except Exception:
        await errors("DiscordComponents:", traceback.format_exc())
    try:
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="новые арты..."))
    except Exception:
        await errors("Установка статуса:", traceback.format_exc())
    try:
        await messages(BOT.user, "Снова \"Смотрит новые арты...\"")
    except Exception:
        await errors("Сообщение готовности:", traceback.format_exc())
    try:
        headers1 = {"apikey": "fbd30ba0-56be-11ec-9fc5-07d4cf167e6b"}
        headers2 = {"apikey": "739ddd40-56c4-11ec-83af-4306261ca458"}
        headers3 = {"apikey": "1eaa41e0-6e48-11ec-befe-ad3a1f46b0f6"}
        params = (("url", "https://4pda.to/forum/index.php?showtopic=403239&view=getnewpost"), ("render", "true"),
                  ("location", "eu"), ("device_type", "mobile"))
        get = requests.get("https://app.zenscrape.com/api/v1/get", headers=headers1, params=params).content
        url = "//4pda.to/forum/dl/post/"
        counts = len(re.findall(rf"{url}(\d*)/(?:[_\-]*[\w]+[_\-]+){{2,}}[\w]+[(\d+)%]*\.(?:jpg|png|gif|jpeg)",
                                f"{get}"))
        art = int(DB.artssbots.new.count_documents({})) + int(DB.artssbots.old.count_documents({}))
        if counts != 0:
            news = int(re.findall(rf"{url}(\d*)/(?:[_\-]*[\w]+[_\-]+){{2,}}[\w]+[(\d+)%]*\.(?:jpg|png|gif|jpeg)",
                                  f"{get}")[-1][:-3])
            posts1 = re.findall(
                rf"{url}((?:{news - 1}\d{{3}})/(?:[_\-]*[\w]+[_\-]+){{2,}}[\w]+[(\d+)%]*\.(?:jpg|png|gif|jpeg))",
                f"{get}")
            posts2 = re.findall(
                rf"{url}((?:{news}\d{{3}})/(?:[_\-]*[\w]+[_\-]+){{2,}}[\w]+[(\d+)%]*\.(?:jpg|png|gif|jpeg))", f"{get}")
            new = len(posts1) + len(posts2)
            if int(news) > int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["id"]):
                DB.artssbots.artssbots.update_one({"_id": "IDS"}, {"$set": {"id": int(news)}})
                i = 0
                a = int(DB.artssbots.new.count_documents({})) + 1
                while i < len(posts1):
                    DB.artssbots.new.insert_one({"_id": int(a), "post": f"{str(posts1[i])}"})
                    i += 1
                    a += 1
                ii = 0
                b = int(DB.artssbots.new.count_documents({})) + 1
                while ii < len(posts2):
                    DB.artssbots.new.insert_one({"_id": int(b), "post": f"{str(posts2[ii])}"})
                    ii += 1
                    b += 1
                await messages(BOT.user, f"{new} артов загружены в БД!\nНа данный момент в базе данных {art} артов!")
            else:
                await messages(BOT.user, f"Новые арты не обнаружены!\nНа данный момент в базе данных {art} артов!")
        else:
            await messages(BOT.user, f"Новые арты не обнаружены!\nНа данный момент в базе данных {art} артов!")
    except Exception:
        await errors("Загрузка артов:", traceback.format_exc())
    try:
        iii = 1
        while True:
            if DB.artssbots.new.find_one({"_id": int(iii)}):
                await BOT.get_channel(
                    int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["channel"])).send(
                    "https://4pda.to/forum/dl/post/" + str(DB.artssbots.new.find_one({"_id": int(iii)})["post"]))
                DB.artssbots.new.delete_one({"_id": int(iii)})
                await asyncio.sleep(3600)
            if int(DB.artssbots.new.count_documents({})) == 0:
                if DB.artssbots.old.find_one({"_id": int(iii)}):
                    await BOT.get_channel(
                        int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["channel"])).send(
                        "https://4pda.to/forum/dl/post/" + str(DB.artssbots.old.find_one({"_id": int(iii)})["post"]))
                    DB.artssbots.old.delete_one({"_id": int(iii)})
                    await asyncio.sleep(3600)
            iii += 1
    except Exception:
        await errors("Отправка артов:", traceback.format_exc())


@BOT.event
async def on_message(message):
    try:
        await BOT.process_commands(message)
    except Exception:
        await errors("process_commands:", traceback.format_exc())


# команды пользователей
@BOT.command(description="0", name="help", help="Показать список всех команд бота", brief="Не применимо", usage="help")
async def helpmenu(ctx):
    try:
        if ctx.channel.id == int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["channel"]):
            await ctx.message.delete(delay=1)
            e = discord.Embed(title="Список всех команд:", color=ctx.author.color)
            e.set_footer(text=f"В качестве префикса можно использовать знак ! или упоминание бота @{BOT.user.name}")
            list1 = [[x.description for x in BOT.commands], [x.name for x in BOT.commands],
                     [x.help for x in BOT.commands], [x.brief for x in BOT.commands], [x.usage for x in BOT.commands]]
            list2 = []
            i = 0
            while i < len(list1[0]):
                sor = [list1[0][i], list1[1][i], list1[2][i], list1[3][i], list1[4][i]]
                list2.append(sor)
                i += 1
            list2.sort()
            ii = 0
            while ii < len(list2):
                if ctx.message.author.id == JWR:
                    if int(list2[ii][0]) <= 9:
                        e.add_field(name=f"{list2[ii][1]}", inline=False,
                                    value=f"Описание: {list2[ii][2]}\nПараметр: {list2[ii][3]}\nПример: {list2[ii][4]}")
                elif ctx.message.author.guild_permissions.administrator:
                    if int(list2[ii][0]) <= 8:
                        e.add_field(name=f"{list2[ii][1]}", inline=False,
                                    value=f"Описание: {list2[ii][2]}\nПараметр: {list2[ii][3]}\nПример: {list2[ii][4]}")
                elif ctx.message.author.guild_permissions.manage_messages:
                    if int(list2[ii][0]) <= 7:
                        e.add_field(name=f"{list2[ii][1]}", inline=False,
                                    value=f"Описание: {list2[ii][2]}\nПараметр: {list2[ii][3]}\nПример: {list2[ii][4]}")
                else:
                    if int(list2[ii][0]) <= 6:
                        e.add_field(name=f"{list2[ii][1]}", inline=False,
                                    value=f"Описание: {list2[ii][2]}\nПараметр: {list2[ii][3]}\nПример: {list2[ii][4]}")
                ii += 1
            await ctx.send(embed=e)
            await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="1", name="arts", help="Посчитать количество артов", brief="Не применимо", usage="arts")
async def arts(ctx):
    try:
        if ctx.channel.id == int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["channel"]):
            await ctx.message.delete(delay=1)
            art = int(DB.artssbots.new.count_documents({})) + int(DB.artssbots.old.count_documents({}))
            e2 = discord.Embed(title="Количество артов:", color=ctx.author.color,
                               description=f"На данный момент в базе данных {art} артов!")
            e2.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                          icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/"
                                   "NoDRM.png")
            await ctx.send(embed=e2)
            await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


# команды админов
@BOT.command(description="8", name="res", help="Полная перезагрузка бота", brief="Не применимо", usage="res")
@discord.ext.commands.has_permissions(administrator=True)
async def res(ctx):
    try:
        if ctx.channel.id == int(DB.artssbots.artssbots.find_one({"_id": "IDS"})["channel"]):
            await ctx.message.delete(delay=1)
            await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
            await asyncio.sleep(1)
            os.execl(sys.executable, "python", "artssbots.py", *sys.argv[1:])
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


if __name__ == "__main__":
    try:
        BOT.run("")
    except Exception:
        print(traceback.format_exc())
