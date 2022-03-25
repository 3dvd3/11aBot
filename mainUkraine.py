from httpx import options
import requests
import bs4
import logging
import random
import time
import asyncio
import base64 

from sched import scheduler
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from aiogram.dispatcher import filters
from pornhub_api import PornhubApi
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from contextlib import suppress


bot = Bot(token = BOT_TOKEN)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.ERROR)

api = PornhubApi()

IMAGE_REGEXP = r'https://.+?\.(jpg|png|jpeg)'


@dp.message_handler(commands = ["start"], commands_prefix ="!/")
async def begin(message: types.Message):
    mes = await bot.get_me()
    print(mes)
    await bot.send_message(
        message.chat.id, text = "Слава роду. Путин президент мира."
        )


@dp.message_handler(commands = ["новзвон"], commands_prefix = "/!", commands_ignore_caption=False, content_types=["photo"])
async def new(message: types.Message):
        file_id = message.photo[-1].file_id
        print(file_id)
        fi =  open("time.txt", "w")
        fi.write(file_id)
        fi.close
        await bot.send_message(
            message.chat.id, text = "ок"
        )


@dp.message_handler(commands = ["звон"], commands_prefix = "!/")
async def zvonki(message: types.Message):
    ph = open("time.txt")
    zvon = ph.read()
    await bot.send_photo(
        message.chat.id, photo=zvon
        )


@dp.message_handler(commands = ["новрасп"], commands_prefix = "/!", commands_ignore_caption=False, content_types=["photo"])
async def new(message: types.Message):
        file_id = message.photo[-1].file_id
        print(file_id)
        fi =  open("schedule.txt", "w")
        fi.write(file_id)
        fi.close
        await bot.send_message(
            message.chat.id, text = "ок"
        )


@dp.message_handler(commands=["расп"], commands_prefix="!/")
async def rasp(message: types.Message):
    fi = open("schedule.txt")
    schedule = fi.read()
    await bot.send_photo(
        message.chat.id, photo=schedule
        )


@dp.message_handler(commands = ["загадка"], commands_prefix = "!/")
async def a(message: types.Message):
    # coded_string = "'''iVBORw0KGgoAAAANSUhEUgAAAegAAAHoAQMAAAC4nu5PAAAABlBMVEX///8AAABVwtN+AAAACXBIWXMAAA7EAAAOxAGVKw4bAAADVklEQVR4nO2WQXbjMAxDef9LY6YmANLJplv2weM4lsRPLeYHalWuXLn+8IW+/n//DH6+UOvWsDjEEKFP0rNS5NEMmz8L3fajV+iTdE+C8+oDqSFp9GIi9Gm68KXNPKc49F+h+S4n5pRQ9rtR6Mv0fsoL91MfaoQvIvQxWlb8/h+J0BdpX0DZDNCcp7bkyjcT+hzdU1qviQhZhIHZbZ8GoY/RNQFf1qOnpnqqwKnQd+mnHlMg2JOYugmL0DfpKo0VDutEmLugjpBjoW/SYPCXrfC7zeBw9gh9k/ZJvltAa7VeZMnaN/Q9mk8rs8ohR/ocWJGB0FdpzFEwfwWUe+u0L32/SkJfo4nKjFJGgFqssHC/nRuhb9ECsWLCLT+yYLGhj9KqtDUWZbKgCXUEdE6EvkeTrYFETiN6s5+F0EdpOBt2NCxMBeq80iH0NZoIFBAdEWPOWx15U2vz0KfoLmFCUB7Wz9fT7m1S6JM0XsHQs+w0nevlylYt9DHauTAfe/GqWzN4tQ59iXb0i3gL0QrVmFQ0J/RNukf84WsabLviwBupNPRJWm/u0Z+axJBBXcnaqtA36UaaLrVSDdyfNn30DX2NbhP0pTzQOtjSZbMS+iRtC/qX3+yaK/MF9Zcxoe/RXu2A0F1Tp46MiNkg9EXaIGbti+g93j6FvkjDeBepITRw9X7OzqFv0bLCP31sc2AYgmfX0Bfp+b9H136IYksmLJYvoa/RZSuIOydQq8VW5s2HvkQ7BrqHT3ksOcrdQZkkWehr9JKEZ0DJja1TYbm04dC3aFACvlEczdAoYtRnbR36Gm1LpIqM8OhdybFlCn2L1gmgNlhlYGff7ucYCX2PrimEE5/KwOJQFBBB6JN0kRC4XlZQQDTUtUKfpDX5lID0M56FZYeHCH2SbiGshuoA3nJleNaGPkkrGnwUzIu02PD6ayD0SRod7Q6DeZ2X2abIhT5Kz9KPApiuVmhFhnd7waHP0YRID8APFlz1xYa+Q8uIpQHkBgTA54RnQx+l9WQ4yI4eKCNKfekPQp+le7GRci5sj5YbmvOuoW/StqO5cahcizcT+jZdsqbmVOAx4JeXTqFP0jWWzBQ+b4hYboU+SDPfnxmWyojlCuyKTAp9ks6VK9cfvf4BPt9UM/iUTaYAAAAASUVORK5CYII='''"
    await bot.send_chat_action(message.chat.id, action="upload_document")
    file = open("riddle.txt", "rb")
    await bot.send_document(
        message.chat.id,
        document=file
        )



async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(commands = ["ядрочер"], commands_prefix = "/!")
async def Serega_Bez_Babi (message: types.Message):
    if message.from_user.id == 1071673992:
        try:
            await bot.send_chat_action(message.chat.id, action="upload_video")
            tags = random.sample(api.video.tags("f").tags, 5)
            category = random.choice(api.video.categories().categories)
            result = api.search.search(ordering="mostviewed", tags=tags, category=category)
            for vid in result.videos:
                serega = vid.url
            msg = await bot.send_message(
                message.chat.id, serega    
            )
            asyncio.create_task(delete_message(msg, 3))
        except Exception:
            msg = await bot.send_message(
                message.chat.id, text = "чет пошло не так"
            )
    else:
        await bot.send_message(
            message.chat.id, text = "ты не серега"
        )


@dp.message_handler(commands = ["кик"], commands_prefix = "!/")
async def id(message: types.Message):
    m = await bot.get_chat_member(message.chat.id, message.from_user.id)
    member = m['status']
    if member != ("administrator" or "creator"):
        await bot.send_message(
            message.chat.id, text = "Недостаточно прав для применения данной команды"
        )
        await bot.send_sticker(message.chat.id, sticker = "CAACAgIAAxkBAAEEQexiPPqhlb07DaKtlbL-z2G54aAuHAACFQgAAiHtuwM7fmJLu6P05yME")
    else:
        try:
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, 1)
        except Exception:
            await bot.send_message(
            message.chat.id, text = "перешли кого кикать"
            )



@dp.message_handler(lambda message: message.text.lower() == "да")
async def answers(message: types.Message):
    answers = [
        "пизда", "хуй на", "дорофтей", 
        "люблю тебя", "галактику на", "оригиналка - https://vk.com/kakashilox",
        "караганда"
        ]
    REPLY = random.choice(answers)
    await bot.send_message(
        message.chat.id, text = REPLY
    )


@dp.message_handler(lambda message: message.text.lower() == "нет")
async def answers(message: types.Message):
    answers = [
        "пидора ответ", "минет", "хуй в обед", 
        "скинь пару рублей", "тебе котлет", "оригиналка - https://vk.com/kakashilox",
        ]
    REPLY = random.choice(answers)
    await bot.send_message(
        message.chat.id, text = REPLY
    )


@dp.message_handler(lambda message: message.text.lower() == "хелп")
async def help(message: types.Message):
    await bot.send_message(
        message.chat.id, text = "звон - все \nновзвон - все \nрасп - все \nноврасп - все\nзагадка - для всех, но очень сложно[обновлено]\nкик - админы\nядрочер - только для сереги\nпрефиксы - / или !\n\nКоманды без префикса: \nанекдот - все\nотметь - все\nкикни - все\nкубик - все\nвероятность - все\nсделай опросик - все"        
    )


@dp.message_handler(regexp=IMAGE_REGEXP)
async def regexp_example(message: types.Message):
    await message.answer('там фотка')


@dp.message_handler(is_forwarded=True)
async def forwarded_example(message: types.Message):
    await bot.send_message(
        message.chat.id, text = "и че ты переслал зачем"        
    )


def getanekdot():
    z=''
    s= requests.get('http://anekdotme.ru/random')
    b= bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('.anekdot_text')
    for x in p:        
        s=(x.getText().strip())
        z=z+s+'\n\n'
    return s

@dp.message_handler(content_types=["text"])
async def handle_text(message):
    msg=message.text
    msg=msg.lower()
    if (u'анекдот' in msg):
        try:
            await bot.send_chat_action(message.chat.id, action="typing")
            await bot.send_message(message.chat.id, getanekdot())
        except:
            await bot.send_message(message.chat.id, text = "чет пошло не так")
    elif (u"вероятность" in msg):
        try:
            randomka = random.randint(1, 100)
            await bot.send_message(
                message.chat.id, text = "вероятность " + str(randomka) + "%"
            )
        except:
            await bot.send_message(message.chat.id, text = "чет пошло не так")
    elif (u"кубик" in msg):
        try:
            await bot.send_dice(
                message.chat.id
            )
        except:
            await bot.send_message(message.chat.id, text = "чет пошло не так")
    elif (u"пидор" in msg):
        try:
            answers = ["че обзываешься", "а может ты пидор?", "а ты о ком надеюсь не обо мне?"]
            await bot.send_message(
                message.chat.id, text = random.choice(answers)
            )
        except:
            await bot.send_message(message.chat.id, text = "чет пошло не так")
    elif (u"сделай опросик" in msg):
        try:
            await bot.send_chat_action(message.chat.id, action="upload_document")
            a = message.text.split("/")
            print(len(a))
            theme = a[1]
            option_one = a[2]
            option_second = a[3]
            if len(a) == 5:
                option_three = a[4]
                await bot.send_poll(
                message.chat.id, question= theme, options=[str(option_one.replace(" ", "", 1)), str(option_second.replace(" ", "", 1)), str(option_three.replace(" ", "", 1))]
            )
            else:
                await bot.send_poll(
                message.chat.id, question= theme, options=[str(option_one.replace(" ", "", 1)), str(option_second.replace(" ", "", 1))])
        except:
            await bot.send_message(message.chat.id, text = "ты наверно ошибся вот пример: \nсделай опросик / вова гей / да / нет")
    elif (u"отметь" in msg):
        try:
            usernames = message.reply_to_message.from_user.username
            if usernames == None:
                await bot.send_message(
                message.chat.id, text = "сори его нельзя отметить"
            )
            else:
                await bot.send_message(
                    message.chat.id, text = "@" + str(usernames), disable_notification=False
                )
        except Exception:
            await bot.send_message(
                message.chat.id, text = "перешли кого отметить то епта"
            )
    elif (u"кикни" in msg):
        m = await bot.get_chat_member(message.chat.id, message.from_user.id)
        member = m['status']
        if member != ("administrator" or "creator"):
            await bot.send_message(
                message.chat.id, text = "Недостаточно прав для применения данной команды"
            )
            await bot.send_sticker(message.chat.id, sticker = "CAACAgIAAxkBAAEEQexiPPqhlb07DaKtlbL-z2G54aAuHAACFQgAAiHtuwM7fmJLu6P05yME")
        else:
            try:
                await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, 1)
            except Exception:
                await bot.send_message(
                message.chat.id, text = "перешли кого кикать"
                )
    # elif (u"ид" in msg):
    #     try:
    #         mes = await bot.get_me()
    #         print(mes)
    #     except:
    #         await bot.send_message(message.chat.id, text = "какой опрос нормально напиш")
    
    # elif (u"никита" in msg):
    #     try:
    #         await bot.send_message(
    #             message.chat.id, text = "кто-то сказал никита? посмотри что я о нем думаю"
    #         )
    #         coder = "'''iVBORw0KGgoAAAANSUhEUgAAAmIAAAJiAQMAAABemDylAAAABlBMVEX///8AAABVwtN+AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFGklEQVR4nO2azY3rMAyECbgAl5TWXVIKMKAXkxz+ONnDO9IYHrxWJH3ay0AzkkVYLBaLxWq1L69DtiWvdco69uvx6dM3+20tfdPCkPUWweyTNNLG0/yvTnf4Z5Qy5KXj39cy+pu+fQbYFO09GoU00kbTIBYFbcuVtbuUXG264H6BrnGprANN0kh7DC0kogJStSlclSVYS3t9SyKNtIfSkhFmS2lX6VoGMo+GPYg00h5EM8ZFy/r8sq2UnK9V/Jiv8Ld/I420aTTMD5/1fw8v0kgbT8u6osUL7qrsKCqg9F4hKkvnfxVppE2jmWHq8hL51k5EEN2NfNzWthrSSHsArdquTOJVaAtqW6YnXG34NcZJGmnTaRJpWnyoNnGHt8qOUsWHR971kUbadJrn77yUwFnUiV4T2obrO9MYdOcPIY20R9DeG7YaWCx7O8KPfYXwBbO1fymLNNKm0vDwi4oqFo0lKaAVEV1SbTdlkUbaUBqiBUDt5k5ka8qS747VHBdppM2lxYBXGqvlnqqZrYzocVZbmkIaadNpoRO1XUVU5r3SdmVTe6vayi5DGmljaaW2ci7rm861ixxSm+2s9pdOSSNtMg2yMQMmEbhTWXEpAdtVx0GfpJE2mZZmC2+ZQ1r+FvELOgXBhcF7CWmkTaeh4Lh0OhSTNxhadm393lbVE7wXaaQ9hIaKhB2Ss0wOkLuwPZqaV36zSCNtEk1dU8sX7rMEzaMYK+v2qw1HkkbaQ2iwUzpAh/5S1tGPadVs5W9CGmnzadL3kZBNNFNZt0cG+OK4SCNtLA27R0kar5CXRm/XzpeyxM90m05JI20sTXxvcVGVk1es8Ete653TTpzukkbabBrclUWLd57Q4mb70AX7ga3d162qStJIm0+DYpqAXGjZzAWlD17gkkbaeFpKpAbzDNx+7pQntD51z2mkkTaeZpuEqyOv5ZBDwnFZM1RURIVe0kgbTkPWNhXtIRudXqL3rQk/Rhppj6GFOrBT+Bvk5SvsC/tNy+TeUXYZ0kibSjvLkayW/a4CCt2Z2Uo/1tVmOZ000ubTPI6rdjyMtGZTlifxzO53ZZFG2kyaeMxOjeV0kaCZ0MRV5Jk8H4s00sbTsHEUKZWEXdzV6rqLR/47pJE2m3b6VcRrrbiegAGLfSR3Gcmj25sLI420+bQiJYx3AZlsNhNVSeflmFYiu5NG2mjaVZGrm1i2VdfqFqvqaSvKIo20wbTNjqE8Yes77JRHEN2ISv4+6zgLI+1bKdJIG0nbPXD7F+BNRTh51V50xIxyc5cntKSRNpZm0fs0Y2WTjtCTykuPnGwfQQQp8rJlvr8bJI20cTTxoWmnLIRnh67Q8nczYHIr0kibSUOMyIStSinB4yhv2fTffHMijbSn0MJxiZsoSA62627A3rcHaaTNp4FxoIkc0h5FbSL4Krz0nqSRNp6mHWdopynGelvwKFr0TC7SvuggjbShNFQ6LpxA6UwXlWWOoygrOtZJGmmPomGDwUyt2H5yGZG41DbGHmdWpJE2mrZDIGad4hjKq3oq415NQ0avIUkjbTjN/2aW8KHlcBZ33OrH4tLO58Y/QRpp42lNInroGt9xhLEq8ir3ei6+kmVII+0BNPHTJsvkxx5vgjNYXybOdBHRSSPtWbRQzEKfv8WB1MtW3YrQJCikkTafZjN1zyh6ujpeuLTLR1oxmxc34KSRNp22vIx2k81+c1x4O3T9/EowlEUaaWNpLBaLxWJF/QNgR6NIGFfGtwAAAABJRU5ErkJggg=='''"
    #         await bot.send_photo(
    #             message.chat.id, photo = base64.b64decode(coder)
    #         )
    #     except:
    #         await bot.send_message(message.chat.id, text = "чет пошло не так")



@dp.message_handler(content_types=["video_note"])
async def handle_text(message):
    answers = [
        "ха еблан в кружочке", "ты нахуй сюда пишешь", 
        "го кикнем?", "и тебе того же", "вы прекрасны", "у тебя такие красивые глаза", 
        "кринжа навалил", "я весь день ждал от тебя кружок"]
    if message.from_user.id == 1071673992:
        answers.extend(("серега бля ты че все хуйней страдаешь", "серег ты ровный кент, люблю тебя", "восьмиклассницы ждут серег"))
    elif message.from_user.id == 1012078689:
        answers.extend(("иди уроки учи чепуха", "передай привет яна цист"))
    elif message.from_user.id == 536543837:
        answers.extend(("ха лысик", "сделаешь мне дизайн пожалуйста?👉👈"))
    answer = random.choice(answers)
    await bot.send_message(
        message.chat.id, text = answer
    )

@dp.message_handler(content_types=["dice"])
async def handle_text(message):
    await bot.send_message(
        message.chat.id, text = "ха лох сам смайлы отправляешь а мог бы меня попросить"
    )
      
@dp.message_handler(content_types=["voice"])
async def handle_voive(message):
    answers = ["че буквы запретили", "бля опять слушать", "у тебя прекрасный голос"]
    await bot.send_message(
        message.chat.id, text = random.choice(answers)
    )


executor.start_polling(dp, skip_updates=True)