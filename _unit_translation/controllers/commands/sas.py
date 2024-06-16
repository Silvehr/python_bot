from common.dsc import *

@ACL.include
@arc.slash_command('sas', 'discription')
async def cmd_sas(ctx: arc.GatewayContext, number: arc.Option[int, arc.IntParams('podaj liczbe')]):
  wynik = number / 70000000
  await ctx.respond(f'Liczba {number} to {wynik:.7f}sas')