from datetime import datetime, timedelta
from idlelib.replace import replace
from hikari import Message
from  common.dsc.gateways import BOT
from hikari.channels import DMChannel
from common.models.db.ShelveDB import ShelveDB
import asyncio
import uuid
import copy
import threading

class RemindEvent:
    def __init__(self, eventId: str, eventName: str, startDate : datetime, interval: timedelta, message: str):
        self.Id = eventId
        self.Name = eventName
        self.Message = message
        self.LastRun = startDate
        self.Interval = interval
        self.TriggerCount = 1
        self.Listeners: list[str] = []

    def AddListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId not in self.Listeners:
                self.Listeners += clientId

    def RemoveListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId in self.Listeners:
                self.Listeners.remove(clientId)

    async def InvokeReminder(self, service : "ReminderService"):
        self.TriggerCount+=1
        self.LastRun = datetime.now()
        for listener in self.Listeners:
            await (service.GetListener(listener)).Remind(self)

    def GetFormattedMessage(self,*args):
        cStart: int = 0
        cEnd: int = 0
        result = copy.copy(self.Message)

        while cStart != -1 and cEnd != -1:
            cStart = result.find('{', cStart)
            cEnd = result.find('}', cEnd)

            if cEnd == -1:
                break

            fieldName = result[cStart+1:cEnd]

            if fieldName.isdecimal():
                fieldName = int(fieldName)
                result = result.replace(f"{{{fieldName}}}", str(args[fieldName]))
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

                result = result.replace(f"{{{fieldName}}}", str(currentField))
            else:
                result = result.replace(f"{{{fieldName}}}", str(self.__getattribute__(fieldName)))

        return result

class GlobalReminder:
    def __init__(self, eventId: str, eventName: str, startDate : datetime, interval: timedelta, message: str):
        self.Id = eventId
        self.Name = eventName
        self.Message = message
        self.LastRun = startDate
        self.Interval = interval
        self.TriggerCount = 1
        self.Listeners: list[str] = []

    def AddListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId not in self.Listeners:
                self.Listeners.append(clientId)

    def RemoveListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId in self.Listeners:
                self.Listeners.remove(clientId)

    async def InvokeReminder(self, service : "ReminderService"):
        self.TriggerCount+=1
        self.LastRun = datetime.now()
        for listener in service._listeners.values():
            await listener.Remind(self)

    def GetFormattedMessage(self,*args):
        cStart: int = 0
        cEnd: int = 0
        result = copy.copy(self.Message)

        while cStart != -1 and cEnd != -1:
            cStart = result.find('{', cStart)
            cEnd = result.find('}', cEnd)

            if cEnd == -1:
                break

            fieldName = result[cStart+1:cEnd]

            if fieldName.isdecimal():
                fieldName = int(fieldName)
                result = result.replace(f"{{{fieldName}}}", str(args[fieldName]))
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

                result = result.replace(f"{{{fieldName}}}", str(currentField))
            else:
                result = result.replace(f"{{{fieldName}}}", str(self.__getattribute__(fieldName)))

        return result

class ReminderListener:
    def __init__(self, client_id: str):
        self.Id: str = client_id
        self.ReminderEvents: dict[str, int] = {}
        self._channelId: str = ""
        self._channel: DMChannel | None = None

    async def Remind(self, event: RemindEvent | GlobalReminder):
        if len(self._channelId) == 0:
            self._channel = await BOT.rest.create_dm_channel(self.Id)
            self._channelId = self._channel.id

        elif self._channel is None:
            self._channel = await BOT.rest.fetch_channel(self._channelId)

        await self._channel.send(event.GetFormattedMessage(self))

        if self.ReminderEvents.get(event.Id) is None:
            self.ReminderEvents[event.Id] = 1
        else:
            self.ReminderEvents[event.Id] += 1

class ReminderService:
    def __init__(self, listenerDb : ShelveDB[str, ReminderListener], eventDb: ShelveDB[str, RemindEvent | GlobalReminder], debug_mode: bool = False):
        self._listeners: dict[str,ReminderListener] = {}
        self._events: dict[str,RemindEvent | GlobalReminder] = {}
        self._running = False
        self._listenerDb: ShelveDB[str, ReminderListener] = listenerDb
        self._eventDb: ShelveDB[str, RemindEvent | GlobalReminder] = eventDb
        self.debug_mode = debug_mode
        self._task : asyncio.Task = None

    def Initialize(self):
        self._listeners = dict(self._listenerDb.items())
        self._events = dict(self._eventDb.items())

    async def _run(self):
        print("[Started]")
        if self.debug_mode:
            while self._running:
                print("Checking overdue reminders...")
                now = datetime.now()
                anyUserReminded = False
                for event in self._events.values():
                    if now - event.LastRun >= event.Interval:
                        anyUserReminded = True
                        await event.InvokeReminder(self)
                        print(f"Users reminded of \"{event.Name}\"")

                if not anyUserReminded:
                    print("No user was reminded :(")

                await asyncio.sleep(20)
        else:
            while self._running:
                now = datetime.now()
                for event in self._events.values():
                    if now - event.LastRun >= event.Interval:
                        await event.InvokeReminder(self)
                await asyncio.sleep(20)
        print("[Stopped]")

    def AddNewGlobalReminder(self, reminderName: str, startDate : datetime, interval: timedelta, message: str):
        eventToAdd = GlobalReminder(str(uuid.uuid4()), reminderName, startDate, interval, message)
        self._eventDb[eventToAdd.Id] = eventToAdd
        self._events[eventToAdd.Id] = eventToAdd
        return eventToAdd

    def AddNewReminder(self, eventName: str, startDate : datetime, interval: timedelta, message: str) -> RemindEvent:
        eventToAdd = RemindEvent(str(uuid.uuid4()), eventName, startDate, interval, message)
        self._eventDb[eventToAdd.Id] = eventToAdd
        self._events[eventToAdd.Id] = eventToAdd
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

        self.RemoveEventRecord(event)

    def AddListener(self, listenerId):
        listener = self._listeners.get(listenerId)

        if listener is None:
            listener = ReminderListener(listenerId)
            self._listenerDb[listenerId] = listener
            self._listeners[listenerId] = listener

    def AddListenerToReminder(self, reminderId: str, listenerId: str) -> bool:
        event = self._events.get(reminderId)

        if event is None:
            return False

        listener = self._listeners.get(listenerId)

        if listener is None: # check if user is registered
            listener = ReminderListener(listenerId)
            self._listenerDb[listenerId] = listener
            self._listeners[listenerId] = listener
        elif reminderId in listener.ReminderEvents: # Check if user is already listening to this reminder
            return False

        event.AddListeners(listenerId)

        self._eventDb[reminderId] = event
        self._listenerDb[listenerId] = listener

        return True

    def RemoveListenerFromEvent(self, reminderId: str, listenerId: str) -> bool:
        event = self._events.get(reminderId)
        if event is None:
            return False

        listener = self._listeners.get(listenerId)
        if listener is None:
            return False

        # clear record for counting reminder triggers for this user
        listener.ReminderEvents[event.Id] = 0

        # remove listener from event
        event.RemoveListeners(listener.Id)

        # update dbs
        self._eventDb[reminderId] = event
        self._listenerDb[listenerId] = listener

        return True

    def GetListener(self, listenerId: str) -> ReminderListener | None:
        return self._listenerDb.get_value(listenerId)

    def RemoveListener(self, listenerId: str) -> bool:
        listener = self._listeners.get(listenerId)
        if listener is None:
            return False

        for eventId in listener.ReminderEvents.keys():
            self._events[eventId].RemoveListeners(listenerId)

        self.RemoveListenerRecord(listener)
        return True

    def RemoveListenerRecord(self, listener: ReminderListener):
        del self._listenerDb[listener.Id]
        del self._listeners[listener.Id]

    def RemoveEventRecord(self, event: RemindEvent):
        del self._events[event.Id]
        del self._eventDb[event.Id]

    def Start(self):
        if not self._running:
            print("Starting service... ", end="")
            self._running = True
            self._eventDb.open()
            self._listenerDb.open()
            self._task = asyncio.create_task(self._run())
            return self._task

    def Stop(self):
        self._running = False
        if self._task and self._running:
            print("Stopping service... ", end="")
            self._task.cancel()
        self._eventDb.close()
        self._listenerDb.close()