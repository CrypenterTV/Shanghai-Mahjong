import time

class ScorePopup:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.start_time = time.time()
        self.duration = 1.0

    def update(self):
        self.y -= 1  # Faire monter le texte
        return time.time() - self.start_time < self.duration

    def draw(self, surface, font):
        text = font.render(f"+{self.score}", True, (255, 255, 0))
        surface.blit(text, (self.x, self.y))