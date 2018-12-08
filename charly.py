from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.utils import get_display_name
from subprocess import call
from os import listdir
from variables import rolename, users, pattern, lynchpattern, templynch
from telethon.tl.types import MessageEntityMentionName, MessageEntityTextUrl, MessageEntityMention, \
    MessageEntityBotCommand
from telethon.errors import DataInvalidError, MessageIdInvalidError, MessageNotModifiedError
# fun
from random import randint, choice
from time import sleep

import logging
import asyncio
import re
import json

logging.basicConfig(filename="logs/charly.log", level=logging.ERROR, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger()

api_id =
api_hash = ''
TLdevice_model = 'Its an'
TLsystem_version = 'Autobot'
TLapp_version = '- Army 2.0'
TLlang_code = 'en'
TLsystem_lang_code = 'en'
wolfbots = [175844556, 198626752, 242418604]
group = (-1001217315658)
sleeping = 2

# bot variables

jsonfile = './databases/charly.json'
joinpattern = '(/joinarmy$|/joinarmy charly$|/joinarmy [1-9]| /joinarmy 1[0-9])$'
fleepattern = '(/fleearmy$|/fleearmy charly$|/fleearmy [1-9]| /joinarmy 1[1-9]$)'
autopattern = '^({}|(?i)autoskip|(?i)/manual|(?i)Manual|(?i)/manual charly|(?i)Manual Charly|' \
              '(i?)Charlylynch)'.format(templynch)
mylink = 'https://t.me/TheBetterCharly'
myname = 'TheBetterCharly'


data_file = open(jsonfile)
database = json.load(data_file)

client = TelegramClient('charly', api_id, api_hash, device_model=TLdevice_model, system_version=TLsystem_version,
                        app_version=TLapp_version, lang_code=TLlang_code, system_lang_code=TLsystem_lang_code).start()
bot = TelegramClient('charly_bot', api_id, api_hash).start()

loop = asyncio.get_event_loop()
myself = get_display_name(loop.run_until_complete(client.get_me()))


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


async def await_event(sender, chat, event):
    async with sender.conversation(chat) as conv:
        try:
            response = conv.wait_event(event)
            response = await response
            return response
        except asyncio.TimeoutError:
            pass


async def await_events(chat, event1, event2):
    async def wait1():
        async with bot.conversation('@Clone_Army') as conv:
            try:
                response = conv.wait_event(event1)
                response = await response
                return response
            except asyncio.TimeoutError:
                pass

    async def wait2():
        async with client.conversation(chat) as conv:
            try:
                response = conv.wait_event(event2)
                response = await response
                return response
            except asyncio.TimeoutError:
                pass

    async def wait_first():
        done, pending = await asyncio.wait(
            [wait1(), wait2()],
            return_when=asyncio.FIRST_COMPLETED)
        return done.pop().result()
    return await wait_first()


@client.on(events.NewMessage(chats=group, from_users='@Poolitzer', pattern="/afk"))
async def handler(_):
    call(['python3', 'poolitzer.py'])


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
                             pattern=re.compile(pattern.format(myself)).search))
async def handler(event):
    sleep(randint(1, 3))
    await event.respond('/dead')
    stats(event.from_id, 8)


@client.on(events.NewMessage(chats=group, from_users=wolfbots,
                             pattern=re.compile("Game Length").search))
async def handler(_):
    tolynch.change_joined(False)
    tolynch.change_auto(False)


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
            delete = await event.reply('Autolynch on, wuhu :)')
            sleep(sleeping)
            await delete.delete()
        elif payload.group(1) == "off":
            tolynch.change_auto(False)
            delete = await event.reply('Autolynch off, ohh :(')
            sleep(sleeping)
            await delete.delete()
        elif event.entities:
            if isinstance(event.entities[1], MessageEntityMention):
                temp = event.get_entities_text(MessageEntityMention)
                username = temp[0][1][1:len(temp[0][1])]
                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.username == username:
                        tolynch.change_id(member.id)
                        delete = await event.reply('Updated the person to lynch \o/')
                        sleep(sleeping)
                        await delete.delete()
                        break
            elif isinstance(event.entities[1], MessageEntityMentionName):
                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                for member in members:
                    if member.id == event.entities[1].user_id:
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
            delete = await event.reply('Autolynch off, ohh :(')
            sleep(sleeping)
            await delete.delete()
        else:
            tolynch.change_auto(True)
            delete = await event.reply('Autolynch on, wuhu :)')
            sleep(sleeping)
            await delete.delete()


@client.on(events.NewMessage(chats=group, from_users=430190253, pattern="Lynchorder"))
async def handler(event):
    if tolynch.is_auto and event.entities:
        if len(event.entities) > 1:
            for ente in event.entities:
                if isinstance(ente, MessageEntityTextUrl):
                    if ente.url == mylink:
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
                                members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
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


async def autolynch(event, liste, data):
    message = await bot.send_message('clone_army', 'Waiting for input')
    response = await await_event(client, group, events.NewMessage(from_users=users, chats=group, pattern=autopattern))
    payload = re.search(lynchpattern, response.raw_text)
    if payload:
        if response.is_reply is True:
            await bot.delete_messages('@clone_army', message.id)
            result = await response.get_reply_message()
            await detection(result, event, liste, data)
        elif response.entities:
            await bot.delete_messages('@clone_army', message.id)
            result = response
            await detection(result, event, liste, data)
        else:
            await bot.delete_messages('@clone_army', message.id)
            await fail(event, liste)
        stats(response.from_id, 3)
    else:
        payload = re.search("(?i)Autoskip", response.raw_text)
        if payload:
            await bot.delete_messages('@clone_army', message.id)
            stats(response.from_id, 3)
        else:
            await bot.delete_messages('@clone_army', message.id)
            stats(response.from_id, 4)
            await manuallynch(event, liste)


async def fail(event, liste):
    await bot.send_message('@clone_army', "Automatic detection failed, manual needed.")
    await manuallynch(event, liste)


async def manuallynch(event, liste):
    message = await bot.send_message('@clone_army', event.message, buttons=liste)
    response = await await_event(bot, "@Clone_Army", events.CallbackQuery)
    try:
        await event.message.click(data=response.data)
    except MessageIdInvalidError:
        pass
    for buttons in message.buttons:
        for button in buttons:
            if button.data == response.data:
                try:
                    await bot.edit_message('@clone_army', response.message_id, (
                        '{} choose {}!'.format(get_display_name(await response.get_sender()), button.text)))
                except MessageNotModifiedError:
                    pass
                stats(response.sender_id, 6)
                break


async def detection(result, event, liste, data):
    if 'Lynchorder:' in result.raw_text:
        for ente in result.entities:
            if isinstance(ente, MessageEntityTextUrl):
                if ente.url == mylink:
                    nextid = result.entities.index(ente) + 1
                    if isinstance(result.entities[nextid], MessageEntityMentionName):
                        members = await client.get_participants('https://t.me/joinchat/DG7UjkiOw0r1IfF7e5U8yQ')
                        for member in members:
                            if member.id == result.entities[nextid].user_id:
                                buttondata = data + str(member.id).encode('ascii')
                                try:
                                    await event.message.click(data=buttondata)
                                    break
                                except DataInvalidError:
                                    await fail(event, liste)
                                except MessageIdInvalidError:
                                    pass
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
    elif isinstance(result.entities[0], MessageEntityMention):
        grr = result.entities[0]
        beginning = grr.offset + 1
        ending = grr.offset + grr.length
        username = result.message[beginning:ending]
        if username == myname:
            await fail(event, liste)
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
    elif isinstance(result.entities[0], MessageEntityMentionName):
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
            buttonlist = await bot.send_message('@clone_army', event.message, buttons=liste)
            response = await await_event(bot, await event.get_chat(), events.CallbackQuery)
            try:
                await event.message.click(data=response.data)
            except MessageIdInvalidError:
                pass
            for buttons in buttonlist.buttons:
                for button in buttons:
                    if button.data == response.data:
                        try:
                            await bot.edit_message('@clone_army', response.message_id, (
                                '{} choose {}!'.format(get_display_name(await response.get_sender()), button.text)))
                        except MessageNotModifiedError:
                            pass
                        stats(response.sender_id, 6)
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
                await bot.send_message('@clone_army', 'Role detected: **' + item + '** ')
                await await_event(client, group, events.NewMessage(from_users=users, pattern='/autorole$'))
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
        database["users"].append([ids, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for userids in database["users"]:
            if userids[0] == ids:
                userids[index] += 1
                with open(jsonfile, 'w') as outfile:
                    json.dump(database, outfile, indent=4, sort_keys=True)
                break


@client.on(events.NewMessage(from_users=users, pattern='((i?)/armystats$)'))
async def handler(event):
    amount = 0
    joincount = 0
    fleecount = 0
    autocount = 0
    manualcount = 0
    buttoncount = 0
    for databases in listdir('./databases'):
        amount += 1
        tempfile = open('./databases/{}'.format(databases))
        tempbase = json.load(tempfile)
        for userids in tempbase["users"]:
            if userids[0] == event.from_id:
                joincount += userids[1]
                fleecount += userids[2]
                autocount += userids[3]
                manualcount += userids[4]
                buttoncount += userids[6]
        tempfile.close()
    await event.reply("Hey [{}](tg://user?id={}), here are your stats for the army:\n"
                      "You joined us {} times\n"
                      "You fleed us {} times\n"
                      "You used autolynch {} times\n"
                      "You used manual lynch {} times\n"
                      "You pressed {} buttons".format(get_display_name(await event.get_sender()),
                                                      event.from_id, joincount / amount,
                                                      fleecount / amount, autocount / amount,
                                                      manualcount / amount, buttoncount))


@client.on(events.NewMessage(from_users=users, pattern='/armystats (.+)'))
async def handler(event):
    expression = event.pattern_match.group(1)
    if expression:
        try:
            tempfile = open('./databases/{}.json'.format(expression))
            tempbase = json.load(tempfile)
            for userids in tempbase["users"]:
                if userids[0] == event.from_id:
                    await event.reply("Hey [{}](tg://user?id={}), here are your stats for {}:\n"
                                      "You joined me {} times\n"
                                      "You fleed me {} times\n"
                                      "You used autolynch {} times\n"
                                      "You used manual lynch {} times\n"
                                      "You pressed {} buttons".format(get_display_name(await event.get_sender()),
                                                                      event.from_id, expression, userids[1], userids[2],
                                                                      userids[3], userids[4], userids[6]))
                    tempfile.close()
                    break
        except FileNotFoundError:
            await event.reply("The wanted bot doesn't exist, I'm sorry :(")


@client.on(events.NewMessage(chats='@Clone_Army', from_users=users, pattern='/stop all$|/stop charly'))
async def handler(event):
    await bot.send_message('@clone_army', 'Bot stopped')
    stats(event.from_id, 10)
    await client.disconnect()
    await bot.disconnect()
    logging.shutdown()
    exit()


@client.on(events.NewMessage(chats='@Clone_Army', pattern='skip'))
async def handler(_):
    await bot.send_message('@clone_army', 'Skipping detection')
    tolynch.change_joined(False)


@client.on(events.NewMessage(chats='@Clone_Army', pattern='noskip'))
async def handler(_):
    await bot.send_message('@clone_army', 'Starting detection')
    tolynch.change_joined(True)


# fun stuff


@client.on(events.NewMessage(from_users='@Poolitzer', pattern='(?i)Sudo Charly (.+)|(?i)Sudo all (.+)'))
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


@client.on(events.NewMessage(from_users='@Poolitzer', pattern='Who is a great dev?'))
async def handler(event):
    if event.is_reply is True:
        result = await event.get_reply_message()
        delete = await result.reply('You are :)')
        sleep(sleeping)
        await delete.delete
    else:
        delete = await event.reply('You are :)')
        sleep(sleeping)
        await delete.delete


@client.on(events.NewMessage(pattern="(?i)Pingpoolitzer"))
async def handler(event):
    if event.from_id == 336513500:
        choose = ['@Poolitzer, Iba wants your attention. Better not ignore her.', "[POOOL](@poolitzer), come here. Now.",
                  "Oh come on Iba, do I need to call him again? @poolitzer, move.", "@Poolitzer, ping ;P", "@Poolitzer just made a fith one for Iba"]
        await event.reply(choice(choose))
    elif event.from_id == 502577108:
        await event.reply('Hey @Poolitzer, 27 want you here. Right. Now.')
    elif event.from_id == 685223169:
        await event.reply('I dont even know how this happend @Poolitzer')
    elif event.from_id == 481743192:
        await event.reply('Uh look Elli, you use this as well? Let me call @Poolitzer to this')
    elif event.from_id == 493051787:
        await event.reply('@Poolitzer, Kiri wants something from you :D')
    elif event.from_id == 416950101:
        await event.reply('Its Star. Pool. [POOOL](@poolitzer), he pinged you. Come and read it.')
    else:
        await event.reply('@Poolitzer, ping')
    await client.send_message('Poolitzer', 'PIIING')


@client.on(events.NewMessage(chats=group, pattern='DENIED'))
async def handler(event):
    await event.reply('@exagerado, someone said denied LOL')


@client.on(events.NewMessage(chats='@Clone_army', pattern='(?i)Iba'))
async def handler(event):
    await bot.send_message('@clone_army', 'Look :O', reply_to=event.id, buttons=Button.inline('🦋', ibaa))
    stats(event.from_id, 10)


async def ibaa(event):
    await event.edit('🦋')


@client.on(events.NewMessage(chats='@Clone_army', pattern='(?i)Jeha'))
async def handler(event):
    await bot.send_message('@clone_army', 'Look :O', reply_to=event.id, buttons=Button.inline('💚', jeha))
    stats(event.from_id, 11)


async def jeha(event):
    await event.edit('💚')


@client.on(events.NewMessage(chats='@Clone_army', pattern='(?i)Ludwig'))
async def handler(event):
    await bot.send_message('@clone_army', 'Look :O', reply_to=event.id, buttons=Button.inline('🐒', ludwig))
    stats(event.from_id, 12)


async def ludwig(event):
    await event.edit('🐒')


client.start()
bot.start()
loop.create_task(bot.send_message('@clone_army', 'Bot is online'))
client.run_until_disconnected()
bot.run_until_disconnected()
