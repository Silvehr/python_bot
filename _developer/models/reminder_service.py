from datetime import datetime, timedelta
import asyncio

import hikari.channels

from common.dsc.gateways import BOT
from common.models.db.ShelveDB import ShelveDB


class ReminderClient:
    client_id: str
    last_run: datetime
    interval: timedelta

    _message: str
    _reminder_counter: int

    _initialized: bool
    _channel_id: str
    _channel: hikari.channels.DMChannel

    def __init__(self, client_id: str, start_date: datetime, interval: timedelta, message: str):
        self.client_id = client_id
        self.last_run = start_date
        self.interval = interval
        self._message = message

        self._reminder_counter = 1
        self._initialized = False

    async def initialize_reminder_for_user(self):
        if not self._initialized:
            self._channel = await BOT.rest.create_dm_channel(self.client_id)
            self._channel_id = self._channel.id.__str__()
            self._initialized = True

    async def remind(self, db : ShelveDB):
        if not self._initialized:
            await self.initialize_reminder_for_user()

        try:
            channel = await BOT.rest.fetch_channel(channel=self._channel_id)
            await channel.send(self._message.replace("{c}", str(self._reminder_counter)))
            self._reminder_counter+=1
            self.last_run = datetime.now()
            self.save_user_state(db)

        except Exception as e:
            err_channel = await BOT.rest.create_dm_channel(569608391840759837)
            print(str(e))
            await err_channel.send(str(e))
            raise


    def save_user_state(self, db: ShelveDB):

        # Do not save the DMChannel object
        ch_tmp = self._channel
        self._channel = None

        db[self.client_id] = self

        self._channel = ch_tmp


class ReminderService:
    _clients: list[ReminderClient]
    _running = False
    _db : ShelveDB
    _task: asyncio.Task

    def __init__(self, db : ShelveDB):
        self._db = db

    def initialize(self):
        self._clients = list(self._db.items().values())

    async def _run(self):
        while self._running:
            now = datetime.now()
            for client in self._clients:
                if now - client.last_run >= client.interval:
                    await client.remind(self._db)

            await asyncio.sleep(600)

    def remove_client(self, client_id):
        self._db.__delitem__(client_id)
        for i in range(len(self._clients)):
            if self._clients[i].client_id == client_id:
                self._clients.pop(i)
                break

    async def add_client(self, client: ReminderClient):
        for i in range(len(self._clients)):
            if self._clients[i].client_id == client.client_id:
                return

        self._clients.append(client)
        await client.initialize_reminder_for_user()
        self._db[client.client_id] = client

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()




