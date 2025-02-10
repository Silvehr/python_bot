from datetime import datetime, timedelta
from idlelib.replace import replace
from hikari import Message
from  common.dsc.gateways import BOT
from hikari.channels import DMChannel
from common.models.db.ShelveDB import ShelveDB
import asyncio
import uuid
import copy

class RemindEvent:
    def __init__(self, eventId: str, eventName: str, startDate : datetime, interval: timedelta, message: str):
        self.Id = eventId
        self.Name = eventName
        self.Message = message
        self.LastRun = startDate
        self.Interval = interval
        self.TriggerCount = 0
        self.Listeners: set[str] = set()

    def AddListener(self, clientId: str) -> bool:
        if clientId in self.Listeners:
            return False

        self.Listeners.add(clientId)
        return True

    def RemoveListener(self, clientId: str) -> bool:
        if clientId in self.Listeners:
            self.Listeners.remove(clientId)
            return True

        return False

    async def InvokeReminder(self, service : "ReminderService"):
        self.LastRun = datetime.now()
        for listener in self.Listeners:
            await (service.GetListener(listener.Id)).Remind(self)

    def GetFormattedMessage(self,*args):
        cStart: int = 0
        cEnd: int = 0
        result = copy.copy(self.Message)

        while cStart != -1 and cEnd != -1:
            cStart = result.find('{', cStart)
            cEnd = result.find('}', cEnd)

            fieldName = result[cStart+1:cEnd]

            if fieldName.isdecimal():
                fieldName = int(fieldName)
                result = result.replace(f"{{{fieldName}}}", args[fieldName])
            elif '.' in fieldName:
                fields = fieldName.split('.')
                currentIndex = 1
                currentField = None

                if fields[0].isdecimal():
                    fIndex = int(fields[0])
                    if fIndex < len(args):
                        currentField = args[fIndex]

                while currentIndex < len(fields):
                    if fields[currentIndex].isdecimal():
                        currentField = currentField[int(fields[currentIndex])]
                    else:
                        currentField = currentField.__getattribute__(fields[currentIndex])
                    currentIndex+=1

                result = result.replace(fieldName, str(currentField))
            else:
                result = result.replace(f"{{{fieldName}}}", self.__getattribute__(fieldName))

        return result

class ReminderListener:
    def __init__(self, client_id: str):
        self.Id: str = client_id
        self.ReminderEvents: dict[str, int] = {}
        self._channelId: str = ""
        self._channel: DMChannel | None = None

    async def Remind(self, event: "RemindEvent"):
        if len(self._channelId) == 0:
            self._channel = await BOT.rest.create_dm_channel(self.Id)
            self._channelId = self._channel.id

        elif self._channel is None:
            self._channel = await BOT.rest.fetch_channel(self._channelId)

        await self._channel.send(event.GetFormattedMessage(self))
        self.ReminderEvents[event.Id] += 1

class ReminderService:
    def __init__(self, listenerDb : ShelveDB[str, ReminderListener], eventDb: ShelveDB[str, RemindEvent], debug_mode: bool = False):
        self._clients: list[ReminderListener] = []
        self._events: list[RemindEvent] = []
        self._running = False
        self._listenerDb: ShelveDB[str, ReminderListener] = listenerDb
        self._eventDb: ShelveDB[str, RemindEvent] = eventDb
        self._task: asyncio.Task = None
        self.debug_mode = debug_mode

    def Initialize(self):
        self._clients = list(self._listenerDb.values())

    async def _run(self):
        if self.debug_mode:
            while self._running:
                print("Checking overdue reminders...")
                now = datetime.now()
                anyUserReminded = False
                for event in self._events:
                    if now - event.LastRun >= event.Interval:
                        anyUserReminded = True
                        await event.InvokeReminder(self)
                        print(f"Users reminded of \"{event.Name}\"")

                if not anyUserReminded:
                    print("No user was reminded :(")
    
                await asyncio.sleep(600)
        else:
            while self._running:
                now = datetime.now()
                for event in self._events:
                    if now - event.LastRun >= event.Interval:
                        await event.InvokeReminder(self)
                await asyncio.sleep(600)

    def AddNewReminderEvent(self, eventName: str, startDate : datetime, interval: timedelta, message: str) -> RemindEvent:
        eventToAdd = RemindEvent(str(uuid.uuid4()), eventName, startDate, interval, message)
        self._eventDb[eventToAdd.Id] = eventToAdd
        return eventToAdd

    def GetReminderEventsByName(self, eventName: str) -> list[RemindEvent]:
        result = []
        eventName = eventName.lower()
        for ev in self._eventDb.values():
            if eventName in ev.Name.lower():
                result.append(ev)

        return result

    def GetReminderEventById(self, eventId: str) -> RemindEvent | None:
        return self._eventDb.get_value(eventId)

    def FindReminders(self, eventIdOrName: str) -> list[RemindEvent]:
        reminder = self.GetReminderEventById(eventIdOrName)

        if reminder:
            return [reminder]
        else:
            return self.GetReminderEventsByName(eventIdOrName)

    def RemoveReminderEvent(self, eventId: str):
        event = self._eventDb.get_value(eventId)
        if event is None:
            return False

        for listenerId in event.Listeners:
            del self._listenerDb[listenerId].ReminderEvents[eventId]

        del self._eventDb[eventId]

    def AddListenerToEvent(self, eventId: str, listenerId: str) -> bool:
        event = self._eventDb.get_value(eventId)

        if event is None:
            return False

        listener = self._listenerDb.get_value(listenerId)

        if listener is None:
            listener = ReminderListener(str(uuid.uuid4()))
            self._listenerDb[listener.Id] = listener
        elif eventId in listener.ReminderEvents:
            return  False

        listener.ReminderEvents[event.Id] = 0
        event.AddListener(listener.Id)

        return True

    def RemoveListenerFromEvent(self, eventId: str, listenerId: str) -> bool:
        event = self._eventDb.get_value(eventId)

        if event is None:
            return False

        listener = self._listenerDb.get_value(listenerId)
        listener.ReminderEvents[event.Id] = 0
        event.RemoveListener(listener.Id)

        return True

    def GetListener(self, listenerId: str) -> ReminderListener | None:
        return self._listenerDb.get_value(listenerId)

    def RemoveListener(self, listenerId: str) -> bool:
        listener = self._listenerDb.get_value(listenerId)
        if listener is None:
            return False

        for eventId in listener.ReminderEvents.keys():
            self._eventDb[eventId].RemoveListener(listenerId)

        del self._listenerDb[listenerId]
        return True

    async def Start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    def Stop(self):
        self._running = False
        if self._task:
            self._task.cancel()