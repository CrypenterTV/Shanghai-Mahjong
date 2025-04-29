import time

class ScorePopup:
    
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = 1.0
        self.text = text
        self.color = color

    def update(self):
        self.y -= 1  # Faire monter le texte vers le haut de la fenêtre
        return time.time() - self.start_time < self.duration

    def draw(self, surface, font):
        text = font.render(f"{self.text}", True, self.color)
        surface.blit(text, (self.x, self.y))
