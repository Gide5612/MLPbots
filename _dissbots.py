import asyncio
import datetime
import os
import sys
import threading
import time
import traceback

import discord
import discord.ext
import discord_components
import pymongo
import pytz

BOT = discord.ext.commands.Bot(command_prefix=discord.ext.commands.when_mentioned_or("!"), help_command=None,
                               intents=discord.Intents.all())

DB = pymongo.MongoClient("+://:@.../?=&w=")

JWR, SER = 496139824500178964, 798851582800035841

GREEN, RED, BLUE, GRAY, LINK = 3, 4, 1, 2, 5


def autores():
    try:
        threading.Timer(1, autores).start()
        atime = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%M%S"))
        print(atime)
        if atime == 0:
            os.execl(sys.executable, "python", "dissbots.py", *sys.argv[1:])
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


async def errors(name, value, reset=0):
    try:
        await BOT.get_user(JWR).send(embed=discord.Embed(
            title="Ошибка!", color=0xFF0000).add_field(name=name, value=value))
        if reset == 1:
            os.execl(sys.executable, "python", "dissbots.py", *sys.argv[1:])
    except Exception:
        print(traceback.format_exc())


async def rainbow():
    try:
        member = BOT.get_guild(SER).get_member(JWR)
        r = [938939067226288199, 907397135266377758, 933037149551468625, 938939201121058836, 938939323221422110,
             938939374291263538]
        a, b = 1, 0
        trigger = 0
        while trigger == 0:
            await member.add_roles(discord.utils.get(BOT.get_guild(SER).roles, id=r[a]))
            await member.remove_roles(discord.utils.get(BOT.get_guild(SER).roles, id=r[b]))
            time.sleep(3)
            a += 1
            b += 1
            if a == 6:
                a = 0
            if b == 6:
                b = 0
        else:
            os.execl(sys.executable, "python", "dissbots.py", *sys.argv[1:])
    except Exception:
        await errors("Радуга:", traceback.format_exc())


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
        await BOT.change_presence(status=discord.Status.invisible)
    except Exception:
        await errors("Установка статуса:", traceback.format_exc())
    try:
        vc2 = await BOT.get_channel(945968315162058783).connect()
        vc2.play(discord.FFmpegPCMAudio("https://everhoof.ru/320"))
    except Exception:
        await errors("Радио:", traceback.format_exc())
    try:
        await rainbow()
    except Exception:
        await errors("Запуск Радуги:", traceback.format_exc())


@BOT.event
async def on_message(message):
    try:
        await BOT.process_commands(message)
    except Exception:
        await errors("process_commands:", traceback.format_exc())


@BOT.command(description="9", name="spam", help="", brief="Не применимо", usage="spam")
@discord.ext.commands.is_owner()
async def spam(ctx, member: discord.Member = None, *, mes):
    try:
        await ctx.message.delete(delay=1)
        await alerts(
            ctx.author, f"Использовал команду: {ctx.command.name} {member} {mes}\nКанал: {ctx.message.channel}")
        while True:
            await ctx.send(f"{member.mention} {mes}")
            time.sleep(3)
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="9", name="res", help="Полная перезагрузка бота", brief="Не применимо", usage="res")
@discord.ext.commands.is_owner()
async def res(ctx):
    try:
        await ctx.message.delete(delay=1)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
        await asyncio.sleep(1)
        os.execl(sys.executable, "python", "dissbots.py", *sys.argv[1:])
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


if __name__ == "__main__":
    try:
        BOT.run("..")
    except Exception:
        print(traceback.format_exc())
