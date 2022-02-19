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
DB = pymongo.MongoClient("")

JWR = 496139824500178964
IDS = 868148805722337320
IDL = 868150460735971328

RAS = DB.mlpsbots.roles.find_one({"_id": "Расы"})
MIN = DB.mlpsbots.roles.find_one({"_id": "Министерства"})


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


async def errors(name, value):
    try:
        await BOT.get_user(JWR).send(embed=discord.Embed(
            title="Ошибка!", color=0xFF0000).add_field(name=name, value=value))
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
            rules = await BOT.get_channel(int(DB.mlpsbots.posts.find_one({"_id": "Rules"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Rules"})["post"]))
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
        rulesid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Rules"})["channel"])).send(
            embed=e1, components=[[discord_components.Button(label="Согласен!", style=3),
                                   discord_components.Button(label="Не согласен!", style=4)]])
        DB.mlpsbots.posts.update_one({"_id": "Rules"}, {"$set": {"post": int(rulesid.id)}})
    except Exception:
        await errors("Пост Правила:", traceback.format_exc())
    try:
        try:
            roles = await BOT.get_channel(int(DB.mlpsbots.posts.find_one({"_id": "Roles"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Roles"})["post"]))
            await roles.delete()
        except Exception:
            print(traceback.format_exc())
        e2 = discord.Embed(title="На нашем сервере есть 4 основные роли:", color=0xFFFF00,
                           description="<@&798875106868854804> - пони, которые непосредственно управляют сервером."
                                       "\n\n<@&798877123413540876> - пони, которые следят за порядком на сервере."
                                       "\n\n<@&798878290437603369> - основной табун. Добрые и культурные пони сервера."
                                       "\n\n<@&907438760663322634> - те, кто несогласны с правилами, только наблюдают."
                                       "\n\n<a:a131:912433126716866653> Роли <@&798878290437603369> и "
                                       "<@&907438760663322634> выдают автоматически <@&799037336599134208>!"
                                       "\n\n<a:a110:907931053325418506> Также есть ещё дополнительная роль "
                                       "<@&798880441390202891>:\nОна открывает доступ к закрытой категории, где не "
                                       "действуют абсолютно никакие правила и модерация. Истинный мир хаоса! Там всем "
                                       "управляет только Дискорд, и даже <@&799037336599134208> бессильны... Чтобы "
                                       "получить эту роль, нажмите на соответствующую кнопку под этим сообщением.")
        e2.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/915449826731257956/Cheer.png")
        e2.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        rolesid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Roles"})["channel"])).send(
            embed=e2, components=[[discord_components.Button(label="18+", style=2)]])
        DB.mlpsbots.posts.update_one({"_id": "Roles"}, {"$set": {"post": int(rolesid.id)}})
    except Exception:
        await errors("Пост Роли:", traceback.format_exc())
    try:
        try:
            rases = await BOT.get_channel(int(DB.mlpsbots.posts.find_one({"_id": "Rases"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Rases"})["post"]))
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
        rasesid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Rases"})["channel"])).send(
            embed=e3, components=[[
                discord_components.Button(emoji=BOT.get_emoji(919732726888796220), style=2, id="Аликорны"),
                discord_components.Button(emoji=BOT.get_emoji(917553790016688138), style=2, id="Единороги"),
                discord_components.Button(emoji=BOT.get_emoji(917553789798580264), style=2, id="Пегасы"),
                discord_components.Button(emoji=BOT.get_emoji(917553790083801188), style=2, id="Земные_пони"),
                discord_components.Button(emoji=BOT.get_emoji(917553790083825675), style=2, id="Кирины")],
                [discord_components.Button(emoji=BOT.get_emoji(917553789823754331), style=2, id="Оборотни"),
                 discord_components.Button(emoji=BOT.get_emoji(917553790259957800), style=2, id="Гиппогрифы"),
                 discord_components.Button(emoji=BOT.get_emoji(907931049579917342), style=2, id="Грифоны"),
                 discord_components.Button(emoji=BOT.get_emoji(912433127027249242), style=2, id="Кристальные_пони"),
                 discord_components.Button(emoji=BOT.get_emoji(907931053757456444), style=2, id="Зебры")]])
        DB.mlpsbots.posts.update_one({"_id": "Rases"}, {"$set": {"post": int(rasesid.id)}})
    except Exception:
        await errors("Пост Расы:", traceback.format_exc())
    try:
        try:
            minis = await BOT.get_channel(int(DB.mlpsbots.posts.find_one({"_id": "Minis"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Minis"})["post"]))
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
        minisid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Minis"})["channel"])).send(
            embed=e4, components=[[
                discord_components.Button(emoji=BOT.get_emoji(917553790100590622), style=2, id="Стиля"),
                discord_components.Button(emoji=BOT.get_emoji(917553790012510279), style=2, id="Мира"),
                discord_components.Button(emoji=BOT.get_emoji(917553790427742298), style=2, id="Морали")],
                [discord_components.Button(emoji=BOT.get_emoji(917553790079619126), style=2, id="Технологий"),
                 discord_components.Button(emoji=BOT.get_emoji(917553790016688129), style=2, id="Наук"),
                 discord_components.Button(emoji=BOT.get_emoji(917553790159298570), style=2, id="Крутости")]])
        DB.mlpsbots.posts.update_one({"_id": "Minis"}, {"$set": {"post": int(minisid.id)}})
    except Exception:
        await errors("Пост Министества:", traceback.format_exc())
    try:
        try:
            forum = await BOT.get_channel(int(DB.mlpsbots.posts.find_one({"_id": "Forums"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Forums"})["post"]))
            await forum.delete()
        except Exception:
            print(traceback.format_exc())
        e5 = discord.Embed(title="Наши темы на форуме:", color=0x00FFFF)
        e5.add_field(name="MY LITTLE PONY: Магия Принцесс:", value="https://4pda.to/forum/index.php?showtopic=396777")
        e5.add_field(name="Bronies 4PDA:", value="https://4pda.to/forum/index.php?showtopic=403239")
        e5.set_thumbnail(url="https://ds-assets.cdn.devapps.ru/EoAVz2z2w96Lx0PqpnsAuOJVFUbPz1uWLqlwNgtOG92kP.png")
        e5.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        forumid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Forums"})["channel"])).send(
            embed=e5, components=[[discord_components.Button(label="MY LITTLE PONY: Магия Принцесс", style=5,
                                                             url="https://4pda.to/forum/index.php?showtopic=396777"),
                                   discord_components.Button(label="Bronies 4PDA", style=5,
                                                             url="https://4pda.to/forum/index.php?showtopic=403239")]])
        DB.mlpsbots.posts.update_one({"_id": "Forums"}, {"$set": {"post": int(forumid.id)}})
    except Exception:
        await errors("Пост Наши темы на форуме:", traceback.format_exc())
    try:
        try:
            discords = await BOT.get_channel(
                int(DB.mlpsbots.posts.find_one({"_id": "Discords"})["channel"])).fetch_message(
                int(DB.mlpsbots.posts.find_one({"_id": "Discords"})["post"]))
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
        e6.set_thumbnail(url="https://cdn.discordapp.com/attachments/915008263253266472/929399822895710228/cran.png")
        e6.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                      icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        discordsid = await BOT.get_channel(
            int(DB.mlpsbots.posts.find_one({"_id": "Discords"})["channel"])).send(
            embed=e6, components=[[
                discord_components.Button(label="My Little Pony Gameloft Вики", url="https://discord.gg/sJAwM2yS98",
                                          style=5),
                discord_components.Button(label="Дружба – это Чудо Вики", url="https://discord.gg/79TZp5q",
                                          style=5)], [
                discord_components.Button(label="Everhoof Radio", url="https://discord.gg/YV9HhHRd4M",
                                          style=5),
                discord_components.Button(label="Anon2Anon", url="https://discord.gg/trxVtrj",
                                          style=5),
                discord_components.Button(label="Fallout Equestria: REMAINS", url="https://discord.gg/qWYAbsp",
                                          style=5)], [
                discord_components.Button(label="Legends of Equestria", url="https://discord.gg/uPvn8Xr",
                                          style=5)]])
        DB.mlpsbots.posts.update_one({"_id": "Discords"}, {"$set": {"post": int(discordsid.id)}})
    except Exception:
        await errors("Пост Наши друзья в Дискорде:", traceback.format_exc())
    try:
        if BOT.user.id == IDS:
            await messages(BOT.user, "Снова \"Смотрит за Эквестрией...\"")
        if BOT.user.id == IDL:
            await messages(BOT.user, "Снова \"Слушает тишину ночи...\"")
    except Exception:
        await errors("Сообщение готовности:", traceback.format_exc())


@BOT.event
async def on_message(message):
    try:
        await BOT.process_commands(message)
    except Exception:
        await errors("process_commands:", traceback.format_exc())
    try:
        wor = "пон|млп|няш|еле|эле|гар|мон|дев|кве|рог|пег|рыл|пин|пай|рит|рад|дэш|даш|иск|тва|ппл|дже|фла|шай|лун|сел"
        if message.author.id != IDS and message.author.id != IDL:
            if len(re.findall(rf"{wor}", message.content.lower())) > 0:
                await message.channel.send(
                    str(DB.mlpsbots.quotes.find_one({"_id": f"{random.randint(1, 91)}"})["quote"]))
    except Exception:
        await errors("Рандомные Фразы:", traceback.format_exc())


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
async def on_member_join(member):
    try:
        e = discord.Embed(title="В наш клуб присоединилась милая поняшка!", color=0xBA55D3,
                          description=f"Поприветствуем: {member.mention}!")
        e.set_thumbnail(url=member.avatar_url)
        e.set_footer(text="Все права принадлежат пони! Весь мир принадлежит пони!",
                     icon_url="https://cdn.discordapp.com/attachments/915008263253266472/915449197388525618/NoDRM.png")
        await BOT.get_channel(int(DB.mlpsbots.channels.find_one({"_id": "Болталка"})["channel"])).send(embed=e)
    except Exception:
        await errors("Новый участник:", traceback.format_exc())


@BOT.event
async def on_member_update(before, after):
    try:
        if before.id != JWR and after.id != JWR:
            rsb = []
            rsa = []
            for role in before.roles:
                rsb.append(role.id)
            for role in after.roles:
                rsa.append(role.id)
            if len(rsa) > len(rsb):
                for x in rsb:
                    rsa.remove(x)
                if re.findall(str(rsa[0]), str(RAS)) or re.findall(str(rsa[0]), str(MIN)):
                    if re.findall(str(rsa[0]), str(RAS)):
                        for key in RAS:
                            if RAS[key] == rsa[0] or RAS[key] == "Расы":
                                continue
                            await after.remove_roles(discord.utils.get(after.guild.roles, id=int(RAS[key])))
                    if re.findall(str(rsa[0]), str(MIN)):
                        for key in MIN:
                            if MIN[key] == rsa[0] or MIN[key] == "Министерства":
                                continue
                            await after.remove_roles(discord.utils.get(after.guild.roles, id=int(MIN[key])))
    except:
        await errors("Удаление ролей:", traceback.format_exc())


@BOT.event
async def on_button_click(interaction):
    try:
        if interaction.component.label == "Согласен!":
            await interaction.send(
                f"Поздравляем! Вам выдана роль <@&{int(DB.mlpsbots.roles.find_one({'_id': 'Пользователи'})['role'])}>")
            role = discord.utils.get(interaction.user.guild.roles,
                                     id=int(DB.mlpsbots.roles.find_one({'_id': 'Пользователи'})['role']))
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(discord.utils.get(interaction.user.guild.roles, id=int(
                DB.mlpsbots.roles.find_one({'_id': 'Читатели'})['role'])))
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Кнопка Согласен:", traceback.format_exc())
    try:
        if interaction.component.label == "Не согласен!":
            await interaction.send(
                f"Поздравляем! Вам выдана роль <@&{int(DB.mlpsbots.roles.find_one({'_id': 'Читатели'})['role'])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(
                DB.mlpsbots.roles.find_one({'_id': 'Читатели'})['role']))
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(discord.utils.get(interaction.user.guild.roles, id=int(
                DB.mlpsbots.roles.find_one({'_id': 'Пользователи'})['role'])))
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Кнопка Не согласен:", traceback.format_exc())
    try:
        if interaction.component.label == "18+":
            await interaction.send(
                f"Поздравляем! Вам выдана роль <@&{int(DB.mlpsbots.roles.find_one({'_id': '18+'})['role'])}>")
            role = discord.utils.get(interaction.user.guild.roles,
                                     id=int(DB.mlpsbots.roles.find_one({'_id': '18+'})['role']))
            await interaction.user.add_roles(role)
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Кнопка 18+:", traceback.format_exc())
    try:
        if re.findall(str(interaction.component.id), str(RAS)):
            await interaction.send(
                f"Поздравляем! Вам выдана роль "
                f"<@&{int(DB.mlpsbots.roles.find_one({'_id': 'Расы'})[interaction.component.id])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(
                DB.mlpsbots.roles.find_one({"_id": "Расы"})[interaction.component.id]))
            await interaction.user.add_roles(role)
            await alerts(interaction.user, f"Выдана роль: {role}")
    except Exception:
        await errors("Выдача Рас:", traceback.format_exc())
    try:
        if re.findall(str(interaction.component.id), str(MIN)):
            await interaction.send(
                f"Поздравляем! Вам выдана роль "
                f"<@&{int(DB.mlpsbots.roles.find_one({'_id': 'Министерства'})[interaction.component.id])}>")
            role = discord.utils.get(interaction.user.guild.roles, id=int(
                DB.mlpsbots.roles.find_one({"_id": "Министерства"})[interaction.component.id]))
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
                ctx.guild.roles, id=int(DB.mlpsbots.roles.find_one({"_id": "Позиция"})["role"])).position - 1
            await ctx.message.guild.edit_role_positions(positions={role: pos})
            await ctx.message.author.add_roles(discord.utils.get(ctx.message.author.guild.roles, id=int(role.id)))
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name} {col}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="2", name="text", help="Создать приватный текстовый канал", brief="Не применимо", usage="text")
async def text(ctx):
    try:
        await ctx.message.delete(delay=1)
        guild = ctx.message.guild
        mods = discord.utils.get(guild.roles, id=int(DB.mlpsbots.roles.find_one({"_id": "Модераторы"})["role"]))
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
            DB.mlpsbots.categories.find_one({"_id": "Приватные каналы"})["category"])), overwrites=overwrites)
        await alerts(ctx.author, f"Использовал команду: {ctx.command.name}\nКанал: {ctx.message.channel}")
    except Exception:
        await errors(f"Команда {ctx.command.name}:", traceback.format_exc())


@BOT.command(description="2", name="voice",
             help="Создать приватный голосовой канал", brief="Не применимо", usage="voice")
async def voice(ctx):
    try:
        await ctx.message.delete(delay=1)
        guild = ctx.message.guild
        mods = discord.utils.get(guild.roles, id=int(DB.mlpsbots.roles.find_one({"_id": "Модераторы"})["role"]))
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
            DB.mlpsbots.categories.find_one({"_id": "Приватные каналы"})["category"])), overwrites=overwrites)
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
            BOT.run("")
        if 200000 <= btime < 270000 or 0 <= btime < 80000:
            BOT.run("")
    except Exception:
        print(traceback.format_exc())
