from ...local import *
from ...models.models import *

from common.dsc.gateways import *
from common.models.Command import Command

@BOT.listen(hikari.GuildMessageCreateEvent)
async def analysis_of_user_as_text(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    await event.message.respond(event.message.content)
    
    