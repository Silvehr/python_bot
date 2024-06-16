from common.models.Campaign import *
from common.dsc import *

from _fabula.local.consts import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('add-player-to-fabula-campaign', 'dodaje gracza do kampani w systemie fabula')
async def cmd_add_player_to_campaign(
  ctx: arc.GatewayContext,
  name: arc.Option[str, arc.StrParams('nazwa kampani')],
  user: arc.Option[hikari.User, arc.UserParams('gracz do dodania')],
):
  campaign = FABULA_CAMPAIGN_DB[name]
  campaign.players.append(user.id)
  FABULA_CAMPAIGN_DB[name] = campaign
  await ctx.respond(f'dodano gracza {user} do kampani {name}')