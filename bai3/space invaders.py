import pygame, os, random , time
pygame.font.init()

# Kích thước cửa sổ
width, height = 750, 750
win = pygame.display.set_mode((width, height))

# Đặt icon và tiêu đề cho cửa sổ
icon = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_ship_red_small.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")

# Tải hình ảnh
red_space_ship = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_ship_red_small.png"))
green_space_ship = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_ship_green_small.png"))
blue_space_ship = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_ship_blue_small.png"))

yellow_space_ship = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_ship_yellow.png"))  # Tàu của người chơi
red_laser = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_laser_red.png"))
green_laser = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_laser_blue.png"))
yellow_laser = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "pixel_laser_yellow.png"))

# Hình nền
BG = pygame.image.load(os.path.join(os.path.dirname(__file__),"img", "background-black.png"))

# Lớp Laser (đạn)
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (0 <= self.y <= height)

    def collision(self, obj):
        return collide(self, obj)

# Lớp Tàu (Ship)
class Ship:
    COOLDOWN = 30  # Thời gian hồi giữa các lần bắn

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# Lớp Người chơi (Player)
class Player(Ship):
    def __init__(self, x, y, health=100, point=100):
        super().__init__(x, y, health)
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0
        self.point = point

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        self.score += self.point
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))

# Lớp Kẻ thù (Enemy)
class Enemy(Ship):
    color_map = {
        "red": (red_space_ship, red_laser),
        "green": (green_space_ship, green_laser),
        "blue": (blue_space_ship, blue_laser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# Hàm phát hiện va chạm
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

# Hàm chính
def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    point = 100
    main_font = pygame.font.Font("robotomono-regular.ttf", 40)
    lost_font = pygame.font.Font("robotomono-regular.ttf", 50)

    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5

    player = Player(300, 630, point=point)

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    def redraw_window():
        win.blit(BG, (0, 0))
        lives_label = main_font.render(f"Số mạng: {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Điểm: {player.score}", 1, (255, 255, 255))

        win.blit(lives_label, (10, 10))
        win.blit(score_label, (10, 40))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            lost_label = lost_font.render("Bạn đã thua!", 1, (255, 255, 255))
            win.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(fps)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < width:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < height:
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

# Menu chính
def main_menu():
    title_font = pygame.font.Font("robotomono-regular.ttf", 70)
    run = True
    while run:
        win.blit(BG, (0, 0))
        title = title_font.render("Click để chơi", 1, (255, 255, 255))
        win.blit(title, (width / 2 - title.get_width() / 2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()
