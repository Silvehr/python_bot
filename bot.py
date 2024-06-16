from common.dsc import *

from _backdoor.backdoor import *
from _developer.developer import *
from _fabula.fabula import *
from _fate.fate import *
from _resources.resources import *
from _unit_translation.unit_translation import *

@BOT.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
  custom_activity = hikari.Activity(name='Solarite', type=hikari.ActivityType.LISTENING)
  await event.app.update_presence(activity=custom_activity)

BOT.run()
