from common.dsc.gateways import *

@ACL.include
@arc.slash_command("rr", "If you do not want to let someone down...")
async def rickrollUser(ctx: arc.GatewayContext, user: arc.Option[hikari.User, arc.UserParams("User you don't wanna to give up")]):
    channel = await user.fetch_dm_channel()
    channel.send(f"# User {ctx.user.global_name} won't ever let you down... \nhttps://tenor.com/en-GB/view/rick-roll-gif-16249163500627956597")