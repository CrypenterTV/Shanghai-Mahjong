import pygame
import random
import time

class ParticleEffect:
    def __init__(self, x, y):

        self.particles = []
        self.start_time = time.time()
        self.duration = 0.8
        
        for i in range(15):
            self.particles.append([
                x, y, 
                random.randint(-6, 6), random.randint(-6, 6),  # Vitesse x, y
                random.randint(5, 10)
            ])

    def update(self):

        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3] 
            particle[4] -= 0.2 
        
        # Supprimer les particules trop petites
        self.particles = [p for p in self.particles if p[4] > 0]
        
        return time.time() - self.start_time < self.duration

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, (255, 200, 0), (int(particle[0]), int(particle[1])), int(particle[4]))