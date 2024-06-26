from common.dsc.gateways import *
import random as rng
from common.functions import *
from _fate.local import FATE_PLAYER_DB, STATY_FATE

@ACL.include
@arc.slash_command('rdf', 'rzuanie koścmi fate')
async def cmd_rdf(ctx: arc.GatewayContext):
  wyniki = ' '.join([rng.choice(['-', '0', '+']) for _ in range(4)])
  suma = wyniki.count('+') - wyniki.count('-')
  await ctx.respond(f'r df {wyniki} = {suma}')
  
@ACL.include
@arc.slash_command('rdfc', 'rzucanie kośćmi fate ze statami twojej postaci')
async def cmd_rdfc(ctx: arc.GatewayContext, stat: arc.Option[str, arc.StrParams('stat twojej postaci', choices=STATY_FATE)], name: arc.Option[str, arc.StrParams('imie postaci')] = None):
  autid = ctx.author.id
  wyniki = ' '.join([rng.choice(['-', '0', '+']) for _ in range(4)])
  suma = wyniki.count('+') - wyniki.count('-')
  if name is None:
    try:
      suma += FATE_PLAYER_DB[str(autid)].skill.get(stat, 0)
    except KeyError:
      return await ctx.respond('nie jesteś w bazie danych')
  else:
    try:
      suma += FATE_PLAYER_DB.get_player_by_name(name).skill[stat]
    except KeyError:
      return await ctx.respond('nie ma takiej postaci')

  await ctx.respond(f'r df {wyniki} = **{suma}** na **{stat}**')