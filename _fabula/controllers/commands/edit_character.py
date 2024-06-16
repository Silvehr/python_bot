from common.dsc import *
from common.functions import *

from _fabula.models.FabulaPlayer import *
from _fabula.local.consts import *

@ACL.include
@arc.slash_command('edit_character', 'edytuje konkretny element postaci')
async def cmd_edit_character(ctx: arc.GatewayContext, name: arc.Option[str, arc.StrParams('Imie postaci')],element: arc.Option[str, arc.StrParams('element do edycji', choices=list(FabulaPlayer.__annotations__))], value: arc.Option[str, arc.StrParams('nowa zawartosc')]):
  character = FABULA_PLAYER_DB[name]
  character.__setattr__(element, value)
  FABULA_PLAYER_DB[name] = character
  await ctx.respond(f'Zmieniono {element} dla {name} na {value}')