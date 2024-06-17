from common.dsc import *

@ACL.include
@arc.slash_command('elazer', 'przelicza drony na elazery')
async def cmd_elazer(ctx: arc.GatewayContext, number: arc.Option[int, arc.IntParams('podaj liczbe')]):
  elazery = number / 20
  await ctx.respond(f'Twój wynik to {elazery:.2f} elazerów dronek :3')
  
@ACL.include
@arc.slash_command('unelazer', 'przelicza elazery na drony')
async def cmd_unelazer(ctx: arc.GatewayContext, elazery: arc.Option[int, arc.IntParams('podaj liczbe elazerów')]):
    await ctx.respond(f"{elazery} elazerów to {elazery * 20} dronów")