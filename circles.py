# Circles
#
# Author: Thomas Hangstoerfer
# License: see LICENSE file
#
# https://developer.akamai.com/blog/2017/06/21/building-virtual-python-environment/
#
# Export requirements to a file:
# pip freeze > requirements.txt

# After cloning the repo, install requirements in virtualenv:
# virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt


import sys
import pygame
import pygame.freetype
from math import sin, cos, radians

pygame.init()

size = width, height = 800, 640
BLUE  = (  0,   0, 255)
RED   = (255,   0, 0)
GREEN = (  0, 255, 0)
BLACK = (  0,   0, 0)

screen = pygame.display.set_mode(size)

ticks = pygame.time.get_ticks()

clck = pygame.time.Clock()

pygame.display.set_caption('Circles')

textsurface = pygame.Surface((200, 70))
textsurface.fill((0, 0, 0))
GAME_FONT = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 10)
GAME_FONT.render_to(textsurface, (0, 0 * (GAME_FONT.size + 2)), "l = show lines", (100, 155, 100))
GAME_FONT.render_to(textsurface, (0, 1 * (GAME_FONT.size + 2)), "r = reset", (100, 155, 100))
GAME_FONT.render_to(textsurface, (0, 2 * (GAME_FONT.size + 2)), "+ = more circles", (100, 155, 100))
GAME_FONT.render_to(textsurface, (0, 3 * (GAME_FONT.size + 2)), "- = less circles", (100, 155, 100))
GAME_FONT.render_to(textsurface, (0, 4 * (GAME_FONT.size + 2)), "select circle with cursor-keys", (100, 155, 100))
GAME_FONT.render_to(textsurface, (0, 5 * (GAME_FONT.size + 2)), "page-up/-down to change frequency", (100, 155, 100))


fps = 50
dt = 0
radius = 30
angle = radians(0)
x = 200
y = 50
show_lines = 0
show_circle_count = 1
selected_circle_x = -1
selected_circle_y = -1


class Circle:

    def __init__(self, freq, color):
        self.freq = freq
        self.color = color
        self.width = 3
        self.angle = radians(0)
        self.x = 0
        self.y = 0
        self.trace = []

    def draw(self, screen, orbit_center_x, orbit_center_y):
        for pos in self.trace:
            screen.set_at(pos, self.color)

        self.angle = self.angle + self.freq
        theta = radians(self.angle)
        self.x = orbit_center_x + radius * cos(theta)
        self.y = orbit_center_y + radius * sin(theta)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.width)

        self.trace.append((int(self.x), int(self.y)))
        if len(self.trace) > 1000*(1/self.freq):
            del self.trace[0]


circleDistance = 100
circleOffsetX = 50
circleOffsetY = 50
circlesX = []
circlesY = []

circlesX.append(Circle(1, RED))
circlesX.append(Circle(2, GREEN))
circlesX.append(Circle(4, BLUE))
circlesX.append(Circle(8, (150, 50, 250)))
circlesX.append(Circle(16, (150, 50, 250)))

circlesY.append(Circle(0.5, (255, 0, 255)))
circlesY.append(Circle(1, (255, 255, 0)))
circlesY.append(Circle(2, (0, 255, 255)))
circlesY.append(Circle(5, (50, 155, 255)))
circlesY.append(Circle(10, (50, 155, 255)))

while True:

    screen.fill(BLACK)
    screen.blit(textsurface, (width-textsurface.get_width(), height-textsurface.get_height()))
    # print("selected_circle_x = %i selected_circle_y = %i" % (selected_circle_x, selected_circle_y))

    for event in pygame.event.get():
        print('event: ', event)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print('Q')
                sys.exit()
            if event.key == pygame.K_r:
                for i in range(len(circlesX)):
                    circlesX[i].trace = []
                    circlesX[i].angle = radians(0)
                for i in range(len(circlesY)):
                    circlesY[i].trace = []
                    circlesY[i].angle = radians(0)
                selected_circle_x = -1
                selected_circle_y = -1
            if event.key == pygame.K_l:
                show_lines = not show_lines
            if show_circle_count < 5 and (event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS):
                show_circle_count += 1
            if show_circle_count > 1 and (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS):
                show_circle_count -= 1
                if show_circle_count+1 > max(selected_circle_x, selected_circle_y):
                    selected_circle_x = -1
                    selected_circle_y = -1
            if event.key == pygame.K_LEFT:
                if selected_circle_x > 0:
                    selected_circle_x -= 1
                    selected_circle_y = -1
                else:
                    selected_circle_x = -1
                    selected_circle_y = -1
            if event.key == pygame.K_RIGHT:
                if selected_circle_x < show_circle_count-1:
                    selected_circle_x += 1
                    selected_circle_y = -1
            if event.key == pygame.K_UP:
                if selected_circle_y > 0:
                    selected_circle_y -= 1
                    selected_circle_x = -1
                else:
                    selected_circle_x = -1
                    selected_circle_y = -1
            if event.key == pygame.K_DOWN:
                if selected_circle_y < show_circle_count - 1:
                    selected_circle_y += 1
                    selected_circle_x = -1
            if event.key == pygame.K_PAGEUP:
                delta = 0.1
                if event.mod & pygame.KMOD_SHIFT:
                    delta = 1.0
                if selected_circle_x >= 0:
                    circlesX[selected_circle_x].freq += delta
                if selected_circle_y >= 0:
                    circlesY[selected_circle_y].freq += delta
            if event.key == pygame.K_PAGEDOWN:
                delta = 0.1
                if event.mod & pygame.KMOD_SHIFT:
                    delta = 1.0
                if selected_circle_x >= 0:
                    if circlesX[selected_circle_x].freq > delta:
                        circlesX[selected_circle_x].freq -= delta
                    else:
                        circlesX[selected_circle_x].freq = 0.0001
                if selected_circle_y >= 0:
                    if circlesY[selected_circle_y].freq > delta:
                        circlesY[selected_circle_y].freq -= delta
                    else:
                        circlesY[selected_circle_y].freq = 0.0001

    if pygame.time.get_ticks() - ticks > 240:
        ticks = pygame.time.get_ticks()

    if selected_circle_x >= 0 or selected_circle_y >= 0:
        rectX = circleOffsetX + ((selected_circle_x+1) * circleDistance) - radius
        rectY = circleOffsetY + ((selected_circle_y+1) * circleDistance) - radius
        pygame.draw.rect(screen, (100, 100, 100), (rectX-5, rectY-5, (radius*2)+10, (radius*2)+10), 1)

    for i in range(min(len(circlesX), show_circle_count)):
        circlesX[i].draw(screen, circleOffsetX + circleDistance + (i * circleDistance), circleOffsetY)
        if selected_circle_x >= 0 or selected_circle_y >= 0:
            GAME_FONT.render_to(screen, (circleOffsetX + circleDistance + (i * circleDistance), circleOffsetY),
                            "%.1f" % circlesX[i].freq, (100, 155, 100))
        if show_lines:
            pygame.draw.line(screen, circlesX[i].color, (circlesX[i].x, 0), (circlesX[i].x, height))

    for i in range(min(len(circlesY), show_circle_count)):
        circlesY[i].draw(screen, circleOffsetX, circleOffsetY + circleDistance + (i * circleDistance))
        if selected_circle_x >= 0 or selected_circle_y >= 0:
            GAME_FONT.render_to(screen, (circleOffsetX, circleOffsetY + circleDistance + (i * circleDistance)),
                            "%.1f" % circlesY[i].freq, (100, 155, 100))
        if show_lines:
            pygame.draw.line(screen, circlesY[i].color, (0, circlesY[i].y), (width, circlesY[i].y))

    for u in range(min(len(circlesX), show_circle_count)):
        for v in range(min(len(circlesY), show_circle_count)):
            min_count = min(len(circlesX[u].trace), len(circlesY[v].trace))
            mix_color = ((circlesX[u].color[0]+circlesY[v].color[0])/2,
                         (circlesX[u].color[1]+circlesY[v].color[1])/2,
                         (circlesX[u].color[2]+circlesY[v].color[2])/2)
            for i in range(min_count):
                x = circlesX[u].trace[len(circlesX[u].trace)-1-i][0]
                y = circlesY[v].trace[len(circlesY[v].trace)-1-i][1]
                if i == 0:
                    screen.set_at((x, y), mix_color)
                else:
                    x1 = circlesX[u].trace[len(circlesX[u].trace) - i][0]
                    y1 = circlesY[v].trace[len(circlesY[v].trace) - i][1]
                    mix_color = (max(min((circlesX[u].color[0] + circlesY[v].color[0]) / 2 - (min_count-i), 255), 0),
                                 max(min((circlesX[u].color[1] + circlesY[v].color[1]) / 2 - (min_count-i), 255), 0),
                                 max(min((circlesX[u].color[2] + circlesY[v].color[2]) / 2 - (min_count-i), 255), 0))
                    pygame.draw.line(screen, mix_color, (x, y), (x1, y1), 1)
            pygame.draw.circle(screen, (255, 255, 255), (int(circlesX[u].x), int(circlesY[v].y)), 3)

    pygame.display.flip()

    dt = clck.tick(fps)  # waste time to reach fps

