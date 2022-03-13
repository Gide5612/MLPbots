import asyncio
import datetime
import os
import random
import re
import sys
import threading
import traceback

import discord
import discord.ext
import discord_components
import pymongo
import pytz

BOT = discord.ext.commands.Bot(command_prefix=discord.ext.commands.when_mentioned_or("!"), help_command=None,
                               intents=discord.Intents.all())

DB = pymongo.MongoClient("+://:@.../?=&w=")

CHANNELS = DB.mlpsbots.server.find_one({"_id": "Каналы"})
POSTS = DB.mlpsbots.server.find_one({"_id": "Посты"})
ROLES = DB.mlpsbots.server.find_one({"_id": "Роли"})
QUOTES = DB.mlpsbots.server.find_one({"_id": "Цытаты"})["quotes"]

JWR, IDS, IDL = 496139824500178964, 868148805722337320, 868150460735971328

GREEN, RED, BLUE, GRAY, LINK = 3, 4, 1, 2, 5


def autores():
    try:
        threading.Timer(1, autores).start()
        atime = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H%M%S"))
        print(atime)
        if atime == 80000 or atime == 200000:
            os.execl(sys.executable, "python", "mlpbots.py", *sys.argv[1:])
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
            os.execl(sys.executable, "python", "mlpbots.py", *sys.argv[1:])
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
        await messages(BOT.user, "Запускается...")
    except Exception:
        await errors("Сообщение запуска:", traceback.format_exc())
    try:
        if BOT.user.id == IDS:
            await BOT.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching, name="за Эквестрией..."))
        if BOT.user.id == IDL:
            await BOT.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name="тишину ночи..."))
    except Exception:
        await errors("Установка статуса:", traceback.format_exc())
    try:
        try:
            rules = await BOT.get_channel(int(CHANNELS["добро_пожаловать"])).fetch_message(int(POSTS["Правила"]))
            await rules.delete()
        except Exception:
            print(traceback.format_exc())
        e1 = discord.Embed(title="Приветствуем тебя милая поняшка в нашем клубе!", color=0x008000,
                           description="<a:a136:912433125244665866> Несмотря на название, этот клуб создан для "
                                       "простого и дружественного общения всех участников на любые возможные темы. "
                                       "Но тем не менее, для поддержания уютной и комфортной атмосферы, у нас есть "
                                       "несколько правил:")
        e1.add_field(name="Правила:",
                     value=":one: Не использовать нецензурную лексику, в том числе замаскированную! Не обсуждать и "
                           "не использовать материалы для взрослых!\n\n:two: Не оскорблять других участников! Не "
                           "обсуждать и не указывать на внешность, голос, и подобные биологические особенности "
                           "других участников!\n\n:three: Не обсуждать религию, политику, расовые особенности, и "
                           "другие подобные темы, которые могут задеть и оскорбить чувства других участников!")
        e1.add_field(name="<a:a118:912433128268783656> Дружба - это чудо!",
                     value="В нашем клубе действует главный закон Эквестрии: Дружба - это чудо! И мы искренне "
                           "надеемся на поддержание этого всеми участниками клуба!")
        e1.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/915419331804954634/PPWHY.png")
        e1.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        rulesid = await BOT.get_channel(int(CHANNELS["добро_пожаловать"])).send(embed=e1, components=[[
            discord_components.Button(label="Согласен!", style=GREEN),
            discord_components.Button(label="Не согласен!", style=RED)]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Правила": int(rulesid.id)}})
    except Exception:
        await errors("Пост Правила:", traceback.format_exc())
    try:
        try:
            roles = await BOT.get_channel(int(CHANNELS["роли_сервера"])).fetch_message(int(POSTS["Роли"]))
            await roles.delete()
        except Exception:
            print(traceback.format_exc())
        e2 = discord.Embed(title="На нашем сервере есть 4 основные роли:", color=0xFFFF00,
                           description="<@&798875106868854804> - пони, которые непосредственно управляют сервером."
                                       "\n\n<@&798877123413540876> - пони, которые следят за порядком на сервере."
                                       "\n\n<@&798878290437603369> - основной табун. Добрые и культурные пони сервера."
                                       "\n\n<@&907438760663322634> - те, кто несогласны с правилами, только наблюдают."
                                       "\n\n<a:a131:912433126716866653> Роли <@&798878290437603369> и "
                                       "<@&907438760663322634> выдают автоматически <@&799037336599134208>!")
        e2.add_field(name="Также есть ещё дополнительная роль:",
                     value="Она открывает доступ к закрытой категории, где не действуют абсолютно никакие правила и "
                           "модерация. Истинный мир хаоса! Там всем управляет только Дискорд, и даже "
                           "<@&799037336599134208> бессильны... Чтобы получить эту роль, нажмите на соответствующую "
                           "кнопку под этим сообщением.")
        e2.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/915449826731257956/Cheer.png")
        e2.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        rolesid = await BOT.get_channel(int(CHANNELS["роли_сервера"])).send(embed=e2, components=[[
            discord_components.Button(label="18+", style=GRAY)]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Роли": int(rolesid.id)}})
    except Exception:
        await errors("Пост Роли:", traceback.format_exc())
    try:
        try:
            rases = await BOT.get_channel(int(CHANNELS["роли_сервера"])).fetch_message(int(POSTS["Расы"]))
            await rases.delete()
        except Exception:
            print(traceback.format_exc())
        e3 = discord.Embed(title="А еще у нас есть расы:", color=0xFFA500,
                           description=f"<a:a149:919732726888796220> <@&919382861512052747>\n\n"
                                       f"<a:a147:917553790016688138> <@&917562915400335420>\n\n"
                                       f"<a:a143:917553789798580264> <@&917563172242747392>\n\n"
                                       f"<a:a140:917553790083801188> <@&917563225195827252>\n\n"
                                       f"<a:a139:917553790083825675> <@&917563537331740672>\n\n"
                                       f"<a:a138:917553789823754331> <@&917563336240009247>\n\n"
                                       f"<a:a137:917553790259957800> <@&917563653899825152>\n\n"
                                       f"<a:a107:907931049579917342> <@&917563852021989478>\n\n"
                                       f"<a:a126:912433127027249242> <@&917563886314594336>\n\n"
                                       f"<a:a111:907931053757456444> <@&917563928211521547>\n\n"
                                       f"Чтобы выбрать себе расу нажмите на соответствующую ей кнопку под этим "
                                       f"сообщением. Одновременно себе можно выбрать только одну расу!")
        e3.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/917800054042009630/chars.png")
        e3.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        rasesid = await BOT.get_channel(int(CHANNELS["роли_сервера"])).send(embed=e3, components=[[
            discord_components.Button(emoji=BOT.get_emoji(919732726888796220), style=GRAY, id="Аликорны"),
            discord_components.Button(emoji=BOT.get_emoji(917553790016688138), style=GRAY, id="Единороги"),
            discord_components.Button(emoji=BOT.get_emoji(917553789798580264), style=GRAY, id="Пегасы"),
            discord_components.Button(emoji=BOT.get_emoji(917553790083801188), style=GRAY, id="Земные_пони"),
            discord_components.Button(emoji=BOT.get_emoji(917553790083825675), style=GRAY, id="Кирины")],
            [discord_components.Button(emoji=BOT.get_emoji(917553789823754331), style=GRAY, id="Оборотни"),
             discord_components.Button(emoji=BOT.get_emoji(917553790259957800), style=GRAY, id="Гиппогрифы"),
             discord_components.Button(emoji=BOT.get_emoji(907931049579917342), style=GRAY, id="Грифоны"),
             discord_components.Button(emoji=BOT.get_emoji(912433127027249242), style=GRAY, id="Кристальные_пони"),
             discord_components.Button(emoji=BOT.get_emoji(907931053757456444), style=GRAY, id="Зебры")]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Расы": int(rasesid.id)}})
    except Exception:
        await errors("Пост Расы:", traceback.format_exc())
    try:
        try:
            minis = await BOT.get_channel(int(CHANNELS["роли_сервера"])).fetch_message(int(POSTS["Министерства"]))
            await minis.delete()
        except Exception:
            print(traceback.format_exc())
        e4 = discord.Embed(title="И министерства:", color=0xFF0000,
                           description=f"<a:a149:917553790100590622> <@&917564125306044458>\n\n"
                                       f"<a:a149:917553790012510279> <@&917564125570301962>\n\n"
                                       f"<a:a149:917553790427742298> <@&917564269233582103>\n\n"
                                       f"<a:a149:917553790079619126> <@&917564380588175411>\n\n"
                                       f"<a:a149:917553790016688129> <@&917564425827921980>\n\n"
                                       f"<a:a149:917553790159298570> <@&917564471327723540>\n\n"
                                       f"Чтобы присоединиться к министерству нажмите на соответствующую ему кнопку "
                                       f"под этим сообщением. Одновременно присоединится можно только к одному "
                                       f"министерству!")
        e4.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/917587318930550794/mine6.png")
        e4.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        minisid = await BOT.get_channel(int(CHANNELS["роли_сервера"])).send(embed=e4, components=[[
            discord_components.Button(emoji=BOT.get_emoji(917553790100590622), style=GRAY, id="Стиля"),
            discord_components.Button(emoji=BOT.get_emoji(917553790012510279), style=GRAY, id="Мира"),
            discord_components.Button(emoji=BOT.get_emoji(917553790427742298), style=GRAY, id="Морали")],
            [discord_components.Button(emoji=BOT.get_emoji(917553790079619126), style=GRAY, id="Технологий"),
             discord_components.Button(emoji=BOT.get_emoji(917553790016688129), style=GRAY, id="Наук"),
             discord_components.Button(emoji=BOT.get_emoji(917553790159298570), style=GRAY, id="Крутости")]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Министерства": int(minisid.id)}})
    except Exception:
        await errors("Пост Министества:", traceback.format_exc())
    try:
        try:
            forum = await BOT.get_channel(int(CHANNELS["объявления"])).fetch_message(int(POSTS["Форум"]))
            await forum.delete()
        except Exception:
            print(traceback.format_exc())
        e5 = discord.Embed(title="Наши темы на форуме:", color=0x00FFFF)
        e5.add_field(name="MY LITTLE PONY: Магия Принцесс:", value="https://4pda.to/forum/index.php?showtopic=396777")
        e5.add_field(name="Bronies 4PDA:", value="https://4pda.to/forum/index.php?showtopic=403239")
        e5.set_thumbnail(url="https://ds-assets.cdn.devapps.ru/EoAVz2z2w96Lx0PqpnsAuOJVFUbPz1uWLqlwNgtOG92kP.png")
        e5.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        forumid = await BOT.get_channel(int(CHANNELS["объявления"])).send(embed=e5, components=[[
            discord_components.Button(label="MY LITTLE PONY: Магия Принцесс", style=LINK,
                                      url="https://4pda.to/forum/index.php?showtopic=396777"),
            discord_components.Button(label="Bronies 4PDA", style=LINK,
                                      url="https://4pda.to/forum/index.php?showtopic=403239")]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Форум": int(forumid.id)}})
    except Exception:
        await errors("Пост Наши темы на форуме:", traceback.format_exc())
    try:
        try:
            discords = await BOT.get_channel(int(CHANNELS["объявления"])).fetch_message(int(POSTS["Друзья"]))
            await discords.delete()
        except Exception:
            print(traceback.format_exc())
        e6 = discord.Embed(title="Наши друзья в Дискорде:", color=0xFF69B4)
        e6.add_field(name="My Little Pony Gameloft Вики:", value="https://discord.gg/sJAwM2yS98")
        e6.add_field(name="Дружба – это Чудо Вики:", value="https://discord.gg/79TZp5q")
        e6.add_field(name="Everhoof Radio:", value="https://discord.gg/YV9HhHRd4M")
        e6.add_field(name="Anon2Anon:", value="https://discord.gg/trxVtrj")
        e6.add_field(name="Fallout Equestria: REMAINS:", value="https://discord.gg/qWYAbsp")
        e6.add_field(name="Legends of Equestria:", value="https://discord.gg/uPvn8Xr")
        e6.add_field(name="MC4EP:", value="https://discord.gg/Kd5HYj6")
        e6.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/929399822895710228/cran.png")
        e6.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        discordsid = await BOT.get_channel(int(CHANNELS["объявления"])).send(embed=e6, components=[[
            discord_components.Button(label="My Little Pony Gameloft Вики", url="https://discord.gg/sJAwM2yS98",
                                      style=LINK),
            discord_components.Button(label="Дружба – это Чудо Вики", url="https://discord.gg/79TZp5q", style=LINK)], [
            discord_components.Button(label="Everhoof Radio", url="https://discord.gg/YV9HhHRd4M", style=LINK),
            discord_components.Button(label="Anon2Anon", url="https://discord.gg/trxVtrj", style=LINK),
            discord_components.Button(label="Fallout Equestria: REMAINS", url="https://discord.gg/qWYAbsp",
                                      style=LINK)], [
            discord_components.Button(label="Legends of Equestria", url="https://discord.gg/uPvn8Xr", style=LINK),
            discord_components.Button(label="MC4EP", url="https://discord.gg/Kd5HYj6", style=LINK)]])
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Друзья": int(discordsid.id)}})
    except Exception:
        await errors("Пост Наши друзья в Дискорде:", traceback.format_exc())
    try:
        try:
            instruction = await BOT.get_channel(int(CHANNELS["объявления"])).fetch_message(int(POSTS["Инструкция"]))
            await instruction.delete()
        except Exception:
            print(traceback.format_exc())
        e7 = discord.Embed(title="Инструкция по использованию ботов:", color=0x0000FF,
                           description="1. Вызвать список всех текущих команд бота можно командой: !help\n\n2. "
                                       "Вместо \"!\" можно использовать упоминание бота, например: "
                                       "<@868150460735971328> help\n\n3. Список \"Help\" является динамически "
                                       "генерируемым, в зависимости от текущих прав пользователя. Проще говоря, у "
                                       "<@&798878290437603369> будет свой список доступных команд, у "
                                       "<@&798877123413540876> свой, у <@&798875106868854804> свой.\n\n4. У каждого "
                                       "бота свой список команд. Но те боты, которые закреплены за определенным "
                                       "каналом, будут реагировать на команды только в своем канале.\n\n5. Все "
                                       "параметры для команд являются полностью необязательными. Например команда "
                                       "\"!ava <@868150460735971328>\" выведет аватарку пользователя "
                                       "<@868150460735971328>, но если вызвать просто команду \"!ava\", то она "
                                       "выведет вашу собственную аватарку.\n\n6. Такие команды как \"text\" и "
                                       "\"voice\" создают для вас личные каналы со всеми возможными правами. "
                                       "Проще говоря вы являетесь полноценным Администратором в своих личных каналах.")
        e7.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/946392955000872981/swet.png")
        e7.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        instructionid = await BOT.get_channel(int(CHANNELS["объявления"])).send(embed=e7)
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Инструкция": int(instructionid.id)}})
    except Exception:
        await errors("Пост Инструкция по использованию ботов:", traceback.format_exc())
    try:
        try:
            moderation = await BOT.get_channel(int(CHANNELS["объявления"])).fetch_message(int(POSTS["Модерация"]))
            await moderation.delete()
        except Exception:
            print(traceback.format_exc())
        e8 = discord.Embed(title="Пользовательская модерация:", color=0x4B0082,
                           description="1. Теперь все пользователи сервера могут сами решать, какие сообщения "
                                       "действительно полезные, а какие стоит сразу удалять. Суть заключается в том, "
                                       "что вы можете ставить под любым сообщением лайк, или дизлайк: 👍 👎\n\n2. Если "
                                       "под сообщением набирается 3 лайка, оно автоматически закрепляется в канале.\n"
                                       "\n3. Если под сообщением набирается 3 дизлайка, оно автоматически удаляется."
                                       "\n\n4. Но! Система также учитывает разницу. Например, если сообщение имеет 2 "
                                       "лайка, и 1 дизлайк, то результатом будет 1 лайк и -1 дизлайк. Что бы удалить "
                                       "такое сообщение, нужно (3 дизлайка + количество лайков) дизлайка.")
        e8.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/946395421171929109/like.png")
        e8.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        moderationid = await BOT.get_channel(int(CHANNELS["объявления"])).send(embed=e8)
        await moderationid.add_reaction("👍")
        await moderationid.add_reaction("👎")
        DB.mlpsbots.server.update_one({"_id": "Посты"}, {"$set": {"Модерация": int(moderationid.id)}})
    except Exception:
        await errors("Пост Пользовательская модерация:", traceback.format_exc())
    try:
        if BOT.user.id == IDS:
            await messages(BOT.user, "Снова \"Смотрит за Эквестрией...\"")
        if BOT.user.id == IDL:
            await messages(BOT.user, "Снова \"Слушает тишину ночи...\"")
    except Exception:
        await errors("Сообщение готовности:", traceback.format_exc())
    try:
        for guild in BOT.guilds:
            for member in guild.members:
                delta = datetime.datetime.now() - member.joined_at
                user = DB.mlpsbots.achievements.find_one({"_id": member.id})
                if user is None:
                    DB.mlpsbots.achievements.insert_one({
                        "_id": int(member.id), "Имя": member.name, "Дни": int(delta.days)})
                else:
                    DB.mlpsbots.achievements.update_one({"_id": int(member.id)}, {"$set": {"Дни": int(delta.days)}})
                try:
                    if int(delta.days) >= 30:
                        if "achievements" in user:
                            if "d30" not in user["achievements"]:
                                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                    f"**Ей! <@{member.id}> только что получил достижение!**",
                                    file=discord.File("achievements/d30.png"))
                                DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                    {"$push": {"achievements": "d30"}})
                        else:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{member.id}> только что получил достижение!**",
                                file=discord.File("achievements/d30.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                {"$push": {"achievements": "d30"}})
                    if int(delta.days) >= 90:
                        if "achievements" in user:
                            if "d90" not in user["achievements"]:
                                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                    f"**Ей! <@{member.id}> только что получил достижение!**",
                                    file=discord.File("achievements/d90.png"))
                                DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                    {"$push": {"achievements": "d90"}})
                        else:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{member.id}> только что получил достижение!**",
                                file=discord.File("achievements/d90.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                {"$push": {"achievements": "d90"}})
                    if int(delta.days) >= 180:
                        if "achievements" in user:
                            if "d180" not in user["achievements"]:
                                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                    f"**Ей! <@{member.id}> только что получил достижение!**",
                                    file=discord.File("achievements/d180.png"))
                                DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                    {"$push": {"achievements": "d180"}})
                        else:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{member.id}> только что получил достижение!**",
                                file=discord.File("achievements/d180.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                {"$push": {"achievements": "d180"}})
                    if int(delta.days) >= 365:
                        if "achievements" in user:
                            if "d365" not in user["achievements"]:
                                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                    f"**Ей! <@{member.id}> только что получил достижение!**",
                                    file=discord.File("achievements/d365.png"))
                                DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                    {"$push": {"achievements": "d365"}})
                        else:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{member.id}> только что получил достижение!**",
                                file=discord.File("achievements/d365.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                {"$push": {"achievements": "d365"}})
                    if int(delta.days) >= 1095:
                        if "achievements" in user:
                            if "d1095" not in user["achievements"]:
                                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                    f"**Ей! <@{member.id}> только что получил достижение!**",
                                    file=discord.File("achievements/d1095.png"))
                                DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                    {"$push": {"achievements": "d1095"}})
                        else:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{member.id}> только что получил достижение!**",
                                file=discord.File("achievements/d1095.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(member.id)},
                                                                {"$push": {"achievements": "d1095"}})
                except Exception:
                    print(traceback.format_exc())
    except Exception:
        await errors("Достижения дней:", traceback.format_exc())


@BOT.event
async def on_message(message):
    try:
        await BOT.process_commands(message)
    except Exception:
        await errors("process_commands:", traceback.format_exc())
    try:
        wor = "кве|рог|пег|рыл|пин|пай|рит|рад|дэш|даш|иск|тва|ппл|дже|фла|шай|лун|сел"
        if message.author.id != IDS and message.author.id != IDL:
            if len(re.findall(rf"{wor}", message.content.lower())) > 0:
                await message.channel.send(f"{QUOTES[random.randint(0, 90)]}")
    except Exception:
        await errors("Рандомные Фразы:", traceback.format_exc())
    try:
        if str(message.channel.type) == "text":
            user = DB.mlpsbots.achievements.find_one({"_id": message.author.id})
            if user is None:
                DB.mlpsbots.achievements.insert_one({
                    "_id": int(message.author.id), "Имя": message.author.name, "Сообщения": int(1)})
            else:
                if "Сообщения" in user:
                    DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                        {"$inc": {"Сообщения": int(1)}})
                else:
                    DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                        {"$set": {"Сообщения": int(1)}})
            try:
                if int(user["Сообщения"]) >= 500:
                    if "achievements" in user:
                        if "m500" not in user["achievements"]:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{message.author.id}> только что получил достижение!**",
                                file=discord.File("achievements/m500.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                                {"$push": {"achievements": "m500"}})
                    else:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{message.author.id}> только что получил достижение!**",
                            file=discord.File("achievements/m500.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                            {"$push": {"achievements": "m500"}})
                if int(user["Сообщения"]) >= 1000:
                    if "achievements" in user:
                        if "m1000" not in user["achievements"]:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{message.author.id}> только что получил достижение!**",
                                file=discord.File("achievements/m1000.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                                {"$push": {"achievements": "m1000"}})
                    else:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{message.author.id}> только что получил достижение!**",
                            file=discord.File("achievements/m1000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                            {"$push": {"achievements": "m1000"}})
                if int(user["Сообщения"]) >= 2000:
                    if "achievements" in user:
                        if "m2000" not in user["achievements"]:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{message.author.id}> только что получил достижение!**",
                                file=discord.File("achievements/m2000.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                                {"$push": {"achievements": "m2000"}})
                    else:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{message.author.id}> только что получил достижение!**",
                            file=discord.File("achievements/m2000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                            {"$push": {"achievements": "m2000"}})
                if int(user["Сообщения"]) >= 5000:
                    if "achievements" in user:
                        if "m5000" not in user["achievements"]:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{message.author.id}> только что получил достижение!**",
                                file=discord.File("achievements/m5000.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                                {"$push": {"achievements": "m5000"}})
                    else:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{message.author.id}> только что получил достижение!**",
                            file=discord.File("achievements/m5000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                            {"$push": {"achievements": "m5000"}})
                if int(user["Сообщения"]) >= 10000:
                    if "achievements" in user:
                        if "m10000" not in user["achievements"]:
                            await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                f"**Ей! <@{message.author.id}> только что получил достижение!**",
                                file=discord.File("achievements/m10000.png"))
                            DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                                {"$push": {"achievements": "m10000"}})
                    else:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{message.author.id}> только что получил достижение!**",
                            file=discord.File("achievements/m10000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                            {"$push": {"achievements": "m10000"}})
            except Exception:
                print(traceback.format_exc())
    except Exception:
        await errors("Достижения: Сообщения:", traceback.format_exc())
    try:
        if message.content.startswith("!achieve"):
            if message.author.bot:
                if message.content.endswith("xjozklsnrfwmqdhaja"):
                    await message.delete(delay=1)
                    user2 = re.findall(r"\d+", message.content)
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user2[0]}> только что получил достижение!**",
                        file=discord.File("achievements/pp.png"))
                    if DB.mlpsbots.achievements.find_one({"_id": user2[0]}) is None:
                        DB.mlpsbots.achievements.insert_one({
                            "_id": int(user2[0]), "Имя": discord.utils.get(
                                message.guild.members, id=int(user2[0])).name, "achievements": ["pp"]})
                    else:
                        DB.mlpsbots.achievements.update_one({"_id": int(user2[0])}, {"$push": {"achievements": ["pp"]}})
    except Exception:
        await errors("Достижение \"Неугомонная Морквуша\":", traceback.format_exc())
    try:
        if len(message.mentions) != 0:
            for mess in message.mentions:
                if int(mess.id) != int(message.author.id):
                    if message.author.id != IDS and message.author.id != IDL:
                        user3 = DB.mlpsbots.achievements.find_one({"_id": mess.id})
                        if user3 is None:
                            DB.mlpsbots.achievements.insert_one({
                                "_id": int(mess.id), "Имя": mess.name, "Упоминания": int(1)})
                        else:
                            if "Упоминания" in user3:
                                DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                    {"$inc": {"Упоминания": int(1)}})
                            else:
                                DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                    {"$set": {"Упоминания": int(1)}})
                        try:
                            if int(user3["Упоминания"]) >= 50:
                                if "achievements" in user3:
                                    if "mt50" not in user3["achievements"]:
                                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                            f"**Ей! <@{mess.id}> только что получил достижение!**",
                                            file=discord.File("achievements/mt50.png"))
                                        DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                            {"$push": {"achievements": "mt50"}})
                                else:
                                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                        f"**Ей! <@{mess.id}> только что получил достижение!**",
                                        file=discord.File("achievements/mt50.png"))
                                    DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                        {"$push": {"achievements": "mt50"}})
                            if int(user3["Упоминания"]) >= 100:
                                if "achievements" in user3:
                                    if "mt100" not in user3["achievements"]:
                                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                            f"**Ей! <@{mess.id}> только что получил достижение!**",
                                            file=discord.File("achievements/mt100.png"))
                                        DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                            {"$push": {"achievements": "mt100"}})
                                else:
                                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                        f"**Ей! <@{mess.id}> только что получил достижение!**",
                                        file=discord.File("achievements/mt100.png"))
                                    DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                        {"$push": {"achievements": "mt100"}})
                            if int(user3["Упоминания"]) >= 300:
                                if "achievements" in user3:
                                    if "mt300" not in user3["achievements"]:
                                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                            f"**Ей! <@{mess.id}> только что получил достижение!**",
                                            file=discord.File("achievements/mt300.png"))
                                        DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                            {"$push": {"achievements": "mt300"}})
                                else:
                                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                        f"**Ей! <@{mess.id}> только что получил достижение!**",
                                        file=discord.File("achievements/mt300.png"))
                                    DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                        {"$push": {"achievements": "mt300"}})
                            if int(user3["Упоминания"]) >= 1000:
                                if "achievements" in user3:
                                    if "mt1000" not in user3["achievements"]:
                                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                            f"**Ей! <@{mess.id}> только что получил достижение!**",
                                            file=discord.File("achievements/mt1000.png"))
                                        DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                            {"$push": {"achievements": "mt1000"}})
                                else:
                                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                        f"**Ей! <@{mess.id}> только что получил достижение!**",
                                        file=discord.File("achievements/mt1000.png"))
                                    DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                        {"$push": {"achievements": "mt1000"}})
                            if int(user3["Упоминания"]) >= 5000:
                                if "achievements" in user3:
                                    if "mt5000" not in user3["achievements"]:
                                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                            f"**Ей! <@{mess.id}> только что получил достижение!**",
                                            file=discord.File("achievements/mt5000.png"))
                                        DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                            {"$push": {"achievements": "mt5000"}})
                                else:
                                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                                        f"**Ей! <@{mess.id}> только что получил достижение!**",
                                        file=discord.File("achievements/mt5000.png"))
                                    DB.mlpsbots.achievements.update_one({"_id": int(mess.id)},
                                                                        {"$push": {"achievements": "mt5000"}})
                        except Exception:
                            print(traceback.format_exc())
    except Exception:
        await errors("Достижения: Упоминания:", traceback.format_exc())
    try:
        if message.content.startswith("!ban"):
            user4 = DB.mlpsbots.achievements.find_one({"_id": message.author.id})
            if "ban" not in user4["achievements"]:
                await BOT.get_channel(int(CHANNELS["достижения"])).send(
                    f"**Ей! <@{message.author.id}> только что получил достижение!**",
                    file=discord.File("achievements/ban.png"))
                DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                    {"$push": {"achievements": "ban"}})
            if str(message.content) == "!ban <@!496139824500178964>":
                if "banjwr" not in user4["achievements"]:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{message.author.id}> только что получил достижение!**",
                        file=discord.File("achievements/banjwr.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                        {"$push": {"achievements": "banjwr"}})
            if str(message.content) == "!ban @everyone":
                if "baneveryone" not in user4["achievements"]:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{message.author.id}> только что получил достижение!**",
                        file=discord.File("achievements/baneveryone.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                        {"$push": {"achievements": "baneveryone"}})
    except Exception:
        await errors("Достижение \"Бан\":", traceback.format_exc())


@BOT.event
async def on_message_delete(message):
    try:
        user = DB.mlpsbots.achievements.find_one({"_id": message.author.id})
        if user is not None:
            if "Сообщения" in user:
                DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)}, {"$inc": {"Сообщения": int(-1)}})
    except Exception:
        await errors("Удаление сообщения:", traceback.format_exc())


@BOT.event
async def on_bulk_message_delete(messages):
    try:
        for message in messages:
            user = DB.mlpsbots.achievements.find_one({"_id": message.author.id})
            if user is not None:
                if "Сообщения" in user:
                    DB.mlpsbots.achievements.update_one({"_id": int(message.author.id)},
                                                        {"$inc": {"Сообщения": int(-1)}})
    except Exception:
        await errors("Массовое удаление сообщений:", traceback.format_exc())


@BOT.event
async def on_raw_reaction_add(payload):
    try:
        post = await BOT.get_channel(payload.channel_id).fetch_message(payload.message_id)
        like, dlike = 0, 0
        for reaction in post.reactions:
            if reaction.emoji == "👍":
                like = int(reaction.count)
            if reaction.emoji == "👎":
                dlike = int(reaction.count)
        if like - dlike == 3:
            await post.pin()
        if dlike - like == 3:
            await post.delete()
    except Exception:
        await errors(f"Пользовательская модерация:", traceback.format_exc())


@BOT.event
async def on_reaction_add(reaction, user):
    try:
        usr = DB.mlpsbots.achievements.find_one({"_id": user.id})
        if str(reaction) == "👍":
            if usr is None:
                DB.mlpsbots.achievements.insert_one({"_id": int(user.id), "Имя": user.name, "Лайки": int(1)})
            else:
                if "Лайки" in usr:
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$inc": {"Лайки": int(1)}})
                else:
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$set": {"Лайки": int(1)}})
        if str(reaction) == "👎":
            if usr is None:
                DB.mlpsbots.achievements.insert_one({"_id": int(user.id), "Имя": user.name, "Дизлайки": int(1)})
            else:
                if "Дизлайки" in usr:
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$inc": {"Дизлайки": int(1)}})
                else:
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$set": {"Дизлайки": int(1)}})
        try:
            if int(usr["Лайки"]) >= 10:
                if "achievements" in usr:
                    if "l10" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File(
                                "achievements/l10.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l10"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/l10.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l10"}})
            if int(usr["Лайки"]) >= 50:
                if "achievements" in usr:
                    if "l50" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/l50.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l50"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/l50.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l50"}})
            if int(usr["Лайки"]) >= 100:
                if "achievements" in usr:
                    if "l100" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/l100.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l100"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/l100.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l100"}})
            if int(usr["Лайки"]) >= 300:
                if "achievements" in usr:
                    if "l300" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/l300.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l300"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/l300.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l300"}})
            if int(usr["Лайки"]) >= 1000:
                if "achievements" in usr:
                    if "l1000" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/l1000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l1000"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/l1000.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "l1000"}})
        except Exception:
            print(traceback.format_exc())
        try:
            if int(usr["Дизлайки"]) >= 10:
                if "achievements" in usr:
                    if "dl10" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/dl10.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl10"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/dl10.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl10"}})
            if int(usr["Дизлайки"]) >= 50:
                if "achievements" in usr:
                    if "dl50" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/dl50.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl50"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/dl50.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl50"}})
            if int(usr["Дизлайки"]) >= 100:
                if "achievements" in usr:
                    if "dl100" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/dl100.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl100"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/dl100.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl100"}})
            if int(usr["Дизлайки"]) >= 300:
                if "achievements" in usr:
                    if "dl300" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/dl300.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl300"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/dl300.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl300"}})
            if int(usr["Дизлайки"]) >= 1000:
                if "achievements" in usr:
                    if "dl1000" not in usr["achievements"]:
                        await BOT.get_channel(int(CHANNELS["достижения"])).send(
                            f"**Ей! <@{user.id}> только что получил достижение!**",
                            file=discord.File("achievements/dl1000.png"))
                        DB.mlpsbots.achievements.update_one({"_id": int(user.id)},
                                                            {"$push": {"achievements": "dl1000"}})
                else:
                    await BOT.get_channel(int(CHANNELS["достижения"])).send(
                        f"**Ей! <@{user.id}> только что получил достижение!**",
                        file=discord.File("achievements/dl1000.png"))
                    DB.mlpsbots.achievements.update_one({"_id": int(user.id)}, {"$push": {"achievements": "dl1000"}})
        except Exception:
            print(traceback.format_exc())
    except Exception:
        await errors("Достижения за реакции:", traceback.format_exc())


@BOT.event
async def on_member_join(member):
    try:
        e = discord.Embed(title="В наш клуб присоединилась милая поняшка!", color=0xBA55D3,
                          description=f"Поприветствуем: {member.mention}!")
        e.set_thumbnail(url=member.avatar_url)
        e.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                     icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        await BOT.get_channel(int(CHANNELS["болталка"])).send(embed=e)
    except Exception:
        await errors("Новый участник:", traceback.format_exc())


@BOT.event
async def on_member_update(before, after):
    try:
        if before.id != JWR and after.id != JWR:
            rasdb = DB.mlpsbots.server.find_one({"_id": "Расы"})
            mindb = DB.mlpsbots.server.find_one({"_id": "Министерства"})
            rsb = []
            rsa = []
            for role in before.roles:
                rsb.append(role.id)
            for role in after.roles:
                rsa.append(role.id)
            if len(rsa) > len(rsb):
                for x in rsb:
                    rsa.remove(x)
                if re.findall(str(rsa[0]), str(rasdb)) or re.findall(str(rsa[0]), str(mindb)):
                    if re.findall(str(rsa[0]), str(rasdb)):
                        for key in rasdb:
                            if rasdb[key] == rsa[0] or rasdb[key] == "Расы":
                                continue
                            await after.remove_roles(discord.utils.get(after.guild.roles, id=int(rasdb[key])))
                    if re.findall(str(rsa[0]), str(mindb)):
                        for key in mindb:
                            if mindb[key] == rsa[0] or mindb[key] == "Министерства":
                                continue
                            await after.remove_roles(discord.utils.get(after.guild.roles, id=int(mindb[key])))
    except:
        await errors("Удаление ролей:", traceback.format_exc())


@BOT.event
async def on_button_click(interaction):
    try:
        if interaction.component.label == "Согласен!":
            await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['Пользователи'])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(ROLES['Пользователи']))
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(
                discord.utils.get(interaction.user.guild.roles, id=int(ROLES['Читатели'])))
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Кнопка Согласен:", traceback.format_exc())
    try:
        if interaction.component.label == "Не согласен!":
            await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['Читатели'])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(ROLES['Читатели']))
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(
                discord.utils.get(interaction.user.guild.roles, id=int(ROLES['Пользователи'])))
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Кнопка Не согласен:", traceback.format_exc())
    try:
        if interaction.component.label == "18+":
            role = discord.utils.get(interaction.user.guild.roles, id=int(ROLES['18+']))
            if discord.utils.get(interaction.user.roles, id=int(ROLES['18+'])) is None:
                await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['18+'])}>")
                await interaction.user.add_roles(role)
                await alerts(interaction.user, f"Выдана роль: {role}")
            else:
                await interaction.send(f"Поздравляем! Вам убрана роль <@&{int(ROLES['18+'])}>")
                await interaction.user.remove_roles(role)
                await alerts(interaction.user, f"Удалена роль: {role}")
    except Exception:
        await errors("Кнопка 18+:", traceback.format_exc())
    try:
        rasdb = DB.mlpsbots.server.find_one({"_id": "Расы"})
        if re.findall(str(interaction.component.id), str(rasdb)):
            await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(rasdb[interaction.component.id])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(rasdb[interaction.component.id]))
            await interaction.user.add_roles(role)
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Выдача Рас:", traceback.format_exc())
    try:
        mindb = DB.mlpsbots.server.find_one({"_id": "Министерства"})
        if re.findall(str(interaction.component.id), str(mindb)):
            await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(mindb[interaction.component.id])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(mindb[interaction.component.id]))
            await interaction.user.add_roles(role)
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Выдача Министерств:", traceback.format_exc())


# команды пользователей
@BOT.command(description="0", name="help", help="Показать список всех команд бота", brief="Не применимо", usage="help")
async def helpmenu(ctx):
    try:
        await ctx.message.delete(delay=1)
        e = discord.Embed(title="Список всех команд:", color=ctx.author.color)
        e.set_footer(text=f"В качестве префикса можно использовать знак ! или упоминание бота @{BOT.user.name}")
        list1 = [[x.description for x in BOT.commands], [x.name for x in BOT.commands], [x.help for x in BOT.commands],
                 [x.brief for x in BOT.commands], [x.usage for x in BOT.commands]]
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


@BOT.command(description="1", name="ava", help="Прислать аватарку пользователя", brief="Упоминание пользователя",
             usage="ava @Принцесса Луна")
async def ava(ctx, member: discord.Member = None):
    try:
        await ctx.message.delete(delay=1)
        if not member:
            member = ctx.message.author
        await ctx.send(member.avatar_url)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {member}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="1", name="info", help="Показать информацию о пользователе", brief="Упоминание пользователя",
             usage="info @Принцесса Луна")
async def info(ctx, member: discord.Member = None):
    try:
        await ctx.message.delete(delay=1)
        if not member:
            member = ctx.message.author
        e = discord.Embed(title="Информация о пользователе:", color=ctx.author.color)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Имя на сервере:", value=member.mention, inline=False)
        e.add_field(name="Дата добавления на сервер:", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"),
                    inline=False)
        e.add_field(name="Роли на сервере:",
                    value=" ".join([role.mention for role in list(reversed(member.roles[1:]))]), inline=True)
        e.add_field(name="Имя аккаунта:", value=f"{member.name}#{member.discriminator}", inline=False)
        e.add_field(name="ID аккаунта:", value=member.id, inline=False)
        e.add_field(name="Дата регистрации:", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
        e.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                     icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        await ctx.send(embed=e)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {member}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="1", name="color", help="Сделать себе персональный цвет", brief="Цвет в формате HEX",
             usage="color #FF1493")
async def color(ctx, col: str = "#FF1493"):
    try:
        await ctx.message.delete(delay=1)
        c = re.findall(r"#[\w]{6}", col)
        if len(c) != 0:
            role = await ctx.message.guild.create_role(name=c[0], colour=int(c[0][1:], 16))
            pos = discord.utils.get(
                ctx.guild.roles, id=int(DB.mlpsbots.server.find_one({"_id": "Прочее"})["Позиция"])).position - 1
            await ctx.message.guild.edit_role_positions(positions={role: pos})
            await ctx.message.author.add_roles(discord.utils.get(ctx.message.author.guild.roles, id=int(role.id)))
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {col}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="1", name="achv", help="Показать достижения пользователя", brief="Упоминание пользователя",
             usage="achv @Принцесса Луна")
async def achv(ctx, member: discord.Member = None):
    try:
        await ctx.message.delete(delay=1)
        if not member:
            member = ctx.message.author
        a = DB.mlpsbots.achievements.find_one({"_id": member.id})
        if "achievements" not in a:
            await ctx.send(f"Сейчас у {member.mention} нет достижений...")
        else:
            i = 1
            files = []
            files2 = []
            files3 = []
            for x in a["achievements"]:
                if i <= 10:
                    files.append(discord.File(f"achievements/{x}.png"))
                if 11 <= i <= 20:
                    files2.append(discord.File(f"achievements/{x}.png"))
                if 21 <= i <= 30:
                    files3.append(discord.File(f"achievements/{x}.png"))
                i += 1
            await ctx.send(f"Текущие достижения {member.mention}:", files=files)
            if len(files2) != 0:
                await ctx.send(files=files2)
            if len(files3) != 0:
                await ctx.send(files=files3)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {member}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="2", name="text", help="Создать приватный текстовый канал", brief="Не применимо", usage="text")
async def text(ctx):
    try:
        await ctx.message.delete(delay=1)
        guild = ctx.message.guild
        mods = discord.utils.get(guild.roles, id=int(ROLES["Модераторы"]))
        overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False),
                      mods: discord.PermissionOverwrite(view_channel=True),
                      guild.get_member(ctx.author.id): discord.PermissionOverwrite(view_channel=True,
                                                                                   manage_channels=True,
                                                                                   manage_permissions=True,
                                                                                   manage_webhooks=True,
                                                                                   create_instant_invite=True,
                                                                                   send_messages=True,
                                                                                   embed_links=True,
                                                                                   attach_files=True,
                                                                                   add_reactions=True,
                                                                                   use_external_emojis=True,
                                                                                   mention_everyone=True,
                                                                                   manage_messages=True,
                                                                                   external_emojis=True,
                                                                                   read_messages=True,
                                                                                   read_message_history=True,
                                                                                   send_tts_messages=True,
                                                                                   use_slash_commands=True,
                                                                                   connect=True,
                                                                                   speak=True,
                                                                                   stream=True,
                                                                                   request_to_speak=True,
                                                                                   use_voice_activation=True,
                                                                                   priority_speaker=True,
                                                                                   mute_members=True,
                                                                                   deafen_members=True,
                                                                                   move_members=True)}
        await guild.create_text_channel(name=ctx.author.name, category=discord.utils.get(guild.categories, id=int(
            DB.mlpsbots.server.find_one({"_id": "Категории"})["Приватные каналы"])), overwrites=overwrites)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="2", name="voice",
             help="Создать приватный голосовой канал", brief="Не применимо", usage="voice")
async def voice(ctx):
    try:
        await ctx.message.delete(delay=1)
        guild = ctx.message.guild
        mods = discord.utils.get(guild.roles, id=int(ROLES["Модераторы"]))
        overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
                      mods: discord.PermissionOverwrite(view_channel=True),
                      guild.get_member(ctx.author.id): discord.PermissionOverwrite(view_channel=True,
                                                                                   manage_channels=True,
                                                                                   manage_permissions=True,
                                                                                   manage_webhooks=True,
                                                                                   create_instant_invite=True,
                                                                                   send_messages=True,
                                                                                   embed_links=True,
                                                                                   attach_files=True,
                                                                                   add_reactions=True,
                                                                                   use_external_emojis=True,
                                                                                   mention_everyone=True,
                                                                                   manage_messages=True,
                                                                                   external_emojis=True,
                                                                                   read_messages=True,
                                                                                   read_message_history=True,
                                                                                   send_tts_messages=True,
                                                                                   use_slash_commands=True,
                                                                                   connect=True,
                                                                                   speak=True,
                                                                                   stream=True,
                                                                                   request_to_speak=True,
                                                                                   use_voice_activation=True,
                                                                                   priority_speaker=True,
                                                                                   mute_members=True,
                                                                                   deafen_members=True,
                                                                                   move_members=True)}
        await guild.create_voice_channel(name=ctx.author.name, category=discord.utils.get(guild.categories, id=int(
            DB.mlpsbots.server.find_one({"_id": "Категории"})["Приватные каналы"])), overwrites=overwrites)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


# команды модераторов
@BOT.command(description="7", name="del", help="Удалить указанное количество сообщений",
             brief="Количество сообщений и упоминание пользователя", usage="del 10 @Принцесса Луна")
@discord.ext.commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 0, member: discord.Member = None):
    try:
        await ctx.message.delete(delay=1)
        msg = []
        if not member:
            await ctx.channel.purge(limit=amount)
        else:
            async for m in ctx.channel.history():
                if len(msg) == amount:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {amount} {member}\n"
                                 f"Канал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


# команды админов
@BOT.command(description="8", name="res", help="Полная перезагрузка бота", brief="Не применимо", usage="res")
@discord.ext.commands.has_permissions(administrator=True)
async def res(ctx):
    try:
        await ctx.message.delete(delay=1)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
        await asyncio.sleep(1)
        os.execl(sys.executable, "python", "mlpbots.py", *sys.argv[1:])
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


if __name__ == "__main__":
    try:
        btime = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H%M%S"))
        if 80000 <= btime < 200000:
            BOT.run("..")
        if 200000 <= btime < 240000 or 0 <= btime < 80000:
            BOT.run("..")
    except Exception:
        print(traceback.format_exc())
