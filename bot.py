# (c) @xditya
# This file is a part of https://github.com/xditya/BotStatus

import pytz
import logging
import asyncio
from datetime import datetime as dt
from telethon.tl.functions.messages import GetHistoryRequest
from decouple import config
from telethon.sessions import StringSession
from telethon import TelegramClient

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

try:
    appid = config("APP_ID")
    apihash = config("API_HASH")
    session = config("SESSION", default=None)
    chnl_id = config("CHANNEL_ID", cast=int)
    msg_id = config("MESSAGE_ID", cast=int)
    botlist = config("BOTS")
    bots = botlist.split()
    session_name = str(session)
    user_bot = TelegramClient(StringSession(session_name), appid, apihash)
    print("Started")
except Exception as e:
    print(f"ERROR\n{str(e)}")

async def BotzHub():
    async with user_bot:
        while True:
            print("[INFO] starting to check uptime..")
            await user_bot.edit_message(int(chnl_id), msg_id, "**@HxBots Bots Stats.**\n\n`Performing a periodic check...`")
            c = 0
            edit_text = "**@HxBots Bots Stats.**\n\n💗 𝐎𝐮𝐫 𝐀𝐥𝐥 𝐁𝐨𝐭𝐬 𝐋𝐢𝐬𝐭 𝐚𝐧𝐝 𝐋𝐢𝐯𝐞 𝐒𝐭𝐚𝐭𝐮𝐬 💖\n\n💡__𝘉𝘰𝘵 𝘜𝘱𝘥𝘢𝘵𝘦𝘥 𝘌𝘷𝘦𝘳𝘺 15 𝘔𝘪𝘯𝘶𝘵𝘦𝘴__\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = await user_bot.send_message(bot, "/start")
                await asyncio.sleep(10)

                history = await user_bot(GetHistoryRequest(
                    peer=bot,
                    offset_id=0,
                    offset_date=None,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                msg = history.messages[0].id
                if snt.id == msg:
                    print(f"@{bot} is down.")
                    edit_text += f"🤖 Bot: @{bot} \n🔰 Status: ❌\n\n"
                elif snt.id + 1 == msg:
                    edit_text += f"🤖 Bot: @{bot} \n🔰 Status: ✅\n\n"
                await user_bot.send_read_acknowledge(bot)
                c += 1
                await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            k = pytz.timezone("Asia/Kolkata")
            month = dt.now(k).strftime("%B")
            day = dt.now(k).strftime("%d")
            year =  dt.now(k).strftime("%Y")
            t = dt.now(k).strftime("%H:%M:%S")
            edit_text +=f"\n**Last Checked & Updated:** \n`{t} - {day} {month} {year} [IST]`\n\n__Bots Status Are Auto-updated Every 1 hour__"
            await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            print(f"Checks since last restart - {c}")
            print("Sleeping for 1 hours.")
            await asyncio.sleep(1 * 60 * 60)

user_bot.loop.run_until_complete(BotzHub())
