class PauseManager:
    def __init__(self,paused = True):
        self.paused = True

    def toggle(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused