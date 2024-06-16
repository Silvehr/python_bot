from _backdoor.local.consts import *

from common.dsc import *

import tcrutils as tcr

@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_ea_mode_listener(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    user = event.author_id
    
    if (user in EA_MODE_CLIENTS) and (EA_MODE_CLIENTS[user].enabled == True):
        await event.message.respond("test passes, smth is wrong with respond in **embed**")
        await event.message.respond(embed= tcr.discord.embed(
            tcr.Null,
            'Zapłać 21.37zł aby móc swobodnie używać naszych usług',
            color=0xF0BFFF,
            footer='uwu',
            author={
                'name': f'Płatność',
                'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
            },
        ))
    else:
        await event.message.respond(f"test not passed, smth is wrong with db check (checked id : {user})")