import os
import pygame
import random
import sys

pygame.init()
FPS = 50
fps = 10
fenses = ["black_fense.png", "green_fense.png", "white_fense.png"]
chickens = ["black_chicken.png", 'green_chicken.png', 'white_chicken.png']
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 300, 500
screen = pygame.display.set_mode(size)
running = True
rule_group = pygame.sprite.Group()
play_group = pygame.sprite.Group()
start_button = pygame.draw.rect(screen, (0, 0, 240), (25, 130, 245, 50))
pygame.display.flip()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def terminate():
    pygame.quit()
    sys.exit()


class BackButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(rule_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = 65
        text_y = 10
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class Rule_button(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(rule_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = 5
        text_y = 7
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class Play_button(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(play_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = 65
        text_y = 7
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Fense(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        image = pygame.transform.scale(load_image(name), (300, 85))
        super().__init__(all_sprites)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.collide_mask(self, chicken):
            return True
        return self.rect.y


chicken_color = 0
chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, 113, 400)


def game_screen():
    screen = pygame.display.set_mode(size)
    running = True
    fenses = ["black_fense.png", "green_fense.png", "white_fense.png"]
    chickens = ["black_chicken.png", 'green_chicken.png', 'white_chicken.png']
    x = 125
    fox = False
    # count = 0
    chicken_color = 0
    screen.blit(load_image("game_fon.png"), (0, 0))
    chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, 113, 400)
    chicken_group = pygame.sprite.Group(chicken)
    USEREVENT = 31
    pygame.time.set_timer(USEREVENT, 12000)
    while running:
        screen.blit(load_image("game_fon.png"), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                if WIDTH > (chicken.rect[0] - 100) > 0:
                    chicken.rect[0] -= 100
            if keys_pressed[pygame.K_RIGHT]:
                if (chicken.rect[0] + 100) < WIDTH:
                    chicken.rect[0] += 100
            if event.type == USEREVENT:
                fox = True
                print("fense")
                chicken_color = random.randint(0, 2)
                random_fense = Fense(0, -185, fenses[chicken_color])
                fense_group = pygame.sprite.Group(random_fense)
                random_fense.update()
                # if random_fense.update():
                #     black_chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, 113, 400)
                fense_group.draw(screen)

        if fox:
            if random_fense.update() > 550:
                fox = False
                pygame.time.set_timer(USEREVENT, 12000)
            random_fense.update()
            fense_group.draw(screen)
            chicken.update()
            chicken_group.draw(screen)
        if fox == False:
            chicken.update()
            chicken_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
        # count += 1

    pygame.quit()


def rule_screen():
    screen = pygame.display.set_mode(size)
    running = True
    intro_text = ["Правила игры", 'Назад']
    fon = pygame.transform.scale(load_image('rule_fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    back_button = BackButton(250, 50, intro_text[1], 25, 440)
    rule_group.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_click(event.pos):
                    print("clicked")
                    back_button.kill()
                    start_screen()
                else:
                    pass
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["COLOR ROAD", "",
                  "Правила игры",
                  "Играть"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(intro_text[0], 1, (176, 226, 255))
    text_x = 30
    text_y = 30
    screen.blit(text, (text_x, text_y))
    rule_button = Rule_button(250, 50, intro_text[2], 20, 240)
    play_button = Play_button(250, 50, intro_text[3], 20, 330)
    rule_group.draw(screen)
    play_group.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rule_button.check_click(event.pos):
                    print("clicked")
                    rule_button.kill()
                    play_button.kill()
                    rule_screen()
                else:
                    pass

                if play_button.check_click(event.pos):
                    print("clicked")
                    rule_button.kill()
                    play_button.kill()
                    game_screen()
                else:
                    pass

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
