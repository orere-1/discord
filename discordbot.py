import discord
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()


# リアクション関係のメソッド
@client.event
async def on_raw_reaction_add(payload):

    # 指定したメッセージにリアクションがついたら。
    if payload.message_id == 990415099468603462:
        # サーバーの情報を取得
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        # サーバー情報からロール情報を取得
        role = guild.get_role(990414877921263637)
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

client.run(token)
