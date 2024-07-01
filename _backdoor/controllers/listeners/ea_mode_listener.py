import hikari.embeds
from ...local import *
from ...models import *

from common.dsc.gateways import *
@BOT.listen(hikari.GuildMessageCreateEvent)
async def cmd_ea_mode_listener(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    user = str(event.author_id)
    
    if (user in EA_MODE_CLIENTS_DB) and (EA_MODE_CLIENTS_DB[user].enabled == True):
        response = hikari.Embed(
            title="Subskrypcja",
        )
        
        response.set_author(name=BOT.get_me().global_name)
        
        response.add_field(name="Chcesz dalej korzystać z naszych usług?", value="Uiść opłatę w wysokości 21.37 zł na podane konto, aby móc swobodnie korzystać z usług zarządzania kampaniami RPG w systemie Fabula Ultima oraz FATE Core")
        response.url  = RICKROLL
        response.set_image(hikari.files.URL(EA_PAYMENT_ICON))
        await event.message.respond(embed= response)