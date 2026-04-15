'''A globla level system'''
class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.boss_active = False

State = GameState()