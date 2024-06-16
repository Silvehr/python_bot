from common.models.Campaign import *
from common.dsc import *

from _fate.local.consts import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('del-fate-campaign', 'usuwa kampanie w systemie fate')
async def cmd_del_fate_campaign(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('nazwa kampani')]):
  msg = f'poprawinie usunięto kampanie {name}'
  if name in FATE_CAMPAIGN_DB:
    roles = FATE_CAMPAIGN_DB[name].roles.copy()
    del FATE_CAMPAIGN_DB[name]
  else:
    return await ctx.respond('nie ma takiej kampani')
  guild = ctx.get_guild()
  channels = guild.get_channels()
  categories = {cid: ch for cid, ch in channels.items() if ch.type == hikari.ChannelType.GUILD_CATEGORY}
  try:
    category_to_delete = [x for x in categories.values() if x.name == name][0]
  except IndexError:
    msg += '\n :x: nie ma kategori do usunięcia'
  else:
    channels_to_delete = [ch for ch in channels.values() if ch.parent_id == category_to_delete.id]
    await category_to_delete.delete()
    for channel in channels_to_delete:
      await channel.delete()
    guildroles = await BOT.rest.fetch_roles()
    roles_to_delete = [x for x in guildroles if x.id in roles]
    for role in roles_to_delete:
      await role.delete()
  await ctx.respond(msg)