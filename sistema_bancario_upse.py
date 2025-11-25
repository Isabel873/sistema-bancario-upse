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
class Banco:
    def _init_(self, nombre):
        self.nombre, self.clientes = nombre, []
        self.cuentas, self.cola_transacciones = ArbolBinarioBusqueda(), ColaTransacciones()
        self.pila_deshacer = Pila()
        self.pila_rehacer = Pila()
        self.contador_cuentas, self.contador_clientes, self.cliente_actual = 1000, 1, None

    def registrar_cliente(self, nom, dni, em, tel, pwd):
        cliente = Cliente(f"C{self.contador_clientes:03d}", nom, dni, em, tel, pwd)
        self.clientes.append(cliente)
        self.contador_clientes += 1
        return cliente

    def buscar_cliente_por_dni(self, dni):
        for c in self.clientes:
            if c.dni == dni: return c
        return None

    def buscar_cuenta_global(self, numero):
        return self.cuentas.buscar(numero)
def crear_cuenta_ahorro(self, cliente, saldo=0, tasa=0.03):
        self.contador_cuentas += 1
        cuenta = CuentaAhorro(self.contador_cuentas, saldo, cliente, tasa)
        self.cuentas.insertar(cuenta)
        cliente.agregar_cuenta(cuenta)
        return cuenta

    def crear_cuenta_corriente(self, cliente, saldo=0, limite=500):
        self.contador_cuentas += 1
        cuenta = CuentaCorriente(self.contador_cuentas, saldo, cliente, limite)
        self.cuentas.insertar(cuenta)
        cliente.agregar_cuenta(cuenta)
        return cuenta
def cargar_datos_demo(self):
        c1 = self.registrar_cliente("Luis Torres","0912345678","luis-torres@email.com","0991234567","1234")
        c2 = self.registrar_cliente("Valentina Ramirez","0923456789","valentina-ramirez@email.com","0992345678","1234")
        ct1 = self.crear_cuenta_ahorro(c1, 2500, 0.03)
        ct2 = self.crear_cuenta_corriente(c1, 1953, 800)
        ct3 = self.crear_cuenta_ahorro(c2, 3800, 0.025)
        ct1.depositar(500); ct1.retirar(200); ct2.depositar(300)
def registrar_accion_deshacer(self, accion):
        self.pila_deshacer.push(accion)
        self.pila_rehacer.clear()

    def deshacer(self):
        acc = self.pila_deshacer.pop()
        if not acc: return False, "Nada que deshacer"
        tipo = acc.get('tipo')
        if tipo == 'RETIRAR':
            cuenta = self.buscar_cuenta_global(acc['cuenta'])
            if cuenta:
                cuenta.depositar(acc['monto'])
self.pila_rehacer.push({'tipo':'RETIRAR','cuenta':acc['cuenta'],'monto':acc['monto']})
                return True, f"Deshacer: depósito de ${acc['monto']:.2f} en cuenta {acc['cuenta']}"
            return False, "Cuenta no encontrada para deshacer"
        elif tipo == 'DEPOSITAR':
            cuenta = self.buscar_cuenta_global(acc['cuenta'])
            if cuenta and cuenta.puede_retirar(acc['monto']):
                cuenta.retirar(acc['monto'])
self.pila_rehacer.push({'tipo':'DEPOSITAR','cuenta':acc['cuenta'],'monto':acc['monto']})
                return True, f"Deshacer: retiro de ${acc['monto']:.2f} en cuenta {acc['cuenta']}"
            return False, "No se pudo deshacer depósito (fondos insuficientes)"
        elif tipo == 'TRANSFER':
            origen_num, destino_num, monto = acc['origen'], acc['destino'], acc['monto']
            origen = self.buscar_cuenta_global(origen_num)
            destino = self.buscar_cuenta_global(destino_num)
            if destino and destino.puede_retirar(monto):
                destino.transferir_a(origen, monto)
                self.pila_rehacer.push({'tipo':'TRANSFER','origen':origen_num,'destino':destino_num,'monto':monto})
                return True, f"Deshacer: transferencia de ${monto:.2f} revertida ({destino_num}→{origen_num})"
            return False, "No se pudo deshacer transferencia (fondos insuficientes en cuenta destino)"
        return False, "Acción de deshacer no reconocida"
Commit 8: Sistema de rehacer operaciones                                                                                                                                  def rehacer(self):
        acc = self.pila_rehacer.pop()
        if not acc: return False, "Nada que rehacer"
        tipo = acc.get('tipo')
        if tipo == 'RETIRAR':
            cuenta = self.buscar_cuenta_global(acc['cuenta'])
            if cuenta and cuenta.puede_retirar(acc['monto']):
                cuenta.retirar(acc['monto'])
                self.pila_deshacer.push({'tipo':'RETIRAR','cuenta':acc['cuenta'],'monto':acc['monto']})
                return True, f"Rehacer: retiro de ${acc['monto']:.2f} en cuenta {acc['cuenta']}"
            return False, "No se pudo rehacer retiro (fondos insuficientes)"
        elif tipo == 'DEPOSITAR':
            cuenta = self.buscar_cuenta_global(acc['cuenta'])
            if cuenta:
                cuenta.depositar(acc['monto'])
                self.pila_deshacer.push({'tipo':'DEPOSITAR','cuenta':acc['cuenta'],'monto':acc['monto']})
                return True, f"Rehacer: depósito de ${acc['monto']:.2f} en cuenta {acc['cuenta']}"
            return False, "Cuenta no encontrada para rehacer"
        elif tipo == 'TRANSFER':
            origen_num, destino_num, monto = acc['origen'], acc['destino'], acc['monto']
            origen = self.buscar_cuenta_global(origen_num)
            destino = self.buscar_cuenta_global(destino_num)
            if origen and origen.puede_retirar(monto):
                origen.transferir_a(destino, monto)
                self.pila_deshacer.push({'tipo':'TRANSFER','origen':origen_num,'destino':destino_num,'monto':monto})
                return True, f"Rehacer: transferencia de ${monto:.2f} ejecutada ({origen_num}→{destino_num})"
            return False, "No se pudo rehacer transferencia (fondos insuficientes)"
        return False, "Acción de rehacer no reconocida"
