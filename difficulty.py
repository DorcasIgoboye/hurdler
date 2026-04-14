
class DifficultyManager:
    """
    Manages dynamic difficulty scaling over time for gameplay elements.

    Attributes
    ----------
    level : int
        The current difficulty level. Starts at 1 and increases periodically.
    timer : int
        A frame-based counter used to determine when to raise difficulty.

    Methods
    -------
    update():
        Increments the internal timer and increases difficulty level
        every 300 ticks (~5 seconds depending on framerate).

    scale_hurdle(hurdle):
        Scales the hurdle's velocity based on the current difficulty level.
        Applies a 5% speed increase per difficulty level to both X and Y velocity.
    """

    def __init__(self):
        self.level = 1
        self.timer = 0

    def update(self):
        self.timer += 1

        if self.timer % 3600 == 0:  # every ~60 seconds
            self.level += 1

    def scale_hurdle(self, hurdle):
        hurdle.velocityX *= (1 + self.level * 0.05)
        hurdle.velocityY *= (1 + self.level * 0.05)
