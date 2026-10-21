import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eye Love - ASCII Animation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 12, bold=True)
title_font = pygame.font.SysFont("arial", 28, bold=True)
CHARS = "@#$%&*+=-:."
particles = []

def logo_pixel(x, y):
    r = max(abs(x), abs(y))
    outer = r < 1 and not (
        abs(x) > .75 and abs(y) > .75
        and math.hypot(x, y) > 1.13
    )
    inner = max(abs(x), abs(y)) < .76
    border = outer and not inner
    d = math.hypot(x, y)
    circle = .34 < d < .53
    dot = math.hypot(x - .55, y + .55) < .12
    return border or circle or dot

def gradient(x, y):
    t = (x + y + 2) / 4
    if t < .5:
        return (255, int(60 + t * 250), int(50 + t * 300))
    return (int(255 - (t - .5) * 170), 45, 220)

for y in range(-110, 111, 7):
    for x in range(-110, 111, 7):
        nx, ny = x / 110, y / 110
        if logo_pixel(nx, ny):
            particles.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "tx": WIDTH // 2 + x,
                "ty": HEIGHT // 2 + y - 30,
                "char": random.choice(CHARS),
                "color": gradient(nx, ny),
            })

start_time = pygame.time.get_ticks()
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    for p in particles:
        speed = min(1, dt * 3.5)
        p["x"] += (p["tx"] - p["x"]) * speed
        p["y"] += (p["ty"] - p["y"]) * speed
        glyph = font.render(p["char"], True, p["color"])
        screen.blit(glyph, (p["x"], p["y"]))

    if elapsed > 4:
        alpha = min(255, int((elapsed - 4) * 180))
        label = title_font.render("@YOUR_USERNAME", True, (255, 255, 255))
        label.set_alpha(alpha)
        screen.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150)))
    pygame.display.flip()

pygame.quit()
