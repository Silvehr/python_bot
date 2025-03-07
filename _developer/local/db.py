from common.models.db.ShelveDB import ShelveDB
from _developer.models.reminder_service import *

REMINDER_EVENTS_DB : ShelveDB[str, Reminder] = ShelveDB("ReminderEvents")
REMINDER_LISTENERS_DB : ShelveDB[str, ReminderListener] = ShelveDB("ReminderClients")