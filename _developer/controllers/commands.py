from common.dsc.gateways import *

import tcrutils as tcr

@ACL.include
@arc.slash_command('dev', 'moje nie dam')
async def cmd_dev(ctx: arc.GatewayContext, code: arc.Option[str, arc.StrParams('kodzik nie dla frajerów')]):
  if ctx.author.id != 569608391840759837 and ctx.author.id != 574540305597202434:
    return await ctx.respond('nie dla psa kiełabasa frajerze moje')
  try:
    result = tcr.codeblock(tcr.fmt_iterable(eval(code), syntax_highlighting=True), langcode='ansi')
  except Exception as e:
    result = f'{tcr.codeblock(tcr.extract_error(e), langcode="txt" )}\n{tcr.codeblock(tcr.extract_traceback(e), langcode="py")}'
  await ctx.respond(result)
  
@ACL.include
@arc.slash_command("ping", "Komenda do weryfikacji aktywności bota")
async def cmd_ping(ctx: arc.GatewayContext):
  return await ctx.respond("pong!")