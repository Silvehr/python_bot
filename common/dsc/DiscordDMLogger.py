import hikari.channels
from ..models.Logger import *

import hikari
import arc
import miru
import tcrutils

class DiscordDMLogger(Logger):
    _gateway : hikari.GatewayBot
    _targetPersonId : str
    
    def __init__(self, gateway : arc.GatewayClient, targetPersonId : str):
        self._gateway = gateway
        self._targetPersonId = targetPersonId
    
    async def log_event(self,message: str):
        await (await self._gateway.rest.create_dm_channel(self._targetPersonId)).send(message)
        
    async def log_warning(self, warning : str):
        await (await self._gateway.rest.create_dm_channel(self._targetPersonId)).send(f"> !WARNING! : {warning}")
    
    async def log_error(self, error : Exception | str):
        await (await self._gateway.rest.create_dm_channel(self._targetPersonId)).send(f"EXCEPTION\n  {tcrutils.codeblock(str(error), langcode="v")}")