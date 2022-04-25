import sys
from os import execl
from re import findall
from traceback import format_exc

from discord import Embed, utils
from discord.ext.commands import Cog
from discord.ext.tasks import loop
from discord_components import Button, ButtonStyle

from mlpbots import DB, JWR, FOOTERNANE, FOOTERURL

CHANNELS = DB.server.posts.find_one({"_id": "Каналы"})
POSTS = DB.server.posts.find_one({"_id": "Посты"})
ROLES = DB.server.posts.find_one({"_id": "Роли"})
RASES = DB.server.posts.find_one({"_id": "Расы"})
MINIS = DB.server.posts.find_one({"_id": "Министерства"})


class Posts(Cog):
    def __init__(self, bot):
        self.BOT = bot
        self.posts.start()

    def cog_unload(self):
        self.posts.cancel()

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

    @loop(count=1)
    async def posts(self):
        try:
            try:
                rules = await self.BOT.get_channel(
                    int(CHANNELS["Добро пожаловать"])).fetch_message(int(POSTS["Правила"]))
                await rules.delete()
            except Exception:
                pass
            e1 = Embed(title="Приветствуем тебя милая поняшка в нашем клубе!", color=0x008000,
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
            e1.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/915008263253266472/915419331804954634/PPWHY.png")
            e1.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            rulesid = await self.BOT.get_channel(int(CHANNELS["Добро пожаловать"])).send(embed=e1, components=[[
                Button(label="Согласен!", style=ButtonStyle.green),
                Button(label="Не согласен!", style=ButtonStyle.red)]])
            DB.server.posts.update_one({"_id": "Посты"}, {"$set": {"Правила": int(rulesid.id)}})
        except Exception:
            await self.errors("Пост Правила:", format_exc())
        try:
            try:
                roles = await self.BOT.get_channel(int(CHANNELS["Роли сервера"])).fetch_message(int(POSTS["Роли"]))
                await roles.delete()
            except Exception:
                pass
            e2 = Embed(title="На нашем сервере есть 3 основные роли:", color=0xFFFF00,
                       description="<@&798875106868854804> - пони, которые непосредственно управляют сервером."
                                   "\n\n<@&798878290437603369> - основной табун. Добрые и культурные пони серв"
                                   "ера.\n\n<@&907438760663322634> - те, кто несогласны с правилами, только на"
                                   "блюдают.\n\n<a:a131:912433126716866653> Роли <@&798878290437603369> и <@&9"
                                   "07438760663322634> выдают автоматически <@&799037336599134208>!")
            e2.add_field(name="Также есть ещё дополнительная роль:",
                         value="Она открывает доступ к закрытой категории, где не действуют абсолютно никакие правила и"
                               " модерация. Истинный мир хаоса! Там всем управляет только Дискорд, и даже <@&7990373365"
                               "99134208> бессильны... Чтобы получить эту роль, нажмите на соответствующую кнопку под э"
                               "тим сообщением.")
            e2.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/915008263253266472/915449826731257956/Cheer.png")
            e2.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            rolesid = await self.BOT.get_channel(
                int(CHANNELS["Роли сервера"])).send(embed=e2, components=[[Button(label="18+")]])
            DB.server.posts.update_one({"_id": "Посты"}, {"$set": {"Роли": int(rolesid.id)}})
        except Exception:
            await self.errors("Пост Роли:", format_exc())
        try:
            try:
                rases = await self.BOT.get_channel(int(CHANNELS["Роли сервера"])).fetch_message(int(POSTS["Расы"]))
                await rases.delete()
            except Exception:
                pass
            e3 = Embed(title="А еще у нас есть расы:", color=0xFFA500,
                       description=f"<a:a149:919732726888796220> <@&{RASES['Аликорны']}>\n\n"
                                   f"<a:a147:917553790016688138> <@&{RASES['Единороги']}>\n\n"
                                   f"<a:a143:917553789798580264> <@&{RASES['Пегасы']}>\n\n"
                                   f"<a:a140:917553790083801188> <@&{RASES['Земные пони']}>\n\n"
                                   f"<a:a139:917553790083825675> <@&{RASES['Кирины']}>\n\n"
                                   f"<a:a138:917553789823754331> <@&{RASES['Оборотни']}>\n\n"
                                   f"<a:a137:917553790259957800> <@&{RASES['Гиппогрифы']}>\n\n"
                                   f"<a:a107:907931049579917342> <@&{RASES['Грифоны']}>\n\n"
                                   f"<a:a126:912433127027249242> <@&{RASES['Кристальные пони']}>\n\n"
                                   f"<a:a111:907931053757456444> <@&{RASES['Зебры']}>\n\n"
                                   f"Чтобы выбрать себе расу нажмите на соответствующую ей кнопку под этим "
                                   f"сообщением. Одновременно себе можно выбрать только одну расу!")
            e3.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/915008263253266472/917800054042009630/chars.png")
            e3.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            rasesid = await self.BOT.get_channel(int(CHANNELS["Роли сервера"])).send(embed=e3, components=[[
                Button(emoji=self.BOT.get_emoji(919732726888796220), id="Аликорны"),
                Button(emoji=self.BOT.get_emoji(917553790016688138), id="Единороги"),
                Button(emoji=self.BOT.get_emoji(917553789798580264), id="Пегасы"),
                Button(emoji=self.BOT.get_emoji(917553790083801188), id="Земные пони"),
                Button(emoji=self.BOT.get_emoji(917553790083825675), id="Кирины")],
                [Button(emoji=self.BOT.get_emoji(917553789823754331), id="Оборотни"),
                 Button(emoji=self.BOT.get_emoji(917553790259957800), id="Гиппогрифы"),
                 Button(emoji=self.BOT.get_emoji(907931049579917342), id="Грифоны"),
                 Button(emoji=self.BOT.get_emoji(912433127027249242), id="Кристальные пони"),
                 Button(emoji=self.BOT.get_emoji(907931053757456444), id="Зебры")]])
            DB.server.posts.update_one({"_id": "Посты"}, {"$set": {"Расы": int(rasesid.id)}})
        except Exception:
            await self.errors("Пост Расы:", format_exc())
        try:
            try:
                minis = await self.BOT.get_channel(
                    int(CHANNELS["Роли сервера"])).fetch_message(int(POSTS["Министерства"]))
                await minis.delete()
            except Exception:
                pass
            e4 = Embed(title="И министерства:", color=0xFF0000,
                       description=f"<a:a149:917553790100590622> <@&{MINIS['Стиля']}>\n\n"
                                   f"<a:a149:917553790012510279> <@&{MINIS['Мира']}>\n\n"
                                   f"<a:a149:917553790427742298> <@&{MINIS['Морали']}>\n\n"
                                   f"<a:a149:917553790079619126> <@&{MINIS['Технологий']}>\n\n"
                                   f"<a:a149:917553790016688129> <@&{MINIS['Наук']}>\n\n"
                                   f"<a:a149:917553790159298570> <@&{MINIS['Крутости']}>\n\n"
                                   f"Чтобы присоединиться к министерству нажмите на соответствующую ему кнопку "
                                   f"под этим сообщением. Одновременно присоединится можно только к одному "
                                   f"министерству!")
            e4.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/915008263253266472/917587318930550794/mine6.png")
            e4.set_footer(text=FOOTERNANE, icon_url=FOOTERURL)
            minisid = await self.BOT.get_channel(int(CHANNELS["Роли сервера"])).send(embed=e4, components=[[
                Button(emoji=self.BOT.get_emoji(917553790100590622), id="Стиля"),
                Button(emoji=self.BOT.get_emoji(917553790012510279), id="Мира"),
                Button(emoji=self.BOT.get_emoji(917553790427742298), id="Морали")],
                [Button(emoji=self.BOT.get_emoji(917553790079619126), id="Технологий"),
                 Button(emoji=self.BOT.get_emoji(917553790016688129), id="Наук"),
                 Button(emoji=self.BOT.get_emoji(917553790159298570), id="Крутости")]])
            DB.server.posts.update_one({"_id": "Посты"}, {"$set": {"Министерства": int(minisid.id)}})
        except Exception:
            await self.errors("Пост Министества:", format_exc())

    @Cog.listener()
    async def on_member_update(self, before, after):
        try:
            rsb = []
            rsa = []
            for role in before.roles:
                rsb.append(role.id)
            for role in after.roles:
                rsa.append(role.id)
            if len(rsa) > len(rsb):
                for x in rsb:
                    rsa.remove(x)
                if findall(str(rsa[0]), str(RASES)) or findall(str(rsa[0]), str(MINIS)):
                    if findall(str(rsa[0]), str(RASES)):
                        for key in RASES:
                            if RASES[key] == rsa[0] or RASES[key] == "Расы":
                                continue
                            await after.remove_roles(utils.get(after.guild.roles, id=int(RASES[key])))
                    if findall(str(rsa[0]), str(MINIS)):
                        for key in MINIS:
                            if MINIS[key] == rsa[0] or MINIS[key] == "Министерства":
                                continue
                            await after.remove_roles(utils.get(after.guild.roles, id=int(MINIS[key])))
        except Exception:
            await self.errors("Удаление ролей:", format_exc())

    @Cog.listener()
    async def on_button_click(self, interaction):
        try:
            if interaction.component.label == "Согласен!":
                await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['Пользователи'])}>")
                role = utils.get(interaction.user.guild.roles, id=int(ROLES["Пользователи"]))
                await interaction.user.add_roles(role)
                await interaction.user.remove_roles(
                    utils.get(interaction.user.guild.roles, id=int(ROLES["Читатели"])))
                await self.alerts(interaction.user, f"Выдана роль: {role}")
        except Exception:
            await self.errors("Кнопка Согласен:", format_exc())
        try:
            if interaction.component.label == "Не согласен!":
                await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['Читатели'])}>")
                role = utils.get(interaction.user.guild.roles, id=int(ROLES['Читатели']))
                await interaction.user.add_roles(role)
                await interaction.user.remove_roles(
                    utils.get(interaction.user.guild.roles, id=int(ROLES['Пользователи'])))
                await self.alerts(interaction.user, f"Выдана роль: {role}")
        except Exception:
            await self.errors("Кнопка Не согласен:", format_exc())
        try:
            if interaction.component.label == "18+":
                role = utils.get(interaction.user.guild.roles, id=int(ROLES['18+']))
                if utils.get(interaction.user.roles, id=int(ROLES['18+'])) is None:
                    await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(ROLES['18+'])}>")
                    await interaction.user.add_roles(role)
                    await self.alerts(interaction.user, f"Выдана роль: {role}")
                else:
                    await interaction.send(f"Поздравляем! Вам убрана роль <@&{int(ROLES['18+'])}>")
                    await interaction.user.remove_roles(role)
                    await self.alerts(interaction.user, f"Удалена роль: {role}")
        except Exception:
            await self.errors("Кнопка 18+:", format_exc())
        try:
            if findall(str(interaction.component.id), str(RASES)):
                await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(RASES[interaction.component.id])}>")
                role = utils.get(interaction.user.guild.roles, id=int(RASES[interaction.component.id]))
                await interaction.user.add_roles(role)
                await self.alerts(interaction.user, f"Выдана роль: {role}")
        except Exception:
            await self.errors("Выдача Рас:", format_exc())
        try:
            if findall(str(interaction.component.id), str(MINIS)):
                await interaction.send(f"Поздравляем! Вам выдана роль <@&{int(MINIS[interaction.component.id])}>")
                role = utils.get(interaction.user.guild.roles, id=int(MINIS[interaction.component.id]))
                await interaction.user.add_roles(role)
                await self.alerts(interaction.user, f"Выдана роль: {role}")
        except Exception:
            await self.errors("Выдача Министерств:", format_exc())


def setup(bot):
    bot.add_cog(Posts(bot))
