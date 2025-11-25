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

    class NodoABB:
    def __init__(self, cuenta):
        self.cuenta, self.izquierda, self.derecha = cuenta, None, None

class ArbolBinarioBusqueda:
    def __init__(self): self.raiz = None
    def insertar(self, cuenta): self.raiz = self._insertar_recursivo(self.raiz, cuenta)
    def _insertar_recursivo(self, nodo, cuenta):
        if nodo is None: return NodoABB(cuenta)
        if cuenta.numero < nodo.cuenta.numero:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, cuenta)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, cuenta)
        return nodo
    def buscar(self, numero): return self._buscar_recursivo(self.raiz, numero)
    def _buscar_recursivo(self, nodo, numero):
        if nodo is None: return None
        if nodo.cuenta.numero == numero:
            return nodo.cuenta
        if numero < nodo.cuenta.numero:
            return self._buscar_recursivo(nodo.izquierda, numero)
        else:
            return self._buscar_recursivo(nodo.derecha, numero)
        
    class Cliente:
    def __init__(self, id, nombre, dni, email, tel, pwd):
        self.id, self.nombre, self.dni, self.email, self.telefono = id, nombre, dni, email, tel
        self.password, self.cuentas = pwd, []
    def agregar_cuenta(self, c): self.cuentas.append(c)
    def get_saldo_total(self): return sum(c.saldo for c in self.cuentas)

class Cuenta:
    def __init__(self, num, saldo, cliente, tipo):
        self.numero, self.saldo, self.cliente, self.tipo = num, saldo, cliente, tipo
        self.transacciones = []
    def depositar(self, m):
        if m > 0:
            self.saldo += m
            self.transacciones.append({'tipo':'DEPOSITO','monto':m,'fecha':datetime.now().strftime("%d/%m/%Y %H:%M")})
            return True
        return False
    def retirar(self, m):
        if m > 0 and self.puede_retirar(m):
            self.saldo -= m
            self.transacciones.append({'tipo':'RETIRO','monto':m,'fecha':datetime.now().strftime("%d/%m/%Y %H:%M")})
            return True
        return False
    def puede_retirar(self, m): return m <= self.saldo
    def transferir_a(self, destino, m):
        if self.puede_retirar(m):
            self.saldo -= m
            destino.saldo += m
            self.transacciones.append({'tipo':'TRANSFER ENVIADA','monto':m,'destino':destino.numero,'fecha':datetime.now().strftime("%d/%m/%Y %H:%M")})
            destino.transacciones.append({'tipo':'TRANSFER RECIBIDA','monto':m,'origen':self.numero,'fecha':datetime.now().strftime("%d/%m/%Y %H:%M")})
            return True
        return False
    class CuentaAhorro(Cuenta):
    def __init__(self, num, saldo, cliente, tasa=0.03):
        super().__init__(num, saldo, cliente, "AHORROS")
        self.tasa_interes = tasa

class CuentaCorriente(Cuenta):
    def __init__(self, num, saldo, cliente, limite=500):
        super().__init__(num, saldo, cliente, "CORRIENTE")
        self.limite_sobregiro = limite
    def puede_retirar(self, m): return m <= (self.saldo + self.limite_sobregiro)
