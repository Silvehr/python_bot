import hikari
import miru
import arc
import os

MEINID = '574540305597202434'

BOT = hikari.GatewayBot(
  token = os.environ["SASinBot"],
  intents=hikari.Intents.ALL,
)

MCL = miru.Client(BOT)
ACL = arc.GatewayClient(BOT, default_enabled_guilds=(1136242057502019717, 1193537066944970752, 1231230423678455899, 1125762585501909042, 1067501387572838431, 1235729134764822528,))