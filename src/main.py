import os
import json
from MemberCounter import MemberCounter
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    if os.getenv('DISCORD_TOKEN') is None:
        raise FileNotFoundError('check the env file')
    else:
        shard_ids = json.loads(os.getenv('SHARD_IDS'))
        instance = MemberCounter(
            shard_count = int(os.getenv('SHARDS')),
            shard_ids = shard_ids
        )

        instance.boot(os.getenv('DISCORD_TOKEN'))
