class CooldownVariable:
    def __init__(self, max: float):
        self.max = max
        self.timeLeft = max

    def update_cooldown(self, dt: float):
        self.timeLeft -= dt

    def ready(self) -> bool:
        if self.timeLeft <= 0:
            return True
        
    def reset(self):
        self.timeLeft = self.max

    def try_reset(self) -> bool:
        if self.ready():
            self.reset()
            return True
        return False
        
        