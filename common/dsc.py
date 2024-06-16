import hikari
import miru
import arc

MEINID = '569608391840759837'

BOT = hikari.GatewayBot(
  token="MTI1MTY2OTE4Nzc3NzI2OTc2MQ.GykAoV.4EQ_jXS41PxKK1tIh-KwK016VuegoD_kfJ3oXw",
  intents=hikari.Intents.ALL,
)

MCL = miru.Client(BOT)
ACL = arc.GatewayClient(BOT, default_enabled_guilds=(1235729134764822528,))