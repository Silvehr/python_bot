import hikari
import miru
import arc
import os

MEINID = '574540305597202434'

BOT = hikari.GatewayBot(
  token = os.environ["MaciekBot"],
  intents=hikari.Intents.ALL,
)

MCL = miru.Client(BOT)
ACL = arc.GatewayClient(BOT, default_enabled_guilds=(1235729134764822528,))