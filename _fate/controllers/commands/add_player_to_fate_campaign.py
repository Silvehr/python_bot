from common.dsc import *

from _fate.local.consts import *

@ACL.include
@arc.slash_command('add-player-to-fate-campaign', 'dodaje gracza do kampani w systemie FATE Core')
async def cmd_add_player_to_fate_campaign(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('nazwa kampani')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do dodania')],
):
  campaign = FATE_CAMPAIGN_DB[name]
  campaign.players.append(user.id)
  FATE_CAMPAIGN_DB[name] = campaign
  await ctx.respond(f'dodano gracza {user} do kampani {name}')