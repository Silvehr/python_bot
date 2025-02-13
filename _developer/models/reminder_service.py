import json
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

class Reminder:
    def __init__(self, **kwargs):
        self.Id: str = kwargs["id"]
        self.Name: str = kwargs["name"]
        self.Message: str = kwargs["message"]
        self.NextRun: datetime = kwargs["startDate"]

        self.Listeners: list[str] = kwargs.get("listeners")
        if self.Listeners is None:
            self.Listeners = []

        if kwargs.get("interval") is None:
            self.TriggerCount: int = 1
            self.Interval: timedelta = timedelta(0)
        elif kwargs.get("triggerCount") is None:
            self.TriggerCount: int = -1
            self.Interval: timedelta = kwargs["interval"]
        else:
            self.TriggerCount: int = kwargs["triggerCount"]
            self.Interval: timedelta = kwargs["interval"]

    def AddListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId not in self.Listeners:
                self.Listeners += clientId

    def RemoveListeners(self, *clientIds: str):
        for clientId in clientIds:
            if clientId in self.Listeners:
                self.Listeners.remove(clientId)

    async def InvokeReminder(self, service : "ReminderService"):
        if self.TriggerCount != 0:
            if self.TriggerCount > 0:
                self.TriggerCount -= 1
            self.NextRun = datetime.now() + self.Interval
            for listener in self.Listeners:
                listener = service.GetListener(listener)
                await listener.Remind(self)
                service.SaveListener(listener)

    def GetFormattedMessage(self,*args):
        cStart: int = 0
        cEnd: int = 0
        result = copy.copy(self.Message)
        result = result.replace("$id", self.Id)

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
    def __init__(self, clientId: str):
        self.Id: str = clientId
        self.ReminderEvents: dict[str, int] = {}
        self._channelId: str = ""
        self._channel: DMChannel | None = None

    async def Remind(self, reminder: Reminder):
        if len(self._channelId) == 0:
            self._channel = await BOT.rest.create_dm_channel(self.Id)
            self._channelId = str(self._channel.id)

        elif self._channel is None:
            self._channel = await BOT.rest.fetch_channel(self._channelId)

        if self.ReminderEvents.get(reminder.Id) is None:
            self.ReminderEvents[reminder.Id] = 1
        else:
            self.ReminderEvents[reminder.Id] += 1

        await self._channel.send(reminder.GetFormattedMessage(self.Id, self.ReminderEvents[reminder.Id]))

class ReminderService:
    def __init__(self, listenerDb : ShelveDB[str, ReminderListener], reminderDb: ShelveDB[str, Reminder], debug_mode: bool = False):
        self._listeners: dict[str,ReminderListener] = {}
        self._reminders: dict[str, Reminder] = {}
        self._running = False
        self._listenerDb: ShelveDB[str, ReminderListener] = listenerDb
        self._reminderDb: ShelveDB[str, Reminder] = reminderDb
        self._debugMode = debug_mode
        self._task : asyncio.Task = None

    def Initialize(self):
        self._listeners = dict(self._listenerDb.items())
        self._reminders = dict(self._reminderDb.items())

    async def _run(self):
        print("[Started]")
        if self._debugMode:
            while self._running:
                print("Checking overdue reminders...")
                now = datetime.now()
                anyUserReminded = False
                remindersToRemove = []
                for reminderId, reminder in self._reminders.items():
                    if reminder.TriggerCount == 0:
                        remindersToRemove.append(reminderId)
                    elif now >= reminder.NextRun:
                        await reminder.InvokeReminder(self)
                        self._reminderDb[reminderId] = reminder

                for reminderId in remindersToRemove:
                    self.RemoveReminder(reminderId)

                if not anyUserReminded:
                    print("No user was reminded :(")

                await asyncio.sleep(20)
        else:
            while self._running:
                now = datetime.now()
                remindersToRemove = []
                for reminderId, reminder in self._reminders.items():
                    if reminder.TriggerCount == 0:
                        remindersToRemove.append(reminderId)
                    elif now >= reminder.NextRun:
                        await reminder.InvokeReminder(self)
                        self._reminderDb[reminderId] = reminder

                for reminderId in remindersToRemove:
                    self.RemoveReminder(reminderId)

                await asyncio.sleep(20)
        print("[Stopped]")

    def AddNewReminder(
            self,
            reminderName: str,
            message: str,
            startDate : datetime,
            interval: timedelta = timedelta(0,0,0,0,0),
            triggerCount = 1,
            listeners: list[str] | None = None
    ) -> Reminder:
        eventToAdd = Reminder(
            id=str(uuid.uuid4()),
            name=reminderName,
            startDate=startDate,
            interval=interval,
            message=message,
            triggerCount=triggerCount,
            listeners=listeners
        )
        self._reminderDb[eventToAdd.Id] = eventToAdd
        self._reminders[eventToAdd.Id] = eventToAdd
        return eventToAdd

    def GetReminderEventsByName(self, eventName: str) -> list[Reminder]:
        result = []
        eventName = eventName.lower()
        for ev in self._reminderDb.values():
            if eventName in ev.Name.lower():
                result.append(ev)

        return result

    def GetReminderEventById(self, eventId: str) -> Reminder | None:
        return self._reminderDb.get_value(eventId)

    def FindReminders(self, eventIdOrName: str) -> list[Reminder]:
        reminder = self.GetReminderEventById(eventIdOrName)

        if reminder:
            return [reminder]
        else:
            return self.GetReminderEventsByName(eventIdOrName)

    def RemoveReminder(self, eventId: str):
        event = self._reminderDb.get_value(eventId)
        if event is None:
            return False

        for listenerId in event.Listeners:
            del self._listenerDb[listenerId].ReminderEvents[eventId]

        self.RemoveEventRecord(event)

    def AddListenerToReminder(self, reminderId: str, listenerId: str) -> bool:
        event = self._reminders.get(reminderId)

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

        self._reminderDb[reminderId] = event
        self._listenerDb[listenerId] = listener

        return True

    def RemoveReminderListener(self, reminderId: str, listenerId: str) -> bool:
        event = self._reminders.get(reminderId)
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
        self._reminderDb[reminderId] = event
        self._listenerDb[listenerId] = listener

        return True

    def GetListener(self, listenerId: str) -> ReminderListener | None:
        listener = self._listenerDb.get_value(listenerId)
        if listener is None:
            listener = ReminderListener(listenerId)
            self._listenerDb[listenerId] = listener
            self._listeners[listenerId] = listener

        return listener

    def RemoveListener(self, listenerId: str) -> bool:
        listener = self._listeners.get(listenerId)
        if listener is None:
            return False

        for eventId in listener.ReminderEvents.keys():
            self._reminders[eventId].RemoveListeners(listenerId)

        self.RemoveListenerRecord(listener)
        return True

    def RemoveEmptyListeners(self):
        for listenerId, listener in self._listeners.items():
            if len(listener.ReminderEvents) == 0:
                self.RemoveListenerRecord(listener)

    def SaveListener(self, listener: ReminderListener):
        chTmp = listener._channel
        listener._channel = None
        self._listenerDb[listener.Id] = listener
        listener._channel = chTmp

    def RemoveListenerRecord(self, listener: ReminderListener):
        del self._listenerDb[listener.Id]
        del self._listeners[listener.Id]

    def RemoveEventRecord(self, event: Reminder):
        del self._reminders[event.Id]
        del self._reminderDb[event.Id]

    def Start(self):
        if not self._running:
            print("Starting service... ", end="")
            self._running = True
            self._reminderDb.open()
            self._listenerDb.open()
            self._task = asyncio.create_task(self._run())
            return self._task
    def Stop(self):
        self._running = False
        if self._task and self._running:
            print("Stopping service... ", end="")
            self._task.cancel()
        self._reminderDb.close()
        self._listenerDb.close()