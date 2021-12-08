import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**𝙄𝙢 𝙈𝙚𝙣𝙩𝙞𝙤𝙣𝘼𝙡𝙡 𝘽𝙤𝙩**, 𝙄 𝙘𝙖𝙣 𝙢𝙚𝙣𝙩𝙞𝙤𝙣 𝙖𝙡𝙢𝙤𝙨𝙩 𝙖𝙡𝙡 𝙢𝙚𝙢𝙗𝙚𝙧𝙨 𝙞𝙣 𝙜𝙧𝙤𝙪𝙥 𝙤𝙧 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 👻\nClick **/help** 𝙛𝙤𝙧 𝙢𝙤𝙧𝙚 𝙞𝙣𝙛𝙤𝙢𝙖𝙩𝙞𝙤𝙣.",
                    buttons=(
                      [Button.url('📣 𝗖𝗵𝗮𝗻𝗻𝗲𝗹', 'https://t.me/Tg_Galaxy'),
                      Button.url('➕𝗔𝗱𝗱 𝗠𝗲 𝗚𝗿𝗼𝘂𝗽➕', 'http://t.me/Mentionallbot_Xbot?startgroup=true')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of MentionAllBot**\n\nCommand: /mall\n__You can use this command with text what you want to mention others.__\n`Example: /mall Good Night 🌃!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nBot Cloned Owner @HydraLivegrambot"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('📣 Channel', 'https://t.me/Tg_Galaxy'),
                      Button.url('👀 Source', 'https://t.me/Tg_Galaxy')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which sended before i added to group)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
