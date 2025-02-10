from common.dsc.gateways import *

from _backdoor.controllers import * 
#from _cyberpunk.controllers import *
from _developer.controllers import *
from _fabula.controllers import *
from _fate.controllers import *
from _rpg.controllers import *
from _resources.controllers import *
from _unit_translation.controllers import *
from _developer.models.reminder_service import *
from _developer.local.db import REMINDER_DB
from common.services import REGISTERED_SERVICES

@BOT.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
  custom_activity = hikari.Activity(name='Solarite', type=hikari.ActivityType.LISTENING)
  await event.app.update_presence(activity=custom_activity)

reminder_service = ReminderService(REMINDER_DB)
reminder_service.initialize()
reminder_service.start()

REGISTERED_SERVICES["ReminderService"] = reminder_service

BOT.run()

reminder_service.stop()
