from common.models.Campaign import *
from common.dsc import *

from _fate.local.consts import *

import tcrutils as tcr


@ACL.include
@arc.slash_command('show-fate-campaign', 'pokazuje info o kampani')
async def cmd_show_fate_campaign(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('nazwa kampani')]):
  try:
    campaign = FATE_CAMPAIGN_DB[name]
  except KeyError:
    return await ctx.respond('keep yourself safe nie ma takiej kampani')
  await ctx.respond(
    tcr.discord.embed(
      tcr.Null,
      f'### Name: {campaign.name} \n system: {campaign.system.value} \n Universe: {campaign.universe} \n GMs: \n{'\n'.join(f'- <@{x}>' for x in campaign.gms)}\n\n Players: \n{'\n'.join(f'- <@{x}>' for x in campaign.players)}',
      color=0xF0BFFF,
      footer='uwu',
      author={
        'name': f'Info - {campaign.name}',
        'icon': 'https://cdn.discordapp.com/attachments/866366097242325016/1209539245673422969/cute-anime-pfp-profile-pictures-girls-29.png?ex=65e74a34&is=65d4d534&hm=b76291968f902ca0ad92962354b9ab748f4d902bbd3ca229ed489dfd0de5bbca&',
      },
    )
  )