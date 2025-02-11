import hikari
import miru
import arc
import os

from .consts import *
from ..env.consts import REGISTERED_GUILDS

BOT = hikari.GatewayBot(
  token = os.environ["SASinBot"],
  intents=hikari.Intents.ALL,
)

MCL = miru.Client(BOT)
ACL = arc.GatewayClient(BOT, default_enabled_guilds=REGISTERED_GUILDS)