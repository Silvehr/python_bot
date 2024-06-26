from common.dsc.gateways import *

from _backdoor.controllers import * 
from _cyberpunk.controllers import *
from _developer.controllers import *
from _fabula.controllers import *
from _fate.controllers import *
from _rpg.controllers import *
from _resources.controllers import *
from _unit_translation.controllers import *

@BOT.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
  custom_activity = hikari.Activity(name='Solarite', type=hikari.ActivityType.LISTENING)
  await event.app.update_presence(activity=custom_activity)


BOT.run()