from __future__ import annotations

import os
import signal
import asyncio

from time import sleep
from discord import (
    Intents,
    Activity,
    ActivityType,
    Status,
    Color
)
from discord.ext.commands import AutoShardedBot
from util import (
    Uptimer,
    CounterUpdater,
    Gitinfo,
    Logger
)
from database.servers import Servers

from typing import List

dirname = os.path.dirname(os.path.realpath(__file__))

folders = ["commands", "events"]

class MemberCounter(AutoShardedBot):
    def __init__(self, shard_count: int, shard_ids: List[int]) -> None:
        intents = Intents()
        # necessary intents
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix = '%',
            intents = intents,
            shard_count = shard_count,
            shard_ids = shard_ids,
            max_messages = None,
            chunk_guilds_at_startup = False
        )
        # internal 
        self.tree.on_error = self.app_command_error
        self.commands_loaded = False
        self.dirname = dirname

        # embed color
        self.color = Color.from_str("#05ffe6")

        # initializing logger
        self.logger = Logger(self, 'MemberCounter')

        # initializing gitinfo
        self.gitinfo = Gitinfo(self)

        # initializing database
        self.servers = Servers(self)

        # initializing updater
        self.updater = CounterUpdater(self)

        # initializing uptimer
        self.uptimer = Uptimer(self)

    async def setup_hook(self) -> None:
        self.loop.add_signal_handler(signal.SIGTERM, asyncio.create_task, self.exit())

    def boot(self, token: str, *, reconnect: bool = True) -> None:
        self.uptimer.start()
        self.run(token, reconnect = reconnect, log_handler = None)

    async def on_ready(self):
        self.logger.info(f'User: {self.user.name} | ID: {self.user.id}')
        self.logger.info(f'Owner: {self.application.owner} | ID: {self.application.owner.id}')
        self.logger.info(f"GitHash: {self.gitinfo.commitHash}")

        if not self.commands_loaded:
            await self.load_extensions()

        # trys to sync the application commands
        if os.getenv('SLASH_SYNC') == 'True':
            self.logger.info(f'Synchronize Slash Commands...')
            await self.tree.sync()

        await self.status()

    async def app_command_error(self, interaction, error):
        # calls the on_app_command_error by an error in command tree
        self.dispatch('app_command_error', interaction, error)

    async def status(self):
        # here will be set the bot status for each shard

        self.logger.info('Setting activity...')
        activity = Activity(type = ActivityType.watching, name = "Member Count")
        for shard in self.shards:
            await self.change_presence(status = Status.online, activity = activity, shard_id = shard)

        self.logger.info(f'Activity was changed')

    async def load_extensions(self):
        # here we are loading the extensions
        # the folders in the default configuration are loaded here 
        try:
            for path in folders:
                directorys = [i for i in os.listdir(os.path.join(dirname, path)) if os.path.isdir(os.path.join(dirname, path, i))]

                for directory in directorys:
                    pathdir = os.path.join(dirname, path, directory)

                    for _file in os.listdir(pathdir):
                        if _file.endswith('.py') and not _file.startswith('utils'):
                            try:
                                await self.load_extension(f'{path}.{directory}.{_file[0:-3]}')
                                # self.logger.info(f"Loaded: {_file[0:-3]}")

                            except Exception as e:
                                self.logger.warning(f'Couldn\'t load cog {_file} while {e}')

                self.logger.info(f'Successfully loaded {path}')
        except Exception as e:
            self.logger.warning(e)
            self.logger.warning(f'Shutdown in 5 sec...')
            sleep(5)
            await self.exit()
            return
        
        self.ext_loadded = True

    async def exit(self) -> None:
        await self.close()

    @property
    def invite_url(self) -> str:
        return "https://discord.com/api/oauth2/authorize?client_id={}&permissions={}&scope=bot%20applications.commands".format(self.user.id, os.getenv('INVITECODE'))
