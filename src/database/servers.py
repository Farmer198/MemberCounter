from __future__ import annotations

import os
from discord import Guild
from time import time
from sqlite3 import (
    Connection,
    connect
)

from enum import Enum
from typing import TYPE_CHECKING, Optional

__all__ = (
    'Tags',
    'Server',
    'Servers'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

class Tags(Enum):
    guild_id = "guild_id"
    count_bots = "count_bots"
    last_update = "last_update"

    def to_dict():
        dct = {}
        for i in Tags:
            dct[i.name] = i.value
        return dct

class Server:
    __slots__ = (
        "manager",
        "guild_id",
        "count_bots",
        "last_update"
    )

    def __init__(self, manager, data: dict) -> None:
        self.manager: Servers = manager
        self._from_data(data = data)

    def _from_data(self, data: dict) -> None:
        try:
            self.guild_id: int = int(data["guild_id"])
            self.count_bots: bool = bool(data["count_bots"])
            self.last_update: int = int(data["last_update"])
        except KeyError as key:
            missing_key, = key.args
            raise KeyError('Cannot build Server from partial data! (Missing key: {})'.format(missing_key))

    def __repr__(self) -> str:
        attrs = (
            ('id', self.guild_id),
            ('count_bots', self.count_bots),
            ('last_update', self.last_update),
        )
        inner = ' '.join('%s=%r' % t for t in attrs)
        return f'<Server {inner}>'

    def set_id(self, value: int) -> None:
        self.guild_id = value
        self.manager.update_server(self.guild_id, Tags.guild_id, self.guild_id)

    def set_count_bots(self, value: bool) -> None:
        self.count_bots = value
        self.manager.update_server(self.guild_id, Tags.count_bots, int(self.count_bots))

    def set_last_update(self, value: int) -> None:
        self.last_update = value
        self.manager.update_server(self.guild_id, Tags.last_update, self.last_update)

    @property
    def guild(self) -> Optional[Guild]:
        return self.manager.client.get_guild(self.guild_id)

class Servers:

    __slots__ = (
        'client',
        '_cache',
        'db'
    )
    
    def __init__(self, client: MemberCounter) -> None:
        self.client: MemberCounter = client
        self._cache: dict = {}

        # check path
        self.check_path()

        # init database
        self.db: Connection = connect(r"{0}/data/database.db".format(self.client.dirname))

        # check table
        self.check_table()

    def check_path(self) -> None:
        path = "{}/data".format(self.client.dirname)
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)

    def check_table(self) -> None:
        cursor = self.db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS "guilds" (
                    "guild_id"	INTEGER NOT NULL,
                    "count_bots"	INTEGER NOT NULL,
                    "last_update"	INTEGER NOT NULL,
                    PRIMARY KEY("guild_id")
                );"""
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def create_server(self, guild_id: int):
        if guild_id is None:
            return

        cursor = self.db.cursor()
        info = cursor.execute(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
        info = info.fetchone()
        if info is None:
            sql = ('INSERT INTO guilds({}) VALUES({})').format(', '.join(str(i) for i in Tags.to_dict().values()), ', '.join('?' for i in Tags.to_dict().values()))
            val = (
                guild_id,
                True,
                time()
            )
            cursor.execute(sql, val)
            self.db.commit()
            info = cursor.execute(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
            info = info.fetchone()
            cursor.close()
            return info

    def delete_server(self, guild_id: int, commit = True):
        if guild_id in self._cache.keys():
            del self.cache[guild_id]
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM guilds WHERE guild_id = {guild_id}")
        if commit:
            self.db.commit()
        cursor.close()

    def get_server(self, guild_id: int) -> Optional[Server]:
        if guild_id not in self._cache.keys():
            cursor = self.db.cursor()
            info = cursor.execute(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
            info = info.fetchone()

            if info is None:
                info = self.create_server(guild_id)
                self._cache[guild_id] = Server(self, dict(zip(list(Tags.to_dict()), info)))
            else:
                self._cache[guild_id] = Server(self, dict(zip(list(Tags.to_dict()), info)))
            cursor.close()

        return self._cache.get(guild_id)

    def update_server(self, guild_id: int, tag: Tags, config) -> None:
        cursor = self.db.cursor()

        # checks if the server exists in the database
        info = cursor.execute(f"SELECT * FROM guilds WHERE guild_id = {guild_id}")
        info = info.fetchall()
        if info is None:
            self.client.logger.error("Error while updating server, server not found. [ID: {}]")
            return

        sql = (f'UPDATE guilds SET {tag.value} = ? WHERE guild_id = ?')
        val = (
            config, 
            guild_id
        )

        cursor.execute(sql, val)
        self.db.commit()
        cursor.close()
