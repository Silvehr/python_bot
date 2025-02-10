from common.models.db.ShelveDB import ShelveDB
from _developer.models.reminder_service import *

REMINDER_EVENTS_DB : ShelveDB[str, RemindEvent] = ShelveDB("ReminderEvents")
REMINDER_CLIENTS_DB : ShelveDB[str, ReminderListener] = ShelveDB("ReminderClients")