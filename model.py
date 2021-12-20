import math
import random
import colors
from colors import *

screen = pygame.display.set_mode((1024, 1024))
FPS = 30
star = False
sans = False
sans_picked_up = False
objects = [0, 0, 0]
dtstar = 0
dtsans = 0
pygame.init()


class InputBox:
    """Класс окна ввода игроком текста; x, y - координаты левого верхнего угла окна, w - ширина, h - высота"""
    def __init__(self, x, y, w, h, text=''):
        """Создание основных параметров окна"""
        self.FONT = pygame.font.Font(None, 50)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = manager.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, player_number, input_type):
        """Обработка событий, связанных с окном"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            "Если игрок щёлкнул по окну"
            if self.rect.collidepoint(event.pos):
                "Переключает активную переменную"
                self.active = not self.active
            else:
                self.active = False
            "Меняет цвет в зависимости от активности окна"
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    "Присвоение игрокам введённых имён"
                    if input_type == 'Name':
                        if player_number == 1:
                            manager.Player1.get_a_name(self.text)
                        elif player_number == 2:
                            manager.Player2.get_a_name(self.text)
                    elif input_type == 'Colour':
                        if player_number == 1:
                            manager.Player1.get_a_colour(self.text)
                        elif player_number == 2:
                            manager.Player2.get_a_colour(self.text)

                    self.text = ''
                    screen.fill((0, 0, 0))

                elif event.key == pygame.K_BACKSPACE:
                    "Убирает напечатанные символы при нажатии соответствующей клавиши"
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                "Обновление текста"
                self.txt_surface = manager.FONT.render(self.text, True, self.color)

    def update(self):
        """Удлиняет окно если текст слишком длинный"""
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        pygame.draw.polygon(screen, (0, 0, 0), [(400, 400), (1030, 400), (1030, 500), (400, 500)])
        "Отображает текст"
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        "Отображает окно"
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Big_Manager:
    """
    Класс, изменение параметров которого влечёт переключение между режимами
    игры (меню, собственно игры, паузы, положения между раундами); кроме того, на него ссылаются при необходимости
    узнать/изменить параметры объектов: Player1, Player2, field, spikes, или узнать/изменить громкости музыки и звуков.
    self.activate_sound - определяет, должен ли прозвучать звук нажатия кнопки.
    """

    def __init__(self):
        self.play = False
        self.finished = False
        self.pause = False
        self.game_over = False
        self.game_over_counter = 0
        self.stop = True
        self.not_started = True
        self.game_break = False
        self.game_break_counter = 0
        self.dt = 0
        self.options = False
        self.field = Field()
        self.Player1 = Player(400, 800)
        self.Player2 = Player(800, 800)
        self.FONT = pygame.font.Font(None, 32)


class Button:
    """Класс кнопки меню; j - координата по вертикали, name - текст внутри кнопки"""
    def __init__(self, j, name):
        self.coords1 = (400, j)
        self.coords2 = (650, j)
        self.coords3 = (650, j + 100)
        self.coords4 = (400, j + 100)
        self.text = name
        self.color = GREEN

    def pressed(self, mouse_coords, coords1, coords3):
        """Определяет, наведена ли мышь на кнопку"""

        if coords1[0] < mouse_coords[0] < coords3[0] and coords1[1] < mouse_coords[1] < coords3[1]:
            return True
        else:
            return False

    def change_color(self, mouse_coords, coords1, coords3):
        """Изменение цвета активированной кнопки"""
        if self.pressed(mouse_coords, coords1, coords3):
            self.color = BLUE
        else:
            self.color = GREEN

    def image_button(self, screen, coords1, coords2, coords3, coords4, name, color):
        """Отображение кнопки"""
        pygame.draw.polygon(screen, WHITE, [coords1, coords2, coords3, coords4], 20)
        pygame.draw.polygon(screen, color, [coords1, coords2, coords3, coords4])
        text_surf = pygame.font.Font(None, 60)
        button_text = text_surf.render(name, True, (0, 0, 0))
        screen.blit(button_text, coords1)


class StarPowerUp:
    def __init__(self):
        self.used = False
        self.xc = random.randint(200, 800)
        self.yc = random.randint(200, 800)
        self.r = 30
        self.a = math.sqrt(2 * self.r ** 2 - 2 * self.r ** 2 * math.cos(72/180 * math.pi)) * 1/2 / \
            math.sin(27 / 180 * math.pi)
        self.d = math.sqrt(self.a ** 2 + self.r ** 2 - 2 * self.r * self.a * math.cos(18 / 180 * math.pi))
        self.x1 = self.xc
        self.y1 = self.yc - self.r
        self.x2 = self.xc + self.d * math.sin(36 / 180 * math.pi)
        self.y2 = self.yc - self.d * math.cos(36 / 180 * math.pi)
        self.x3 = self.xc + self.r * math.sin(72 / 180 * math.pi)
        self.y3 = self.yc - self.r * math.cos(72 / 180 * math.pi)
        self.x4 = self.xc + self.d * math.sin(72 / 180 * math.pi)
        self.y4 = self.yc + self.d * math.cos(72 / 180 * math.pi)
        self.x5 = self.xc + self.r * math.sin(36 / 180 * math.pi)
        self.y5 = self.yc + self.r * math.cos(36 / 180 * math.pi)
        self.x6 = self.xc
        self.y6 = self.yc + self.d
        self.x7 = self.xc - self.r * math.sin(36 / 180 * math.pi)
        self.y7 = self.yc + self.r * math.cos(36 / 180 * math.pi)
        self.x8 = self.xc - self.d * math.sin(72 / 180 * math.pi)
        self.y8 = self.yc + self.d * math.cos(72 / 180 * math.pi)
        self.x9 = self.xc - self.r * math.sin(72 / 180 * math.pi)
        self.y9 = self.yc - self.r * math.cos(72 / 180 * math.pi)
        self.x10 = self.xc - self.d * math.sin(36 / 180 * math.pi)
        self.y10 = self.yc - self.d * math.cos(36 / 180 * math.pi)
        self.drawdata = [[self.x2, self.y2], [self.x3, self.y3], [self.x4, self.y4], [self.x5, self.y5],
                         [self.x6, self.y6], [self.x7, self.y7], [self.x8, self.y8], [self.x9, self.y9],
                         [self.x10, self.y10], [self.x1, self.y1]]
        self.color = [255, 255, 39]

    def pickup(self, player, dt):
        if math.sqrt((player.x - self.xc) ** 2 + (player.y - self.yc) ** 2) <= player.size + self.r and not self.used:
            player.star(dt)
            self.used = True


class Player:
    """
    Тип данных, описывающий одного из игроков
    """
    def __init__(self, xcord, ycord):
        self.invincible = False
        self.immovable = False
        self.live = True
        self.mass = 1
        self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
        self.tempcolor = 0
        self.size = 50
        self.x = xcord
        self.y = ycord
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.t = 0
        self.t0 = 0
        self.name = 'Someone'
        self.wins = 0

    def get_a_name(self, name):
        self.name = name

    def get_a_colour(self, color):
        if color == 'Red':
            self.color = colors.RED
        elif color == 'Green':
            self.color = colors.GREEN
        elif color == 'Blue':
            self.color = colors.BLUE
        elif color == 'Orange':
            self.color = colors.ORANGE
        elif color == 'White':
            self.color = colors.WHITE
        elif color == 'Random':
            self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
        else:
            self.color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]

    def restart_parameters(self, xcord, ycord):
        self.x = xcord
        self.y = ycord
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.t = 0
        self.t0 = 0

    def move(self):
        if not self.immovable:
            self.x += self.vx
            self.y += self.vy
            self.vx += self.ax
            self.vy += self.ay

    def newton(self, dt, controls, sans_controls):
        global sans_picked_up
        if not sans_picked_up:
            temp = manager.field.engagement(self.mass, int(self.x), int(self.y), dt)
            self.ax = temp[0] + controls[0]
            self.ay = temp[1] + controls[1]
        elif not self.immovable:
            self.ax = sans_controls[0] * 10
            self.ay = sans_controls[1] * 10

    def wall(self):
        if self.x - self.size < 0:
            self.vx = -self.vx * 0.6
            self.x = self.size
        if self.size + self.x > 1024:
            self.vx = -self.vx * 0.6
            self.x = 1024 - self.size
        if self.y - self.size < 0:
            self.vy = -self.vy * 0.6
            self.y = self.size
        if self.size + self.y > 1024:
            self.vy = -self.vy * 0.6
            self.y = 1024 - self.size

    def death(self):
        global spike
        self.live = not spike.penetration(self)

    def stardeath(self):
        self.live = False

    def star(self, dt=1):
        global star
        if not self.invincible:
            self.tempcolor = self.color
            self.t0 = dt
        self.invincible = True
        if not self.t:
            self.t += 10
            return
        if dt % self.t:
            self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            self.t += 10
        if dt - self.t0 >= FPS * 10:
            self.invincible = False
            self.color = self.tempcolor
            objects[0] = 0
            star = False

    def sans(self, dt):
        global sans, sans_picked_up
        if not self.immovable:
            self.t0 = dt
        self.immovable = True
        if dt - self.t0 >= FPS * 10:
            self.immovable = False
            objects[1] = 1
            sans = False
            sans_picked_up = False


class Sans:
    """
    Тип данных, отвечающий за усиление "SANS"
    """
    def __init__(self):
        self.used = False
        self.x = random.randint(200, 800)
        self.y = random.randint(200, 800)
        self.r = 80

    def pickup(self, player, dt):
        global sans_picked_up
        if math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2) <= player.size + self.r and not self.used:
            player.sans(dt)
            self.used = True
            sans_picked_up = True


class Field:
    """
    Тип данных, описывающий свойства и структуру игрового поля
    """
    def evolve(self, x, y, dt):
        if x == 511 and y > 511:
            xproj = -0.4
            yproj = 0
        if x == 511 and y < 511:
            xproj = 0.4
            yproj = 0
        if y == 511 and x < 511:
            yproj = 0.4
            xproj = 0
        if y == 511 and x > 511:
            yproj = -0.4
            xproj = 0
        if x < 511 and y < 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x < 511 and y > 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = -math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = -math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x > 511 and y < 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4
        if x > 511 and y > 511:
            rad_k = (y - 511) / (511 - x)
            force_k = (1 / rad_k)
            xproj = -math.sqrt(1 / (force_k ** 2 + 1)) * 0.4
            yproj = -math.sqrt(1 / (force_k ** 2 + 1)) * force_k * 0.4

        return(xproj * math.cos(-0.05 * dt) + yproj * math.sin(-0.05 * dt),
               -xproj * math.sin(-0.05 * dt) + yproj * math.cos(-0.05 * dt))

    def engagement(self, m, x, y, dt):
        x = round(x)
        y = round(y)
        return [self.evolve(x, y, dt)[0] / m, self.evolve(x, y, dt)[1] / m]


class Spike:
    """
    Тип данных, отвечающий за взаимодействие игроков с шипами
    """
    def __init__(self):
        self.x1 = random.randint(300, 700)
        self.a = 60
        self.x3 = self.x1 + self.a
        self.x2 = self.x1 + self.a / 2
        self.y1 = random.randint(300, 700)
        self.y3 = self.y1
        self.y2 = self.y1 - math.sin(math.pi / 3) * self.a
        self.b12 = (self.y2 + self.y1 + math.sqrt(3) * (self.x1 + self.x2)) / 2
        self.b23 = (self.y3 + self.y2 - math.sqrt(3) * (self.x2 + self.x3)) / 2

    def penetration(self, player):
        if player.invincible:
            return False
        d1 = math.sqrt((player.x - self.x1) ** 2 + (player.y - self.y1) ** 2)
        d2 = math.sqrt((player.x - self.x2) ** 2 + (player.y - self.y2) ** 2)
        d3 = math.sqrt((player.x - self.x3) ** 2 + (player.y - self.y3) ** 2)
        cos_psi1_1 = (d2 ** 2 - self.a ** 2 - d1 ** 2) / (-2 * d1 * self.a)
        cos_psi2_2 = (d3 ** 2 - self.a ** 2 - d2 ** 2) / (-2 * d2 * self.a)
        cos_psi3_3 = (d1 ** 2 - self.a ** 2 - d3 ** 2) / (-2 * d3 * self.a)
        if d1 <= player.size or d2 <= player.size or d3 <= player.size:
            return True
        if self.y1 >= player.y >= player.x * math.sqrt(3) + self.b23 and d1 * math.sqrt(1 - cos_psi1_1 ** 2) <= player.size:
            return True
        if self.y1 >= player.y >= -player.x * math.sqrt(3) + self.b12 and d2 * math.sqrt(1 - cos_psi2_2 ** 2) <= player.size:
            return True
        if self.y1 <= player.y >= player.x * math.sqrt(3) + self.b23 and player.y >= -player.x * math.sqrt(3) + self.b12 and d3 * math.sqrt(1 - cos_psi3_3 ** 2) <= player.size:
            return True
        if self.y1 >= player.y >= player.x * math.sqrt(3) + self.b23 and player.y >= -player.x * math.sqrt(3) + self.b12:
            return True
        return False


def collide(player1, player2):

    if math.sqrt((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2) <= player1.size + player2.size:
        if player1.immovable or player2.immovable:
            return
        if player1.invincible:
            player2.stardeath()
            return
        if player2.invincible:
            player1.stardeath()
            return
        m1 = player1.mass
        m2 = player2.mass
        v1x = player1.vx
        v1y = player1.vy
        v2x = player2.vx
        v2y = player2.vy
        vx_cm = (m1 * v1x + m2 * v2x) / (m1 + m2)
        vy_cm = (m1 * v1y + m2 * v2y) / (m1 + m2)
        v1x_cm = v1x - vx_cm
        v1y_cm = v1y - vy_cm
        v2x_cm = v2x - vx_cm
        v2y_cm = v2y - vy_cm
        v1x_true = -v1x_cm + vx_cm
        v1y_true = -v1y_cm + vy_cm
        v2x_true = -v2x_cm + vx_cm
        v2y_true = -v2y_cm + vy_cm
        player1.vx = v1x_true
        player1.vy = v1y_true
        player2.vx = v2x_true
        player2.vy = v2y_true


def start():
    """Создание поля, шипов, игроков в начале игры"""

    global spike
    manager.field = Field()
    spike = Spike()
    manager.Player1 = Player(400, 800)
    manager.Player2 = Player(800, 800)
    manager.Player1.wins = 0
    manager.Player2.wins = 0


def restart():
    """Создание нового поля, новых шипов и откат к начальному состоянию игроков перед новым раундом"""

    global spike, sans, sans_picked_up
    manager.field = Field()
    spike = Spike()
    sans = False
    sans_picked_up = False
    manager.Player1.restart_parameters(400, 800)
    manager.Player2.restart_parameters(800, 800)


def tick(dt, controls):
    global objects, star, dtstar, sans, dtsans

    if dtstar == FPS * 20:
        objects[0] = StarPowerUp()
        star = True
        dtstar = -FPS * 10

    if dtsans == FPS * 20:
        objects[1] = Sans()
        sans = True
        dtsans = -FPS * 10
    dt += 1
    dtstar += 1
    dtsans += 1
    collide(manager.Player1, manager.Player2)
    manager.Player1.wall()
    manager.Player2.wall()
    collide(manager.Player1, manager.Player2)
    manager.Player1.death()
    manager.Player2.death()
    collide(manager.Player1, manager.Player2)
    manager.Player1.move()
    manager.Player2.move()
    collide(manager.Player1, manager.Player2)
    if star:
        objects[0].pickup(manager.Player1, dt)
        objects[0].pickup(manager.Player2, dt)
    if manager.Player1.invincible:
        manager.Player1.star(dt)
    if manager.Player2.invincible:
        manager.Player2.star(dt)
    if sans:
        objects[1].pickup(manager.Player1, dt)
        objects[1].pickup(manager.Player2, dt)
    if manager.Player1.immovable:
        manager.Player1.sans(dt)
    if manager.Player2.immovable:
        manager.Player2.sans(dt)
    manager.Player1.death()
    manager.Player2.death()
    collide(manager.Player1, manager.Player2)
    manager.Player1.wall()
    manager.Player2.wall()
    collide(manager.Player1, manager.Player2)
    manager.Player1.newton(dt, [controls[0], controls[1]], [controls[2], controls[3]])
    manager.Player2.newton(dt, [controls[2], controls[3]], [controls[0], controls[1]])
    collide(manager.Player1, manager.Player2)
    return manager.Player1, manager.Player2, spike, manager.field, dt, objects


manager = Big_Manager()
