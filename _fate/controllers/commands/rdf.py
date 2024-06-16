from common.dsc import *
import random as rng

@ACL.include
@arc.slash_command('rdf', 'rzuanie koścmi fate')
async def cmd_rdf(ctx: arc.GatewayContext):
  wyniki = ' '.join([rng.choice(['-', '0', '+']) for _ in range(4)])
  suma = wyniki.count('+') - wyniki.count('-')
  await ctx.respond(f'r df {wyniki} = {suma}')