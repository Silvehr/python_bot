from common.dsc import *

from _fabula.local.consts import *

@ACL.include
@arc.slash_command('lvlup', 'zwiększa lvl postaci o 1')
async def cmd_lvlup(ctx: arc.GatewayContext, user: arc.Option[hikari.User, arc.UserParams('Postać do lvlupa')] = None):
  if user is None:
    user = ctx.user
  character = FABULA_PLAYER_DB[str(user.id)]
  character.clevel += 1
  character.stats["HP"] += 1
  character.stats["MP"] += 1
  FABULA_PLAYER_DB[str(user.id)] = character
  await ctx.respond(f'LVL UP! {character.character_name} ma lvl: {character.clevel}')