import asyncio
import datetime
import json
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
import websockets
import youtube_dl

BOT = discord.ext.commands.Bot(command_prefix=discord.ext.commands.when_mentioned_or("!"), help_command=None,
                               intents=discord.Intents.all())
DB = pymongo.MongoClient("")

JWR = 496139824500178964
IDVR = 935223849128165476


def autores():
    try:
        threading.Timer(1, autores).start()
        atime = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H%M%S"))
        print(atime)
        if atime == 80000 or atime == 200000:
            os.execl(sys.executable, "python", "musicsbots.py", *sys.argv[1:])
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
        os.execl(sys.executable, "python", "musicsbots.py", *sys.argv[1:])
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
        await BOT.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="броняшное радио..."))
    except Exception:
        await errors("Установка статуса:", traceback.format_exc())
    try:
        await messages(BOT.user, "Снова \"Слушает броняшное радио...\"")
    except Exception:
        await errors("Сообщение готовности:", traceback.format_exc())
    try:
        trigger = 0
        i = 1
        while i != 0:
            if int(DB.musicsbots.queue.count_documents({})) != 0:
                if DB.musicsbots.queue.find_one({"_id": int(i)}):
                    vc = None
                    m = DB.musicsbots.queue.find_one({"_id": i})
                    try:
                        for x in BOT.voice_clients:
                            await x.disconnect()
                    except Exception:
                        await errors("Плеер: Отключение от канала:", traceback.format_exc())
                    try:
                        vc = await BOT.get_channel(
                            int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["voice"])).connect()
                    except Exception:
                        await errors("Плеер: Подключение к каналу:", traceback.format_exc())
                    try:
                        vc.play(discord.FFmpegPCMAudio(f"{m['url']}"))
                    except Exception:
                        await errors("Плеер: Воспроизведение:", traceback.format_exc())
                    d = str(datetime.timedelta(seconds=m["duration"]))
                    try:
                        post = await BOT.get_channel(
                            int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"])).fetch_message(
                            int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["post"]))
                        await post.delete()
                    except Exception:
                        print(traceback.format_exc())
                    e1 = discord.Embed(title="Сейчас играет:", color=0x00FFFF)
                    e1.set_thumbnail(url=m["thumbnail"])
                    e1.add_field(
                        name=m["title"], inline=False,
                        value=f"Исполнитель: {m['channel']}\nДлительность: {d}\nСсылка: {m['webpage_url']}")
                    e1.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                                  icon_url="https://cdn.discordapp.com/attachments/915008263253266472/"
                                           "915449197388525618/NoDRM.png")
                    mes = await BOT.get_channel(
                        int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"])).send(
                        embed=e1, components=[[discord_components.Button(label="Очередь", style=3)]])
                    DB.musicsbots.musicsbots.update_one({"_id": "Вечеринка"}, {"$set": {"post": int(mes.id)}})
                    DB.musicsbots.queue.delete_one({"_id": i})
                    await asyncio.sleep(int(m["duration"]))
                a = []
                c = 1
                for b in DB.musicsbots.queue.find():
                    a.append(b["_id"])
                if len(a) != 0:
                    c = int(a[-1])
                if i > c:
                    i = 0
                i += 1
            if int(DB.musicsbots.queue.count_documents({})) == 0:
                vc2 = None
                try:
                    for x in BOT.voice_clients:
                        await x.disconnect()
                except Exception:
                    await errors("Плеер: Отключение от канала:", traceback.format_exc())
                try:
                    vc2 = await BOT.get_channel(
                        int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["voice"])).connect()
                except Exception:
                    await errors("Плеер: Подключение к каналу:", traceback.format_exc())
                try:
                    vc2.play(discord.FFmpegPCMAudio("https://everhoof.ru/320"))
                except Exception:
                    await errors("Плеер: Воспроизведение:", traceback.format_exc())
                icon, artist, title, duration, delta = "", "", "", 0, 0
                try:
                    content = await websockets.connect("wss://everhoof.ru:443/ws")
                    track = json.loads(await content.recv())
                    icon, artist, title, duration = track["art"], track["artist"], track["title"], track["duration"]
                    if len(icon) == 0:
                        icon = "//everhoof.ru/favicon.png"
                    if len(artist) == 0:
                        try:
                            artist = re.split(" - ", track["name"])[0]
                        except:
                            print(traceback.format_exc())
                        if len(artist) == 0:
                            artist = "Everhoof Radio"
                    if len(title) == 0:
                        try:
                            title = re.split(" - ", track["name"])[1]
                        except:
                            print(traceback.format_exc())
                        if len(title) == 0:
                            title = "Everhoof Radio"
                    if len(str(duration)) == 0:
                        duration = 60
                    try:
                        btime = "".join(re.findall(r"\d{2}:\d{2}:\d{2}", track["ends_at"])[0])
                        ctime = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M:%S")
                        time_1 = datetime.datetime.strptime(f'{btime}', "%H:%M:%S")
                        time_2 = datetime.datetime.strptime(f'{ctime}', "%H:%M:%S")
                        h, m, s = str(time_1 - time_2).strip().split(":")
                        delta = int(h) * 3600 + int(m) * 60 + int(s) + 1
                    except:
                        delta = 60
                    if duration == 0:
                        if track["starts_at"] == track["ends_at"]:
                            try:
                                content = json.loads(requests.get("https://everhoof.ru/api/calendar/nogard").text)[0]
                                starts_at = "".join(re.findall(r"\d+", content["starts_at"])[:6])
                                ends_at = "".join(re.findall(r"\d+", content["ends_at"])[:6])
                                dtime = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y%m%d%H%M%S")
                                if int(starts_at) <= int(dtime) <= int(ends_at):
                                    artist, title, delta = "В эфире", content["summary"], 60
                                    if trigger == 0:
                                        await BOT.get_channel(
                                            int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"])).send(
                                            BOT.get_user(JWR).mention + f" Сейчас в прямом эфире \"{title}\"!")
                                        trigger += 1
                            except Exception:
                                delta = 60
                        else:
                            delta = 60
                except Exception:
                    await errors("Плеер: Парсер радио:", traceback.format_exc())
                d = str(datetime.timedelta(seconds=duration))[2:]
                try:
                    post = await BOT.get_channel(
                        int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"])).fetch_message(
                        int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["post"]))
                    await post.delete()
                except Exception:
                    print(traceback.format_exc())
                e2 = discord.Embed(title="Сейчас играет:", color=0x00FFFF)
                e2.set_thumbnail(url=f"https:{icon}")
                e2.add_field(name=title, inline=False,
                             value=f"Исполнитель: {artist}\nДлительность: {d}\nСсылка: https://everhoof.ru")
                e2.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                              icon_url="https://cdn.discordapp.com/attachments/915008263253266472/"
                                       "915449197388525618/NoDRM.png")
                mes = await BOT.get_channel(
                    int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"])).send(
                    embed=e2, components=[[discord_components.Button(label="Очередь", style=3)]])
                DB.musicsbots.musicsbots.update_one({"_id": "Вечеринка"}, {"$set": {"post": int(mes.id)}})
                await asyncio.sleep(int(delta))
        else:
            os.execl(sys.executable, "python", "musicsbots.py", *sys.argv[1:])
    except Exception:
        await errors("Плеер:", traceback.format_exc())


@BOT.event
async def on_message(message):
    try:
        await BOT.process_commands(message)
    except Exception:
        await errors("process_commands:", traceback.format_exc())


@BOT.event
async def on_button_click(interaction):
    try:
        if interaction.component.label == "Очередь":
            e = None
            count = int(DB.musicsbots.queue.count_documents({}))
            if count != 0:
                e = discord.Embed(title="Очередь:", color=0x008000,
                                  description=f"Сейчас в очереди {count} треков!\n\n"
                                              f"Используйте команду **!play** чтобы добавить новые...\n"
                                              f"Или команду **!skip** чтобы удалить...")
                cnt = 1
                for a in DB.musicsbots.queue.find():
                    d = str(datetime.timedelta(seconds=a["duration"]))
                    if cnt <= 20:
                        e.add_field(name=f"{a['_id']}. {a['title']}", inline=False,
                                    value=f"Исполнитель: {a['channel']}\nДлительность: {d}\nСсылка: {a['webpage_url']}")
                    if cnt == 21:
                        e.add_field(name="Ошибка!", inline=False, value="Количество треков превышает допустимый лимит!")
                    cnt += 1
            else:
                e = discord.Embed(title="Очередь:", color=0x008000,
                                  description="Сейчас в очереди нет треков!\n\n"
                                              "Используйте команду **!play** чтобы добавить новые...")
            e.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                         icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/"
                                  "NoDRM.png")
            await interaction.send(embed=e,
                                   components=[[discord_components.Button(label="Очистить очередь", style=4)]])
    except Exception:
        await errors("Кнопка Очередь:", traceback.format_exc())
    try:
        if interaction.component.label == "Очистить очередь":
            await interaction.send("Вы действительно хотите полностью очистить очередь?",
                                   components=[[discord_components.Button(label="Нет", style=3),
                                                discord_components.Button(label="Да", style=4)]])
    except Exception:
        await errors("Кнопка Очистить очередь:", traceback.format_exc())
    try:
        if interaction.component.label == "Да":
            for x in DB.musicsbots.queue.find():
                DB.musicsbots.queue.delete_one(x)
            await interaction.send("Очередь успешно очищена!")
            await alerts(interaction.user, "Очистил всю очередь!")
    except Exception:
        await errors("Кнопка Да:", traceback.format_exc())
    try:
        if interaction.component.label == "Нет":
            await interaction.send("Замечательно!")
    except Exception:
        await errors("Кнопка Нет:", traceback.format_exc())


# команды пользователей
@BOT.command(description="0", name="help", help="Показать список всех команд бота", brief="Не применимо", usage="help")
async def helpmenu(ctx):
    try:
        if ctx.channel.id == int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"]):
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


@BOT.command(description="1", name="play", help="Добавить трек в очередь плеера",
             brief="Ссылка на видео или поисковый запрос", usage="play https://youtu.be/asNy7WJHqdM")
async def play(ctx, *, arg):
    try:
        if ctx.channel.id == int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"]):
            await ctx.message.delete(delay=1)
            if len(re.findall("playlist", arg)) == 0:
                ytdl = youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'False', 'default_search': 'auto'})
                yti = ytdl.extract_info(arg, download=False)
                e = discord.Embed(title="Плеер:", color=0x008000,
                                  description=f"Следующий трек успешно добавлен в очередь!\n\n"
                                              f"Используйте команду **!play** чтобы добавить новые...\n"
                                              f"Или команду **!skip** чтобы удалить...")
                if "entries" in yti:
                    for i in yti["entries"]:
                        a = []
                        c = 1
                        for b in DB.musicsbots.queue.find():
                            a.append(b["_id"])
                        if len(a) != 0:
                            c = int(a[-1]) + 1
                        post = {"_id": c, "channel": i["channel"], "title": i["title"],
                                "webpage_url": i["webpage_url"],
                                "thumbnail": i["thumbnail"], "url": i["url"], "duration": i["duration"]}
                        DB.musicsbots.queue.insert_one(post)
                        d = str(datetime.timedelta(seconds=i["duration"]))
                        e.add_field(name=f"{c}. {i['webpage_url']}", inline=False,
                                    value=f"Испольнитель: {i['channel']}\nНазвание: {i['title']}\nДлительность: {d}")
                        e.set_thumbnail(url=i["thumbnail"])
                else:
                    a = []
                    c = 1
                    for b in DB.musicsbots.queue.find():
                        a.append(b["_id"])
                    if len(a) != 0:
                        c = int(a[-1]) + 1
                    post = {"_id": c, "channel": yti["channel"], "title": yti["title"],
                            "webpage_url": yti["webpage_url"], "thumbnail": yti["thumbnail"], "url": yti["url"],
                            "duration": yti["duration"]}
                    DB.musicsbots.queue.insert_one(post)
                    d = str(datetime.timedelta(seconds=yti["duration"]))
                    e.add_field(name=f"{c}. {yti['webpage_url']}", inline=False,
                                value=f"Испольнитель: {yti['channel']}\nНазвание: {yti['title']}\nДлительность: {d}")
                    e.set_thumbnail(url=yti["thumbnail"])
                e.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                             icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/"
                                      "NoDRM.png")
                await ctx.send(embed=e)
                await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {arg}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="2", name="skip",
             help="Удалить трек из очереди плеера", brief="Номер трека в очереди", usage="skip 1")
async def skip(ctx, pos: int):
    try:
        if ctx.channel.id == int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"]):
            await ctx.message.delete(delay=1)
            inf = DB.musicsbots.queue.find_one({"_id": pos})
            if inf:
                DB.musicsbots.queue.delete_one({"_id": pos})
                d = str(datetime.timedelta(seconds=inf["duration"]))
                mes = await ctx.send(
                    embed=discord.Embed(title="Очередь:", color=0xFF0000,
                                        description=f"Следующий трек успешно удален из очереди!\n\n"
                                                    f"Используйте команду **!play** чтобы добавить новые...\n"
                                                    f"Или команду **!skip** чтобы удалить еще...").add_field(
                        name=f"{inf['_id']}. {inf['title']}", inline=False,
                        value=f"Исполнитель: {inf['channel']}\nДлительность: {d}\nСсылка: {inf['webpage_url']}"))
                await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {pos}\nКанал: {ctx.message.channel}")
                await asyncio.sleep(10)
                await mes.delete()
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


# команды админов
@BOT.command(description="8", name="res", help="Полная перезагрузка бота", brief="Не применимо", usage="res")
@discord.ext.commands.has_permissions(administrator=True)
async def res(ctx):
    try:
        if ctx.channel.id == int(DB.musicsbots.musicsbots.find_one({"_id": "Вечеринка"})["text"]):
            await ctx.message.delete(delay=1)
            await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
            await asyncio.sleep(1)
            os.execl(sys.executable, "python", "musicsbots.py", *sys.argv[1:])
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


if __name__ == "__main__":
    try:
        BOT.run("")
    except Exception:
        print(traceback.format_exc())
