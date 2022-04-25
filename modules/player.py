import sys
from asyncio import sleep
from datetime import datetime, timedelta
from json import loads
from os import execl
from re import findall, split
from traceback import format_exc

from bs4 import BeautifulSoup
from discord import Embed, FFmpegPCMAudio
from discord.ext.commands import Cog
from discord.ext.tasks import loop
from discord_components import Button, ButtonStyle
from pytz import timezone
from requests import get
from websockets import connect

from mlpbots import DB, JWR, FOOTERNANE, FOOTERURL

CHANNELS = DB.server.player.find_one({"_id": "Каналы"})


class Player(Cog):
    def __init__(self, bot):
        self.BOT = bot
        self.player.start()

    def cog_unload(self):
        self.player.cancel()

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

    async def subscribe(self, interaction):
        try:
            status = ""
            try:
                user = DB.server.player.find_one({"_id": "Уведомления"})[f"{interaction.user.id}"]
                status = "Подписан"
            except Exception:
                status = "Не подписан"
            e = Embed(title="Настройки:", color=0x00FFFF,
                      description="Подписатся на уведомления о прямых эфирах?")
            e.add_field(name="Текущий статус:", value=f"{status}")
            e.set_thumbnail(url="https://discord.com/assets/a6d05968d7706183143518d96c9f066e.svg")
            e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            await interaction.send(embed=e, components=[[Button(emoji="🔔", id="notifyon"),
                                                         Button(emoji="🔕", id="notifyoff")]])
        except Exception:
            await self.errors("Подписка:", format_exc())

    @loop()
    async def player(self):
        try:
            trigger = 0
            while True:
                vc = None
                try:
                    for x in self.BOT.voice_clients:
                        await x.disconnect()
                except Exception:
                    pass
                try:
                    vc = await self.BOT.get_channel(int(CHANNELS["Голосовой"])).connect()
                    vc.play(FFmpegPCMAudio("https://everhoof.ru/320"))
                except Exception:
                    pass
                icon, artist, title, = "//everhoof.ru/favicon.png", "Everhoof Radio", "Everhoof Radio"
                duration, delta = 0, 0
                try:
                    content = await connect("wss://everhoof.ru:443/ws")
                    track = loads(await content.recv())
                    icon, artist, title, duration = track["art"], track["artist"], track["title"], track["duration"]
                    if len(icon) == 0:
                        icon = "//everhoof.ru/favicon.png"
                    if len(artist) == 0:
                        try:
                            artist = split(" - ", track["Имя"])[0]
                        except Exception:
                            pass
                        if len(artist) == 0:
                            artist = "Everhoof Radio"
                    if len(title) == 0:
                        try:
                            title = split(" - ", track["Имя"])[1]
                        except Exception:
                            pass
                        if len(title) == 0:
                            title = "Everhoof Radio"
                    if len(str(duration)) == 0:
                        duration = 60
                    try:
                        btime = "".join(findall(r"\d{2}:\d{2}:\d{2}", track["ends_at"])[0])
                        ctime = datetime.now(timezone('Europe/Moscow')).strftime("%H:%M:%S")
                        time_1 = datetime.strptime(f'{btime}', "%H:%M:%S")
                        time_2 = datetime.strptime(f'{ctime}', "%H:%M:%S")
                        h, m, s = str(time_1 - time_2).strip().split(":")
                        delta = int(h) * 3600 + int(m) * 60 + int(s) + 1
                    except Exception:
                        delta = 60
                    if duration == 0:
                        if track["starts_at"] == track["ends_at"]:
                            try:
                                content = loads(get("https://everhoof.ru/api/calendar/nogard").text)[0]
                                starts_at = "".join(findall(r"\d+", content["starts_at"])[:6])
                                ends_at = "".join(findall(r"\d+", content["ends_at"])[:6])
                                dtime = datetime.now(timezone('Europe/Moscow')).strftime(
                                    "%Y%m%d%H%M%S")
                                if int(starts_at) <= int(dtime) <= int(ends_at):
                                    artist, title, delta = "В эфире", content["summary"], 60
                                    if trigger == 0:
                                        members = ""
                                        for mem in DB.server.player.find_one({"_id": "Уведомления"}):
                                            if str(mem) == "_id":
                                                continue
                                            members += f"<@{mem}>, "
                                        await self.BOT.get_channel(int(CHANNELS["Вечеринка"])).send(
                                            f"{members}Сейчас в прямом эфире \"{title}\"!")
                                        trigger += 1
                            except Exception:
                                delta = 60
                        else:
                            delta = 60
                except Exception:
                    pass
                d = str(timedelta(seconds=duration))[2:]
                try:
                    post = await self.BOT.get_channel(int(CHANNELS["Вечеринка"])).fetch_message(
                        int(DB.server.player.find_one({"_id": "Посты"})["Плеер"]))
                    await post.delete()
                except Exception:
                    pass
                e = Embed(title="Сейчас играет:", color=0x00FFFF)
                e.set_thumbnail(url=f"https:{icon}")
                e.add_field(name=title, inline=False,
                            value=f"Исполнитель: {artist}\nДлительность: {d}\nСсылка: https://everhoof.ru")
                e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
                try:
                    mes = await self.BOT.get_channel(int(CHANNELS["Вечеринка"])).send(
                        embed=e, components=[[Button(label="История", style=ButtonStyle.green),
                                              Button(emoji="⚙", style=ButtonStyle.blue, id="settings")]])
                    DB.server.player.update_one({"_id": "Посты"}, {"$set": {"Плеер": int(mes.id)}})
                except Exception:
                    pass
                await sleep(int(delta))
        except Exception:
            await self.errors("Плеер:", format_exc())

    @Cog.listener()
    async def on_button_click(self, interaction):
        try:
            if interaction.component.label == "История":
                e = Embed(title="История:", color=interaction.user.color)
                soup = BeautifulSoup(get("https://everhoof.ru/").text, "html.parser")("li", "history-modal__item")
                for s in soup:
                    track = str(s.get_text(strip=True))
                    a = track.split(". ")
                    b = a[1].split(" - ")
                    e.add_field(name=f"{a[0]}. {b[1]}", value=f"Исполнитель: {b[0]}", inline=False)
                e.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
                await interaction.send(embed=e)
        except Exception:
            await self.errors("Кнопка История:", format_exc())
        try:
            if interaction.component.id == "settings":
                await self.subscribe(interaction)
        except Exception:
            await self.errors("Кнопка Настройки:", format_exc())
        try:
            if interaction.component.id == "notifyon":
                try:
                    DB.server.player.update_one(
                        {"_id": "Уведомления"}, {"$set": {str(interaction.user.id): str(interaction.user.name)}})
                except Exception:
                    pass
                await self.subscribe(interaction)
        except Exception:
            await self.errors("Кнопка Включить уведомления:", format_exc())
        try:
            if interaction.component.id == "notifyoff":
                DB.server.player.update_one({"_id": "Уведомления"}, {"$unset": {str(interaction.user.id): 1}})
                await self.subscribe(interaction)
        except Exception:
            await self.errors("Кнопка Отключить уведомления:", format_exc())


def setup(bot):
    bot.add_cog(Player(bot))
