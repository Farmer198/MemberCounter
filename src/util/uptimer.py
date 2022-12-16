import time

class Uptimer:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.starttime: float = 0

    @property
    def uptime(self) -> int:
        if self.starttime == 0:
            return 0
        return int(time.time() - self.starttime)

    def start(self):
        self.starttime = time.time()
