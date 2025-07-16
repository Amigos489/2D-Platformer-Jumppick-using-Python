import pygame
import random

pygame.init()

#Цвета
BLUE = (66, 170, 255)
BLACK = (0, 0, 0)



FPS = 30
running = True
size = (297, 596)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dudlik")
clock = pygame.time.Clock()
is_GameOver = False



#лист с платформами
#одновременно на экране может находиться ограниченное количество платформ, в каком-то диапазоне
#и пока платформы находятся на экране они находятся в списке, когда выходят за экран из него удаляются
#координаты x и y генерируются в определённом диапазоне
#платформы генерируются по таймеру

Platform_timer = pygame.USEREVENT + 1
pygame.time.set_timer(Platform_timer, 2000)

Platform_rect_list = [] #Список для хранения Rect платформ
#Coordinate_Platform_rect_list = [] #Список хранящий координаты плтаформ
bg_y = 0

#Функция (пока затычка), реализация главного меню
def main_menu():
    return

#Функция для генерации платформ
def Generation_platform(Platform_cnt):
    for i in range(Platform_cnt):
        x = random.randint(0, 300)
        y = random.randint(-30, -20)
        Platform_rect_list.append(pygame.Surface((60, 5)).get_rect(center = (x, y)))


#платформа
Platform = pygame.Surface((60, 20))
Platform_y = 110
Platform_x = 0

Platform1 = pygame.Surface((60, 20))
Platform1_y = 140
Platform1_x = 200


#изображения
background = pygame.image.load("img/background.png").convert() #задний фон
background1 = pygame.image.load("img/background.png").convert() #задний фон для движения
PlatformImage = pygame.image.load("img/Platform.png")


#игрок
player = [pygame.image.load("img/player/player_right.png").convert(), pygame.image.load("img/player/player_left.png").convert()]
for i in range(2):
    player[i].set_colorkey((255, 255, 255))
player_x = 200
player_y = 60
player_speed = 7
is_jump = False
jump_height = 14
direction = True

i = 0

while running:
    #обновление игры
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - 596))
    if direction:
        screen.blit(player[0], (player_x, player_y - 83))
        #screen.blit(pygame.Surface((60, 5)), (player_x, player_y))
        player_rect = pygame.Surface((60, 5)).get_rect(topleft=(player_x, player_y))
    else:
        screen.blit(player[1], (player_x, player_y - 83))
        #screen.blit(pygame.Surface((60, 5)), (player_x, player_y))
        player_rect = pygame.Surface((60, 5)).get_rect(topleft=(player_x, player_y))
    screen.blit(PlatformImage, (Platform_x, Platform_y))
    screen.blit(PlatformImage, (Platform1_x, Platform1_y))

    if Platform_rect_list:
        for el in Platform_rect_list:
            screen.blit(pygame.Surface((60, 5)), el)
            screen.blit(PlatformImage, (el.x , el[1] - 5))
            if el.y >= 596 + 300:
                Platform_rect_list.remove(el)
                print(f"Платформа {i} больше не нужна {el},)")
                i += 1
            else:
                el.y += 3



    #обработка столкновений
    if player_rect.collidelist(Platform_rect_list) > -1:
        if not is_jump:
             is_jump = True
             jump_height = 10






    if bg_y == 596:
        bg_y = 0
    else:
        bg_y += 1


    #Для столкновений
    Platform_rect = Platform.get_rect(topleft=(Platform_x, Platform_y))
    Platform1_rect = Platform1.get_rect(topleft=(Platform1_x, Platform1_y))


    Platform_y += 1
    Platform1_y += 1

    #Соприкосновение с платформой
    if Platform_rect.colliderect(player_rect) or Platform1_rect.colliderect(player_rect):
        #print("Прыжок")
        if not is_jump:
            is_jump = True
            jump_height = 10


    if is_jump:
        if jump_height > 0:
            player_y -= (jump_height ** 2) / 1.7
        if jump_height <= 0:
            is_jump = False
        jump_height -= 1

    player_y += (player_speed ** 2) / 5


    #Управление игроком
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        direction = True
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        direction = False

    if player_x >= 297:
        player_x = -60

    elif player_x < -60:
        player_x = 297



    #обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == Platform_timer:
            PlatformCnt = random.randint(1, 3)
            Generation_platform(PlatformCnt)

    if player_y >= 596 + 15 + 83:
        is_GameOver = True
        print("Игра окнончена!")
        break


    #отрисовка

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()

