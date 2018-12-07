from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.utils import get_display_name
from telethon.tl.types import MessageEntityMentionName, MessageEntityTextUrl, MessageEntityMention, \
    MessageEntityBotCommand
from variables import rolename, users, pattern, lynchpattern, templynch, TLapp_version
from telethon.errors import DataInvalidError, MessageIdInvalidError, MessageNotModifiedError
# fun
from random import randint, random, choice
from time import sleep

import logging
import asyncio
import re
import json
from sys import argv

logging.basicConfig(filename="logs/{}.log".format(argv[1]), level=logging.ERROR,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger()


# pass your own here
api_id =
api_hash = ''
TLdevice_model = 'Its an'
TLsystem_version = 'Autobot'
TLlang_code = 'en'
TLsystem_lang_code = 'en'
# ids of both werewolfbots
wolfbots = [175844556, 198626752]
# id of achievment group
group = (-1001217315658)
# variable for sleeping before deleting stuff
sleeping = 2

# bot variables

jsonfile = './databases/{}.json'.format(argv[1])
joinpattern = '(/joinarmy$|/joinarmy {}|/joinarmy [{}]$|/joinarmy 1[{}]$' \
              '|/joinarmy 2[{}]$)'.format(argv[1], argv[2], argv[3], argv[4])
fleepattern = '(/fleearmy$|/fleearmy {}|/fleearmy [{}]$|/fleearmy 1[{}]$' \
              '|/fleearmy 2[{}]$)'.format(argv[1], argv[2], argv[3], argv[4])
autopattern = '^({0}|(?i)autoskip|(?i)/manual|(?i)Manual|(?i)/manual {1}|(?i)Manual {1})'.format(templynch, argv[1])
bot_id = int('{}'.format(argv[5]))

# userbot
client = TelegramClient('{}'.format(argv[1]), api_id, api_hash, device_model=TLdevice_model,
                        system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code,
                        system_lang_code=TLsystem_lang_code).start()
# fitting normal bot
bot = TelegramClient('{}_bot'.format(argv[1]), api_id, api_hash).start()


loop = asyncio.get_event_loop()
myself = get_display_name(loop.run_until_complete(client.get_me()))


data_file = open(jsonfile)
database = json.load(data_file)


class Tolynch:
    lynchid = -1
    is_auto = False
    is_thief = False
    is_joined = False

    def change_id(self, new_id):
        self.lynchid = new_id

    def change_auto(self, new_status):
        self.is_auto = new_status

    def change_thief(self, new_status):
        self.is_thief = new_status

    def change_joined(self, new_status):
        self.is_joined = new_status


tolynch = Tolynch()


async def await_event(tempclient, event, pre):
    message = asyncio.Future()

    @tempclient.on(event)
    async def hi(ev):
        if isinstance(ev, events.CallbackQuery.Event):
            await ev.answer()
            message.set_result(ev)
        else:
            message.set_result(ev.message)

    await pre
    message = await message
    tempclient.remove_event_handler(handler)
    return message


async def await_event2(tempclient, event, pre):
    message = asyncio.Future()

    @tempclient.on(event)
    async def hi(ev):
        if isinstance(ev, events.CallbackQuery.Event):
            await ev.answer()
            message.set_result(ev)
        else:
            message.set_result(ev.message)
    sended = await pre
    message = await message
    tempclient.remove_event_handler(handler)
    return message, sended


@client.on(events.NewMessage(chats=group, from_users=users, pattern=joinpattern))
async def handler(event):
    if event.is_reply is True:
        message = await event.get_reply_message()
        if message.buttons:
            payload = re.search(r'=(.+)', message.buttons[0][0].url)
            if payload:
                await bot.send_message('@clone_army', 'Joined game, bot is running.')
                await client.send_message(message.from_id, '/start ' + payload.group(1))
                tolynch.change_joined(True)
                stats(event.from_id, 1)
            else:
                delete = await event.reply('Please reply to a **join** button.')
                sleep(sleeping)
                await delete.delete()
        else:
            delete = await event.reply('Please reply to a **join** button.')
            sleep(sleeping)
            await delete.delete()
    else:
        delete = await event.reply('Please **reply** to a join button.')
        sleep(sleeping)
        await delete.delete()


@client.on(events.NewMessage(chats=group, from_users=wolfbots,
                             pattern=re.compile("Game Length").search))
async def handler(_):
    tolynch.change_joined(False)
    tolynch.change_auto(False)


@client.on(events.NewMessage(chats=group, from_users=wolfbots, pattern=re.compile(pattern.format(myself)).search))
async def handler(event):
    sleep(randint(1, 3))
    await event.respond('/dead')
    stats(event.from_id, 8)


@client.on(events.NewMessage(chats=group, from_users=users, pattern=fleepattern))
async def handler(event):
    message = await event.respond('/flee@werewolfbetabot')
    sleep(sleeping)
    await message.delete()
    tolynch.change_joined(False)
    stats(event.from_id, 2)


@client.on(events.NewMessage(from_users=users,
                             pattern='/autolynch'))
async def handler(event):
    payload = re.match(r"/autolynch (.+)", event.raw_text)
    if payload:
        if payload.group(1) == "on":
            tolynch.change_auto(True)
        elif payload.group(1) == "off":
            tolynch.change_auto(False)
        elif event.entities:
            if isinstance(event.entities[0], MessageEntityMention):
                temp = event.get_entities_text(MessageEntityMention)
                username = temp[0][1][1:len(temp[0][1])]
                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.username == username:
                        if member.id == tolynch.lynchid:
                            pass
                        else:
                            tolynch.change_id(member.id)
                            delete = await event.reply('Updated the person to lynch \o/')
                            sleep(sleeping)
                            await delete.delete()
                        break
            elif isinstance(event.entities[0], MessageEntityMentionName):
                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.id == event.entities[0].user_id:
                        if member.id == tolynch.lynchid:
                            pass
                        else:
                            tolynch.change_id(member.id)
                            delete = await event.reply('Updated the person to lynch \o/')
                            sleep(sleeping)
                            await delete.delete()
                        break
    else:
        if tolynch.is_auto:
            tolynch.change_auto(False)
        else:
            tolynch.change_auto(True)


@client.on(events.NewMessage(chats=group, from_users=430190253, pattern="Lynchorder"))
async def handler(event):
    if tolynch.is_auto and event.entities:
        if len(event.entities) > 1:
            for ente in event.entities:
                if isinstance(ente, MessageEntityMentionName):
                    if ente.user_id == bot_id:
                        nextid = event.entities.index(ente) + 1
                        if isinstance(event.entities[nextid], MessageEntityMentionName):
                            members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                            for member in members:
                                if member.id == event.entities[nextid].user_id:
                                    if member.id == tolynch.lynchid:
                                        pass
                                    else:
                                        tolynch.change_id(member.id)
                                        delete = await event.reply('Updated the person to lynch \o/')
                                        sleep(sleeping)
                                        await delete.delete()
                                    break
                        elif isinstance(event.entities[nextid], MessageEntityTextUrl):
                            payload = re.search(r'me/(.+)', event.entities[nextid].url)
                            if payload:
                                members = await client.get_participants(
                                    'https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                                for member in members:
                                    if member.username == payload.group(1):
                                        if member.id == tolynch.lynchid:
                                            pass
                                        else:
                                            tolynch.change_id(member.id)
                                            delete = await event.reply('Updated the person to lynch \o/')
                                            sleep(sleeping)
                                            await delete.delete()
                                        break
                            break
        elif len(event.entities) == 1:
            if isinstance(event.entities[0], MessageEntityMention):
                grr = event.entities[0]
                beginning = grr.offset + 1
                ending = grr.offset + grr.length
                username = event.message[beginning:ending]
                members = await client.get_participants(
                    'https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.username == username:
                        tolynch.change_id(member.id)
                        break
            elif isinstance(event.entities[0], MessageEntityMentionName):
                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.id == event.entities[0].user_id:
                        tolynch.change_id(member.id)
                        break


async def autolynch(event, liste, data):
    messageedit = bot.send_message('clone_army', 'Waiting for input')
    response = await await_event2(client, events.NewMessage(from_users=users, chats=group, pattern=autopattern),
                                  messageedit)
    payload = re.search(lynchpattern, response[0].raw_text)
    if payload:
        if response[0].is_reply is True:
            await bot.delete_messages('@clone_army', response[1].id)
            result = await response[0].get_reply_message()
            await detection(result, event, liste, data)
        elif response[0].entities:
            await bot.delete_messages('@clone_army', response[1].id)
            result = response[0]
            await detection(result, event, liste, data)
        else:
            await bot.delete_messages('@clone_army', response[1].id)
            await fail(event, liste)
        stats(response[0].from_id, 3)
    else:
        payload = re.search("(?i)Autoskip", response[0].raw_text)
        if payload:
            await bot.delete_messages('@clone_army', response[1].id)
            stats(response[0].from_id, 3)
        else:
            await bot.delete_messages('@clone_army', response[1].id)
            stats(response[0].from_id, 4)
            await manuallynch(event, liste)


async def fail(event, liste):
    await bot.send_message('@clone_army', "Automatic detection failed, manual needed.")
    await manuallynch(event, liste)


async def manuallynch(event, liste):
    messageedit = bot.send_message('@clone_army', event.message, buttons=liste)
    response = await await_event2(bot, events.CallbackQuery, messageedit)
    try:
        await event.message.click(data=response[0].data)
    except MessageIdInvalidError:
        pass
    for buttons in response[1].buttons:
        for button in buttons:
            if button.data == response[0].data:
                try:
                    await bot.edit_message('@clone_army', response[0].message_id, (
                        '{} choose {}!'.format(get_display_name(await response[0].get_sender()), button.text)))
                except MessageNotModifiedError:
                    pass
                stats(response[1].sender_id, 6)
                break


async def detection(result, event, liste, data):
    if 'Lynchorder:' in result.raw_text:
        for ente in result.entities:
            if isinstance(ente, MessageEntityMentionName):
                if ente.user_id == bot_id:
                    nextid = result.entities.index(ente) + 1
                    if isinstance(result.entities[nextid], MessageEntityMentionName):
                        members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                        for member in members:
                            if member.id == result.entities[nextid].user_id:
                                buttondata = data + str(member.id).encode('ascii')
                                try:
                                    await event.message.click(data=buttondata)
                                except DataInvalidError:
                                    await fail(event, liste)
                                except MessageIdInvalidError:
                                    pass
                                break
                        break
                    elif isinstance(result.entities[nextid], MessageEntityTextUrl):
                        payload = re.search(r'me/(.+)', result.entities[nextid].url)
                        if payload:
                            members = await client.get_participants(
                                'https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                            for member in members:
                                if member.username == payload.group(1):
                                    buttondata = data + str(member.id).encode('ascii')
                                    try:
                                        await event.message.click(data=buttondata)
                                    except DataInvalidError:
                                        await fail(event, liste)
                                    except MessageIdInvalidError:
                                        pass
                                    break
                        break
    elif result.entities is None or isinstance(result.entities[0], MessageEntityBotCommand):
        person = await result.get_sender()
        members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
        for member in members:
            if member.id == person.id:
                buttondata = data + str(member.id).encode('ascii')
                try:
                    await event.message.click(data=buttondata)
                except DataInvalidError:
                    await fail(event, liste)
                except MessageIdInvalidError:
                    pass
                break
    elif isinstance(result.entities[1], MessageEntityMention):
        grr = result.entities[1]
        beginning = grr.offset + 1
        ending = grr.offset + grr.length
        username = result.message[beginning:ending]
        members = await client.get_participants(
            'https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
        for member in members:
            if member.username == username:
                buttondata = data + str(member.id).encode('ascii')
                try:
                    await event.message.click(data=buttondata)
                except DataInvalidError:
                    await fail(event, liste)
                except MessageIdInvalidError:
                    pass
                break
    elif isinstance(result.entities[1], MessageEntityMentionName):
        if bot_id == result.entities[1].user_id:
            await fail(event, liste)
        members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
        for member in members:
            if member.id == result.entities[0].user_id:
                buttondata = data + str(member.id).encode('ascii')
                try:
                    await event.message.click(data=buttondata)
                except DataInvalidError:
                    await fail(event, liste)
                except MessageIdInvalidError:
                    pass
                break
    else:
        await fail(event, liste)


@client.on(events.NewMessage(chats=wolfbots))
async def handler(event):
    if event.buttons:
        liste = []
        x = 0
        for lists in event.buttons:
            subliste = []
            for item in lists:
                subliste.append(Button.inline(text=item.text, data=item.data))
                x += 1
                if x is 2:
                    liste.append(subliste)
                    subliste = []
                    x = 0
                elif item is lists[-1] and x is 1:
                    liste.append(subliste)
                else:
                    pass
        if 'speech' in event.raw_text:
            await pacifist_hack(event)
        elif 'do you want to lynch' in event.raw_text:
            data = event.buttons[0][0].data[0:51]
            if tolynch.is_auto:
                buttondata = data + str(tolynch.lynchid).encode('ascii')
                try:
                    await event.message.click(data=buttondata)
                except DataInvalidError:
                    await fail(event, liste)
            else:
                await autolynch(event, liste, data)
        else:
            messageedit = bot.send_message('@clone_army', event.message, buttons=liste)
            response = await await_event2(bot, events.CallbackQuery, messageedit)
            try:
                await event.message.click(data=response[0].data)
            except (MessageIdInvalidError, DataInvalidError):
                pass
            for buttons in response[1].buttons:
                for button in buttons:
                    if button.data == response[0].data:
                        try:
                            await bot.edit_message('@clone_army', response[0].message_id, (
                                '{} choose {}!'.format(get_display_name(await response[0].get_sender()), button.text)))
                        except MessageNotModifiedError:
                            pass
                        stats(response[1].sender_id, 6)
                        break
    elif tolynch.is_joined:
        await role_loop(event)
    else:
        if 'madly in love' in event.raw_text:
            await client.send_message(group, '/love')
            stats(event.from_id, 7)
        elif 'struck by love' in event.raw_text:
            await client.send_message(group, '/love')
            stats(event.from_id, 7)
        elif 'The cult has' in event.raw_text:
            await client.send_message(group, '/cult')
        elif 'Your role got stolen!' in event.raw_text:
            await client.send_message(group, '/role thief')
            tolynch.change_joined(True)
            tolynch.change_thief(True)
        elif 'successfully stole' in event.raw_text:
            await bot.send_message('@Clone_army', 'Looks like I got a new role :D')
        elif 'Unlock' in event.raw_text:
            await client.forward_messages(group, event.message)
        else:
            await bot.send_message('@clone_army', event.text)
            stats(event.from_id, 9)


async def pacifist_hack(event):
    # this whole shit just because handling callbacks is hard...
    messageedit = bot.send_message('@clone_army', event.message,
                                   buttons=Button.inline('Make love/peace, not war (🦋) !', data="hihi"))
    sender = await await_event(bot, events.CallbackQuery(data="hihi"), messageedit)
    try:
        await event.click(text='Peace!')
    except MessageIdInvalidError:
        pass
    try:
        await bot.edit_message('@clone_army', sender.message_id, (
            '{} choose PEACE. MORE PEACE!'.format(get_display_name(await sender.get_sender()))))
    except MessageNotModifiedError:
        pass
    stats(event.sender_id, 6)
    

async def role_loop(event):
    for item in rolename:
        if item in event.raw_text and tolynch.is_joined:
            tolynch.change_joined(False)
            if tolynch.is_thief:
                tolynch.change_thief(False)
                await real_loop(item, event)
            else:
                await await_event(client, events.NewMessage(chats=group, from_users=users,
                                                            pattern='/autorole$'),
                                  bot.send_message('@clone_army', 'Role detected: **' + item + '** '))
                sleep(randint(1, 3))
                await real_loop(item, event)
            break


async def real_loop(item, event):
    if item is rolename[4]:
        await client.send_message(group, '/role ga')
    elif item is rolename[16]:
        await client.send_message(group, '/role wc')
    elif item is rolename[9]:
        await client.send_message(group, '/role app')
    elif item is rolename[18]:
        await client.send_message(group, '/role CH')
    elif item is rolename[27]:
        await client.send_message(group, '/role SK')
    elif item is rolename[30]:
        await client.send_message(group, '/role clumsy')
    elif item is rolename[31]:
        await client.send_message(group, '/role alpha')
    elif item is rolename[13]:
        await client.send_message(group, '/role cub')
    elif item is rolename[12]:
        await client.send_message(group, '/role wolfman')
    elif item is rolename[14]:
        await client.send_message(group, '/role wiseelder')
    elif item is rolename[19]:
        await client.send_message(group, '/role cult')
    elif item is rolename[10]:
        await client.send_message(group, '/role seerfool')
    elif item is rolename[5]:
        if event.entities:
            await bot.send_message('@clone_army',
                                   "We got a seer, it should autosend it in the group. But because I don't "
                                   "trust my code, here is the message: {}".format(event.message.message))
            await client.send_message(group, "/role [This_fella_is_the_seer]("
                                             "tg://user?id={}) seer".format(event.entities[0].user_id))
        else:
            await bot.send_message('@clone_army', 'No seer, sad story :(')
            await client.send_message(group, "NO SEER GUYS. I'm sorry :(")
        await client.send_message(group, '/role beholder')
    else:
        await client.send_message(group, '/role ' + item)


def stats(ids, index):
    add = True
    for userids in database["users"]:
        if userids[0] == ids:
            add = False
            userids[index] += 1
            with open(jsonfile, 'w') as outfile:
                json.dump(database, outfile, indent=4, sort_keys=True)
            break
    if add:
        database["users"].append([ids, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for userids in database["users"]:
            if userids[0] == ids:
                userids[index] += 1
                with open(jsonfile, 'w') as outfile:
                    json.dump(database, outfile, indent=4, sort_keys=True)
                break


@client.on(events.NewMessage(chats='@Clone_Army', from_users=users, pattern='/stop all$|/stop {}'.format(argv[1])))
async def handler(event):
    await bot.send_message('@clone_army', 'Bot stopped')
    stats(event.from_id, 10)
    await client.disconnect()
    await bot.disconnect()
    logging.shutdown()
    exit()

# fun stuff


@client.on(events.NewMessage(from_users=users, pattern='(?i)Sudo {} (.+)|(?i)Sudo all (.+)'.format(argv[1])))
async def handler(event):
    if event.is_reply is True:
        result = await event.get_reply_message()
        if event.pattern_match.group(1):
            await result.reply('{}'.format(event.pattern_match.group(1)))
        else:
            await result.reply('{}'.format(event.pattern_match.group(2)))
    else:
        if event.pattern_match.group(1):
            await event.respond('{}'.format(event.pattern_match.group(1)))
        else:
            await event.respond('{}'.format(event.pattern_match.group(2)))


@client.on(events.NewMessage(from_users='Poolitzer', pattern='Who is a great dev?'))
async def handler(event):
    time = randint(0, 10)
    sleep(time)
    if event.is_reply is True:
        result = await event.get_reply_message()
        await result.reply('You are :)')
    else:
        await event.reply('You are :)')


@client.on(events.NewMessage(chats=group, pattern='#longhaul'))
async def handler(event):
    sleep(sleeping)
    if random() < .5:
        choose = choice(['Uh yes... Another long haul...', "Did someone say long haul?", "Why a long haul WHHYYY??",
                        "what are we even doing here boys", "Fuck me. Fuck. Fuck fuck fuck.", "Fuck",
                         "Can someone kill me?", "I don't want to do things here anymore", "Someone. Please. Fuck.",
                         "Argh. Don't trigger that.", "You wake it up", "Run. RUUUUUUUUUUUUUUUUN!!!!!!!!!!!!!!!!!!!!!!",
                         "I need to get more creative in this part of the army. Like, seriously. smh",
                         "Twenty-Seven should sleep more", "get me outta here!", "GRRRR. Way am I part of this?",
                         "This is stupid.", "hey, I'm a wolf, how shall I be useful as thief",
                         "Long haul? That’s as rare as Poolitzer.", "/klickme but that would actually kick the bots",
                         "ajahdhdjajdhdjd awwwn 😭", "my battery is dying\nso\nyeah"])
        await event.reply(choose)


client.start()
bot.start()
loop.create_task(bot.send_message('@clone_army', 'Bot is online'))
client.run_until_disconnected()
bot.run_until_disconnected()
