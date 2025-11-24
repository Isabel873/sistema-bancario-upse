import pygame
import sys
from datetime import datetime

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 1000, 700, 60
DARK_BLUE, BLUE, LIGHT_BLUE = (10,25,47), (41,128,185), (52,152,219)
WHITE, BLACK, GREEN, RED = (255,255,255), (0,0,0), (46,204,113), (231,76,60)
GOLD, ORANGE, PURPLE, GRAY = (241,196,15), (230,126,34), (155,89,182), (149,165,166)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sistema Bancario UPSE")
clock = pygame.time.Clock()

try:
    title_font = pygame.font.SysFont('Arial', 56, bold=True)
    header_font = pygame.font.SysFont('Arial', 40, bold=True)
    normal_font = pygame.font.SysFont('Arial', 28)
    small_font = pygame.font.SysFont('Arial', 22)
    tiny_font = pygame.font.SysFont('Arial', 18)
except:
    title_font = pygame.font.Font(None, 56)
    header_font = pygame.font.Font(None, 40)
    normal_font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)
    tiny_font = pygame.font.Font(None, 18)

class Pila:
    def __init__(self): self._elementos = []
    def push(self, e): self._elementos.append(e)
    def pop(self): return self._elementos.pop() if self._elementos else None
    def peek(self): return self._elementos[-1] if self._elementos else None
    def clear(self): self._elementos.clear()
    def esta_vacia(self): return len(self._elementos) == 0

class ColaTransacciones:
    def __init__(self): self._elementos = []
    def encolar(self, t): self._elementos.append(t)
    def desencolar(self): return self._elementos.pop(0) if self._elementos else None
    def esta_vacia(self): return len(self._elementos) == 0