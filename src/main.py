from __future__ import annotations

import os
import json
from MemberCounter import MemberCounter
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    if os.getenv('DISCORD_TOKEN') is None:
        raise FileNotFoundError('check the env file')
    else:
        _shards = os.getenv('SHARD_IDS').split(",")
        shards = list(map(int, _shards)) if _shards is not None or _shards else [0]

        instance = MemberCounter(
            shard_count = int(os.getenv('SHARDS')),
            shard_ids = shards
        )

        instance.boot(os.getenv('DISCORD_TOKEN'))
