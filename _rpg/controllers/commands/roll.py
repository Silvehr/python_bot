from common.dsc import *
import random as rng

@ACL.include
@arc.slash_command('roll', 'rzucanie koścmi')
async def cmd_roll(ctx: arc.GatewayContext, kosc: arc.Option[str, arc.StrParams('kosci jakimi chcesz rzucac liczby oddzielone spacją')]):
  kosc_split = [int(kosc) for kosc in kosc.split()]
  results = [rng.randint(1, item) for item in kosc_split]
  await ctx.respond(f'Wyrzuciłeś {', '.join([str(x) for x in results])}')