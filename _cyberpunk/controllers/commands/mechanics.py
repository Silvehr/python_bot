from common.dsc.gateways import *

import random as rng

@ACL.include
@arc.slash_command('cyberpunk-roll', 'Rzut kośćmi do cyberpunka')
async def cmd_cyberpunk_roll(ctx: arc.GatewayContext, stat: arc.Option[int, arc.IntParams('Wartość twojej statystyki')], skill: arc.Option[int, arc.IntParams('Wartość twojego skilla')]):
    roll = rng.randint(1, 10)
    suma = roll + stat + skill
    await ctx.respond(f'Wyrzuciłeś {roll} + {stat} + {skill} = **{suma}**')
