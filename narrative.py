'''Adds some narration to the game'''
from game_state import State

class Narrative:

    def __init__(self):
        self.message = ""
        self.timer = 0

    def boss_defeated(self):
        messages = [
            "Users: Our data is safe!",
            "Users: You stopped the breach!",
            "Users: System integrity restored!",
            "Users: You're our last line of defense!"
        ]
        self.message = messages[min(State.level-1, len(messages)-1)]
        self.timer = 180

    def game_lost(self):
        self.message = "Users: Our data is lost..."
        self.timer = 180

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, game):
        if self.timer > 0:
            game.TextOutMiddle(self.message)