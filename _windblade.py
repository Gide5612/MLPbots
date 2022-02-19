import asyncio
import configparser
import re

import discord
import discord_components
from discord.ext import commands

bot = discord.ext.commands.Bot(command_prefix=discord.ext.commands.when_mentioned_or("!"),
                               intents=discord.Intents.all())


@bot.event
async def on_ready():
    discord_components.DiscordComponents(bot)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Transformers"))
    print('Бот загружен!')
    print('Залогинен под:', bot.user.name)
    print('ID бота:', bot.user.id)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.event
async def on_button_click(interaction):
    hel = discord.utils.get(interaction.user.guild.roles, id=930254419109503037)
    dmg = discord.utils.get(interaction.user.guild.roles, id=930254531726548993)
    tnk = discord.utils.get(interaction.user.guild.roles, id=930254585682092122)
    if interaction.component.label == 'Хилер':
        cfg1 = configparser.ConfigParser()
        cfg1.read("config.ini", encoding="utf8")
        if not re.findall(f"{str(hel)}", str(interaction.user.roles)):
            await interaction.send('Вы выбрали роль Хилера')
            await interaction.user.add_roles(hel)
            await interaction.user.remove_roles(dmg)
            await interaction.user.remove_roles(tnk)
            cfg1.set("HEALER", f"{interaction.user.id}", f"{interaction.user.name}")
            cfg1.remove_option("DPS", f"{interaction.user.id}")
            cfg1.remove_option("TANK", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg1.write(configfile)
        if re.findall(f"{str(hel)}", str(interaction.user.roles)):
            await interaction.send('Вы убрали роль Хилера')
            await interaction.user.remove_roles(hel)
            cfg1.remove_option("HEALER", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg1.write(configfile)
    if interaction.component.label == 'Дамагер':
        cfg2 = configparser.ConfigParser()
        cfg2.read("config.ini", encoding="utf8")
        if not re.findall(f"{str(dmg)}", str(interaction.user.roles)):
            await interaction.send('Вы выбрали роль Дамагера')
            await interaction.user.add_roles(dmg)
            await interaction.user.remove_roles(hel)
            await interaction.user.remove_roles(tnk)
            cfg2.set("DPS", f"{interaction.user.id}", f"{interaction.user.name}")
            cfg2.remove_option("HEALER", f"{interaction.user.id}")
            cfg2.remove_option("TANK", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg2.write(configfile)
        if re.findall(f"{str(dmg)}", str(interaction.user.roles)):
            await interaction.send('Вы убрали роль Дамагера')
            await interaction.user.remove_roles(dmg)
            cfg2.remove_option("DPS", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg2.write(configfile)
    if interaction.component.label == 'Танк':
        cfg3 = configparser.ConfigParser()
        cfg3.read("config.ini", encoding="utf8")
        if not re.findall(f"{str(tnk)}", str(interaction.user.roles)):
            await interaction.send('Вы выбрали роль Танка')
            await interaction.user.add_roles(tnk)
            await interaction.user.remove_roles(dmg)
            await interaction.user.remove_roles(hel)
            cfg3.set("TANK", f"{interaction.user.id}", f"{interaction.user.name}")
            cfg3.remove_option("DPS", f"{interaction.user.id}")
            cfg3.remove_option("HEALER", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg3.write(configfile)
        if re.findall(f"{str(tnk)}", str(interaction.user.roles)):
            await interaction.send('Вы убрали роль Танка')
            await interaction.user.remove_roles(tnk)
            cfg3.remove_option("TANK", f"{interaction.user.id}")
            with open("config.ini", "w", encoding="utf8") as configfile:
                cfg3.write(configfile)


@bot.command()
async def event(ctx):
    await ctx.message.delete(delay=1)
    time = int(235959)
    cfg4 = configparser.ConfigParser()
    cfg4.read("config.ini", encoding="utf8")
    hel = []
    dps = []
    tnk = []
    for x in cfg4.options("HEALER"):
        member = discord.utils.get(bot.users, id=int(x))
        hel.append(member.mention)
    for y in cfg4.options("DPS"):
        member = discord.utils.get(bot.users, id=int(y))
        dps.append(member.mention)
    for z in cfg4.options("TANK"):
        member = discord.utils.get(bot.users, id=int(z))
        tnk.append(member.mention)
    embed = discord.Embed(title='Всем привет!', color=0xFF0000, description="Запись на гильд ивенты 16 hm ops")
    embed.add_field(name=f"Время: {str(time)[:2]}:{str(time)[2:4]}:{str(time)[4:]}",
                    value="Цена: 100000$", inline=False)
    if len(hel) != 0:
        embed.add_field(name='Хилер:', value=" ".join([x for x in hel]), inline=False)
    if len(dps) != 0:
        embed.add_field(name='Дамагер:', value=" ".join([x for x in dps]), inline=False)
    if len(tnk) != 0:
        embed.add_field(name='Танк:', value=" ".join([x for x in tnk]), inline=False)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/915008263253266472/929495052693164083/'
                            '1641679284449.png?width=518&height=676')
    embed.set_footer(text='dd h t ', icon_url="https://media.discordapp.net/attachments/915008263253266472/"
                                              "929493149628375040/1641678827378.jpg")
    rec = await ctx.send(embed=embed, components=[[discord_components.Button(label='Хилер', style=3),
                                                   discord_components.Button(label='Дамагер', style=4),
                                                   discord_components.Button(label='Танк', style=1)]])
    while True:
        if int(str(time)[4:]) == 99:
            time -= 40
            continue
        cfg6 = configparser.ConfigParser()
        cfg6.read("config.ini", encoding="utf8")
        hel = []
        dps = []
        tnk = []
        for x in cfg6.options("HEALER"):
            member = discord.utils.get(bot.users, id=int(x))
            hel.append(member.mention)
        for y in cfg6.options("DPS"):
            member = discord.utils.get(bot.users, id=int(y))
            dps.append(member.mention)
        for z in cfg6.options("TANK"):
            member = discord.utils.get(bot.users, id=int(z))
            tnk.append(member.mention)
        embed = discord.Embed(title='Всем привет!', color=0xFF0000, description="Запись на гильд ивенты 16 hm ops")
        embed.add_field(name=f"Время: {str(time)[:2]}:{str(time)[2:4]}:{str(time)[4:]}",
                        value="Цена: 100000$", inline=False)
        if len(hel) != 0:
            embed.add_field(name='Хилер:', value=" ".join([x for x in hel]), inline=False)
        if len(dps) != 0:
            embed.add_field(name='Дамагер:', value=" ".join([x for x in dps]), inline=False)
        if len(tnk) != 0:
            embed.add_field(name='Танк:', value=" ".join([x for x in tnk]), inline=False)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/915008263253266472/929495052693164083/'
                                '1641679284449.png?width=518&height=676')
        embed.set_footer(text='dd h t ', icon_url="https://media.discordapp.net/attachments/915008263253266472/"
                                                  "929493149628375040/1641678827378.jpg")
        msg = await bot.get_channel(int(ctx.channel.id)).fetch_message(rec.id)
        await msg.edit(embed=embed, components=[[discord_components.Button(label='Хилер', style=3),
                                                 discord_components.Button(label='Дамагер', style=4),
                                                 discord_components.Button(label='Танк', style=1)]])
        time -= 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    bot.run("")
