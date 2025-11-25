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
class Button:
    def __init__(self, x, y, w, h, text, color=BLUE, hover=LIGHT_BLUE, tc=WHITE):
        self.rect, self.text, self.color, self.hover_color, self.text_color = pygame.Rect(x,y,w,h), text, color, hover, tc
        self.is_hovered = False
    def draw(self, surf):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=15)
        pygame.draw.rect(surf, WHITE, self.rect, 3, border_radius=15)
        ts = normal_font.render(self.text, True, self.text_color)
        surf.blit(ts, ts.get_rect(center=self.rect.center))
    def check_hover(self, pos): self.is_hovered = self.rect.collidepoint(pos); return self.is_hovered
    def is_clicked(self, pos, event): return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pos)

class InputBox:
    def __init__(self, x, y, w, h, label='', is_pwd=False):
        self.rect, self.label, self.text, self.is_password, self.active = pygame.Rect(x,y,w,h), label, '', is_pwd, False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and len(self.text) < 40: self.text += event.unicode
    def draw(self, surf):
        ls = small_font.render(self.label, True, WHITE)
        surf.blit(ls, (self.rect.x, self.rect.y-30))
        color = LIGHT_BLUE if self.active else GRAY
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=8)
        dt = '•'*len(self.text) if self.is_password else self.text
        ts = normal_font.render(dt, True, BLACK)
        surf.blit(ts, (self.rect.x+10, self.rect.y+8))

def draw_gradient_bg(surf):
    for y in range(SCREEN_HEIGHT):
        cv = int(10+(y/SCREEN_HEIGHT)*40)
        pygame.draw.line(surf, (cv,cv//2,cv+20), (0,y), (SCREEN_WIDTH,y))
Commit 10: Clase BancoApp - Inicialización y gestión de login class BancoApp:
    def __init__(self):
        self.banco = Banco("UPSE")
        self.current_screen, self.input_boxes, self.buttons = "welcome", {}, {}
        self.message, self.message_color = "", GREEN
        self.selected_account, self.selected_dest_account, self.amount_input = None, None, None

    def handle_login(self):
        cedula, pwd = self.input_boxes['cedula'].text, self.input_boxes['password'].text
        c = self.banco.buscar_cliente_por_dni(cedula)
        if c and c.password == pwd:
            self.banco.cliente_actual = c
            self.current_screen, self.message, self.message_color = "main_menu", "¡Bienvenido!", GREEN
        else:
            self.message, self.message_color = "Cédula de identidad o contraseña incorrectos", RED
Commit 11: Pantallas de bienvenida y login                                                                                 def draw_welcome_screen(self):
        draw_gradient_bg(screen)
        title = title_font.render("BANCO UPSE", True, GOLD)
        tr = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        pygame.draw.rect(screen, (0,0,0,100), tr.inflate(40,20), border_radius=20)
        screen.blit(title, tr)
        st = header_font.render("Sistema de Gestión Bancaria", True, WHITE)
        screen.blit(st, (SCREEN_WIDTH//2-st.get_width()//2, 220))
        bl = Button(SCREEN_WIDTH//2-150, 350, 300, 70, "INICIAR SESIÓN", GREEN, LIGHT_BLUE)
        bd = Button(SCREEN_WIDTH//2-150, 440, 300, 70, "VER DEMO", ORANGE, GOLD)
        bl.check_hover(pygame.mouse.get_pos()); bd.check_hover(pygame.mouse.get_pos())
        bl.draw(screen); bd.draw(screen)
        self.buttons = {'login':bl, 'demo':bd}
        ft = small_font.render("Python & Pygame | UPSE 2024", True, GRAY)
        screen.blit(ft, (SCREEN_WIDTH//2-ft.get_width()//2, 650))

    def draw_login_screen(self):
        draw_gradient_bg(screen)
        title = header_font.render("INICIAR SESIÓN", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 80))
        if 'cedula' not in self.input_boxes:
            self.input_boxes['cedula'] = InputBox(SCREEN_WIDTH//2-150, 200, 300, 50, "Cédula de identidad")
            self.input_boxes['password'] = InputBox(SCREEN_WIDTH//2-150, 300, 300, 50, "Contraseña", True)
        for box in self.input_boxes.values(): box.draw(screen)
        be = Button(SCREEN_WIDTH//2-150, 400, 300, 60, "ENTRAR", GREEN, LIGHT_BLUE)
        bb = Button(SCREEN_WIDTH//2-150, 480, 300, 50, "VOLVER", RED, ORANGE)
        be.check_hover(pygame.mouse.get_pos()); bb.check_hover(pygame.mouse.get_pos())
        be.draw(screen); bb.draw(screen)
        self.buttons = {'entrar':be, 'back':bb}
        if self.message:
            msg = normal_font.render(self.message, True, self.message_color)
            screen.blit(msg, (SCREEN_WIDTH//2-msg.get_width()//2, 560))
        di = small_font.render("Demo: Cédula=0912345678 | Pass=1234", True, PURPLE)
        screen.blit(di, (SCREEN_WIDTH//2-di.get_width()//2, 620))
Commit 12: Menú principal y pantalla de cuentas                                                                   def draw_main_menu(self):
        draw_gradient_bg(screen)
        c = self.banco.cliente_actual
        pygame.draw.rect(screen, BLUE, (0,0,SCREEN_WIDTH,150))
        w = header_font.render(f"Bienvenido, {c.nombre}", True, WHITE)
        screen.blit(w, (50,30))
        i1 = small_font.render(f"ID: {c.id} | Cédula: {c.dni}", True, GOLD)
        screen.blit(i1, (50,80))
        st = normal_font.render(f"Saldo Total: ${c.get_saldo_total():.2f}", True, GREEN)
        screen.blit(st, (50,110))
        opts = [("Ver Mis Cuentas","accounts",GREEN),("Realizar Depósito","deposit",BLUE),
                ("Realizar Retiro","withdraw",ORANGE),("Transferir","transfer",PURPLE),
                ("Historial","history",LIGHT_BLUE),("Cerrar Sesión","logout",RED)]
        y, self.buttons = 200, {}
        for txt, key, col in opts:
            btn = Button(SCREEN_WIDTH//2-200, y, 400, 60, txt, col, LIGHT_BLUE)
            btn.check_hover(pygame.mouse.get_pos()); btn.draw(screen)
            self.buttons[key] = btn; y += 75
        b_undo = Button(SCREEN_WIDTH-220, 30, 190, 40, "DESHACER", ORANGE, GOLD)
        b_redo = Button(SCREEN_WIDTH-220, 80, 190, 40, "REHACER", PURPLE, LIGHT_BLUE)
        b_undo.check_hover(pygame.mouse.get_pos()); b_redo.check_hover(pygame.mouse.get_pos())
        b_undo.draw(screen); b_redo.draw(screen)
        self.buttons['undo'] = b_undo; self.buttons['redo'] = b_redo
        if self.message:
            msg = small_font.render(self.message, True, self.message_color)
            screen.blit(msg, (SCREEN_WIDTH//2-msg.get_width()//2, 670))

    def draw_accounts_screen(self):
        draw_gradient_bg(screen)
        title = header_font.render("MIS CUENTAS", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 40))
        c, y = self.banco.cliente_actual, 120
        for cuenta in c.cuentas:
            cr = pygame.Rect(150, y, 700, 120)
            col = GREEN if cuenta.tipo=="AHORROS" else BLUE
            pygame.draw.rect(screen, col, cr, border_radius=15)
            pygame.draw.rect(screen, WHITE, cr, 3, border_radius=15)
            tt = normal_font.render(f"Cuenta {cuenta.tipo}", True, WHITE)
            screen.blit(tt, (180, y+20))
            nt = small_font.render(f"N°: {cuenta.numero}", True, WHITE)
            screen.blit(nt, (180, y+55))
            trt = tiny_font.render(f"Transacciones: {len(cuenta.transacciones)}", True, WHITE)
            screen.blit(trt, (180, y+85))
            st = header_font.render(f"${cuenta.saldo:.2f}", True, GOLD)
            screen.blit(st, (550, y+35))
            y += 140
        tr = pygame.Rect(150, y, 700, 80)
        pygame.draw.rect(screen, PURPLE, tr, border_radius=15)
        pygame.draw.rect(screen, WHITE, tr, 3, border_radius=15)
        tt = header_font.render(f"SALDO TOTAL: ${c.get_saldo_total():.2f}", True, GOLD)
        screen.blit(tt, (tr.centerx-tt.get_width()//2, y+25))
        bb = Button(SCREEN_WIDTH//2-150, 620, 300, 50, "VOLVER AL MENÚ", BLUE, LIGHT_BLUE)
        bb.check_hover(pygame.mouse.get_pos()); bb.draw(screen)
        self.buttons = {'back':bb}
def handle_deposit(self):
        if self.amount_input and self.selected_account is not None:
            try:
                m = float(self.amount_input.text)
                if m > 0:
                    cuenta = self.banco.cliente_actual.cuentas[self.selected_account]
                    if cuenta.depositar(m):
                        self.banco.registrar_accion_deshacer({'tipo':'DEPOSITAR','cuenta':cuenta.numero,'monto':m})
                        self.message, self.message_color = f"¡Depósito de ${m:.2f} exitoso!", GREEN
                        self.amount_input.text, self.selected_account, self.amount_input = "", None, None
                else:
                    self.message, self.message_color = "Monto debe ser mayor a 0", RED
            except:
                self.message, self.message_color = "Ingrese un monto válido", RED

    def draw_deposit_screen(self):
        draw_gradient_bg(screen)
        title = header_font.render("REALIZAR DEPÓSITO", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 50))
        c, y, self.buttons = self.banco.cliente_actual, 150, {}
        st = normal_font.render("Seleccione una cuenta:", True, WHITE)
        screen.blit(st, (SCREEN_WIDTH//2-st.get_width()//2, 120))
        for i, cuenta in enumerate(c.cuentas):
            btn = Button(SCREEN_WIDTH//2-200, y, 400, 60, f"{cuenta.tipo} N°{cuenta.numero} ${cuenta.saldo:.2f}",
                        GREEN if cuenta.tipo=="AHORROS" else BLUE, LIGHT_BLUE)
            btn.check_hover(pygame.mouse.get_pos()); btn.draw(screen)
            self.buttons[f'cuenta_{i}'] = btn; y += 75
        if self.selected_account is not None:
            if self.amount_input is None:
                self.amount_input = InputBox(SCREEN_WIDTH//2-150, y+20, 300, 50, "Monto a depositar")
            self.amount_input.draw(screen)
            bd = Button(SCREEN_WIDTH//2-150, y+100, 300, 60, "DEPOSITAR", GREEN, LIGHT_BLUE)
            bd.check_hover(pygame.mouse.get_pos()); bd.draw(screen)
            self.buttons['confirm'] = bd
        bb = Button(SCREEN_WIDTH//2-150, 620, 300, 50, "VOLVER", RED, ORANGE)
        bb.check_hover(pygame.mouse.get_pos()); bb.draw(screen)
        self.buttons['back'] = bb
        if self.message:
            msg = normal_font.render(self.message, True, self.message_color)
            screen.blit(msg, (SCREEN_WIDTH//2-msg.get_width()//2, 580))
def handle_withdraw(self):
        if self.amount_input and self.selected_account is not None:
            try:
                m = float(self.amount_input.text)
                cuenta = self.banco.cliente_actual.cuentas[self.selected_account]
                if cuenta.retirar(m):
                    self.banco.registrar_accion_deshacer({'tipo':'RETIRAR','cuenta':cuenta.numero,'monto':m})
                    self.message, self.message_color = f"¡Retiro de ${m:.2f} exitoso!", GREEN
                    self.amount_input.text, self.selected_account, self.amount_input = "", None, None
                else:
                    self.message, self.message_color = "Saldo insuficiente", RED
            except:
                self.message, self.message_color = "Ingrese un monto válido", RED

    def draw_withdraw_screen(self):
        draw_gradient_bg(screen)
        title = header_font.render("REALIZAR RETIRO", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2, 50))
        c, y, self.buttons = self.banco.cliente_actual, 150, {}
        st = normal_font.render("Seleccione una cuenta:", True, WHITE)
        screen.blit(st, (SCREEN_WIDTH//2-st.get_width()//2, 120))
        for i, cuenta in enumerate(c.cuentas):
            btn = Button(SCREEN_WIDTH//2-200, y, 400, 60, f"{cuenta.tipo} N°{cuenta.numero} ${cuenta.saldo:.2f}",
                        GREEN if cuenta.tipo=="AHORROS" else BLUE, LIGHT_BLUE)
            btn.check_hover(pygame.mouse.get_pos()); btn.draw(screen)
            self.buttons[f'cuenta_{i}'] = btn; y += 75
        if self.selected_account is not None:
            if self.amount_input is None:
                self.amount_input = InputBox(SCREEN_WIDTH//2-150, y+20, 300, 50, "Monto a retirar")
            self.amount_input.draw(screen)
            bw = Button(SCREEN_WIDTH//2-150, y+100, 300, 60, "RETIRAR", ORANGE, GOLD)
            bw.check_hover(pygame.mouse.get_pos()); bw.draw(screen)
            self.buttons['confirm'] = bw
        bb = Button(SCREEN_WIDTH//2-150, 620, 300, 50, "VOLVER", RED, ORANGE)
        bb.check_hover(pygame.mouse.get_pos()); bb.draw(screen)
        self.buttons['back'] = bb
        if self.message:
            msg = normal_font.render(self.message, True, self.message_color)
            screen.blit(msg, (SCREEN_WIDTH//2-msg.get_width()//2, 580))