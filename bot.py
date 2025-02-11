import asyncio

import hikari

from common.dsc.gateways import *
from _developer.controllers import *
from _fabula.controllers import *
from _fate.controllers import *
from _rpg.controllers import *
from _resources.controllers import *
from _unit_translation.controllers import *
from _developer.models.reminder_service import *
from _developer.local.db import REMINDER_EVENTS_DB, REMINDER_LISTENERS_DB
from common.services import REGISTERED_SERVICES

@BOT.listen()
async def on_starting(event : hikari.StartedEvent):
    custom_activity = hikari.Activity(name='Solarite', type=hikari.ActivityType.LISTENING)
    await event.app.update_presence(activity=custom_activity)
    REGISTERED_SERVICES[ReminderService] = ReminderService(REMINDER_LISTENERS_DB, REMINDER_EVENTS_DB, True)
    REGISTERED_SERVICES[ReminderService].Initialize()
    await REGISTERED_SERVICES[ReminderService].Start()

@BOT.listen(hikari.StoppingEvent)
async def on_stopping(event):
    REGISTERED_SERVICES[ReminderService].Stop()

try:
    BOT.run()
finally:
    REGISTERED_SERVICES[ReminderService].Stop()

