from common.dsc import *

@ACL.include
@arc.slash_command('unsas', 'przelicza liczby z sasinów')
async def cmd_unsas(ctx: arc.GatewayContext, number: arc.Option[float, arc.FloatParams('podaj liczbe')]):
  wynik = number * 70000000
  await ctx.respond(f'Liczba {number}sas to {wynik:.2f}')