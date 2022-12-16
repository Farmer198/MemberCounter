from ..EventManagerBlueprint import EventBlueprint

class Shards(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_shard_ready)
        self.manager.client.add_listener(self.on_shard_resumed)
        self.manager.client.add_listener(self.on_shard_connect)
        self.manager.client.add_listener(self.on_shard_disconnect)

    def unload(self):
        self.manager.client.remove_listener(self.on_shard_ready)
        self.manager.client.remove_listener(self.on_shard_resumed)
        self.manager.client.remove_listener(self.on_shard_connect)
        self.manager.client.remove_listener(self.on_shard_disconnect)

    async def on_shard_ready(self, shard_id):
        self.manager.client.logger.info(f'Shard Ready {shard_id + 1}\{self.manager.client.shard_count}')

    async def on_shard_resumed(self, shard_id):
        self.manager.client.logger.info(f'Shard resumed {shard_id + 1}\{self.manager.client.shard_count}')

    async def on_shard_connect(self, shard_id):
        self.manager.client.logger.info(f'Shard Connected {shard_id + 1}\{self.manager.client.shard_count}')

    async def on_shard_disconnect(self, shard_id):
        self.manager.client.logger.info(f'Shard Disconnected {shard_id + 1}\{self.manager.client.shard_count}')
