import discord
from discord.ext import tasks
from datetime import datetime
import urllib.request
import json


token = 'OTY3NTg4NzczMDQ5Mjk4OTU1.GwP35_.sgClt4SBQHY8lslLvSKEsuz9wsLh9Huvcnn8KA'
messageId = MESSAEGE_ID
roleId = ROLE_ID
channel = CHANNEL_ID

client = discord.Client()

citycode = '080010'
resp = urllib.request.urlopen(f"https://weather.tsukumijima.net/api/forecast/city/{citycode}").read()
resp = json.loads(resp.decode('utf-8'))

# リアクション関係のメソッド
@client.event
async def on_raw_reaction_add(payload):
    # 指定したメッセージにリアクションがついたら。
    if payload.message_id == [messageId]:
        # サーバーの情報を取得
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        # サーバー情報からロール情報を取得
        role = guild.get_role([roleId])
        # 取得したロール情報をリアクションしたユーザに付与。IDがあっていればこれでリアクションロールはOK。
        await payload.member.add_roles(role)

# メッセージ関係のメソッド
@client.event
async def on_message(message):
    if message.content == "/ping":
        # Ping値を取得（変数名に用いている「raw」は「未加工」等の意味を持つ。
        # discord.pyの速度取得は秒単位で取得するため単位を変換する必要がある。）
        raw_ping = client.latency

        # Pingの単位はms（ミリ秒）を用いる。ミリ秒に変換する。
        ping = round(raw_ping * 1000)

        # pingの数値によってメッセージを変更する。
        # 判定基準はここを参照した。https://tinyurl.com/2orgg533
        if ping <= 15:
            judge = '非常に速いです。'
        elif ping <= 35:
            judge = '速いです。'
        elif ping <= 50:
            judge = '普通です。'
        elif ping <= 100:
            judge = '遅いです。'
        else:
            judge = '非常に遅いです。'

        # メッセージを出力する。pythonコマンド上だとbotが遅いのかPing値が大きい。
        await message.reply(f"Ping値は{ping}msです。\n{judge}")

    if message.content == "/weather":
        await message.reply(getWeather())

# 1分毎に時刻を取得する。4時なら発信。
@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')
    if now == '04:00':
        channel.send(getWeather())

# 使いみちが複数ある場合、共通の処理は関数で実装しておくと良い。
def getWeather():
    msg = "__【お天気情報：**" + resp["location"]["city"] + "**】__\n"
    for f in resp["forecasts"]:
        msg += f["dateLabel"] + "：**" + f["telop"] + "**\n"
        msg += "```" + resp["description"]["bodyText"] + "```"

    return msg


loop.start()
client.run(token)
