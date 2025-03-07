from common.dsc.gateways import *
from _fabula.local import *
import random as rng

@ACL.include
@arc.slash_command('fabula-roll', 'rzuca na staty twojej postaci w fabula ultima')
async def cmd_fabula_roll(ctx: arc.GatewayContext, staty: arc.Option[str, arc.StrParams('staty na które rzucasz')]):
  staty = staty.upper()
  staty_split = staty.split()
  if len(staty_split) == 1:
    while True:
      rzut1 = rng.randint(1, (FABULA_PLAYER_DB[str(ctx.author.id)]).skill[staty_split[0]])
      rzut2 = rng.randint(1, (FABULA_PLAYER_DB[str(ctx.author.id)]).skill[staty_split[0]])
      if rzut1 >= 3 and rzut2 >= 3:
          break
    result = rzut1 + rzut2
    await ctx.respond(f'Wyrzuciłeś **{rzut1}** na {staty_split[0]} i **{rzut2}** na {staty_split[0]}, **suma: {result}**')
  else:
    while True:
      rzut1 = rng.randint(1, FABULA_PLAYER_DB[str(ctx.author.id)].skill[staty_split[0]])
      rzut2 = rng.randint(1, FABULA_PLAYER_DB[str(ctx.author.id)].skill[staty_split[1]])
      if rzut1 >= 3 and rzut2 >= 3:
        break
    result = rzut1 + rzut2
    await ctx.respond(f'Wyrzuciłeś **{rzut1}** na {staty_split[0]} i **{rzut2}** na {staty_split[1]}, **suma: {result}**')