from common.dsc import *

from _fabula.local import *

import random as rng
import tcrutils as tcr

@ACL.include
@arc.slash_command('fabula-roll', 'rzuca na staty twojej postaci w fabula ultima')
async def cmd_fabula_roll(ctx: arc.GatewayContext, staty: arc.Option[str, arc.StrParams('staty na które rzucasz')]):
  staty = staty.upper()
  staty_split = staty.split()
  if len(staty_split) == 1:
    rzut1 = rng.randint(1, (FABULA_PLAYER_DB[str(ctx.author.id)]).skill[staty_split[0]])
    rzut2 = rng.randint(1, (FABULA_PLAYER_DB[str(ctx.author.id)]).skill[staty_split[0]])
    result = rzut1 + rzut2
    await ctx.respond(f'Wyrzuciłeś **{rzut1}** na {staty_split[0]} i **{rzut2}** na {staty_split[0]}, **suma: {result}**')
  else:
    rzut1 = rng.randint(1, FABULA_PLAYER_DB[str(ctx.author.id)].skill[staty_split[0]])
    rzut2 = rng.randint(1, FABULA_PLAYER_DB[str(ctx.author.id)].skill[staty_split[1]])
    result = rzut1 + rzut2
    await ctx.respond(f'Wyrzuciłeś **{rzut1}** na {staty_split[0]} i **{rzut2}** na {staty_split[1]}, **suma: {result}**')