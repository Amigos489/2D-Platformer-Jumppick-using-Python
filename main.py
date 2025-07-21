import pygame
import sys
import random

pygame.init()


#Глобальные переменные для всех функций
FPS = 30
size = (297, 596)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Only Jump")
clock = pygame.time.Clock()
is_GameOver = False

#нажат крестик
is_exit = False

#Создание таймера
Platform_timer = pygame.USEREVENT + 1
pygame.time.set_timer(Platform_timer, 1500) #1,5 сек


Platform_rect_list = [] #Список для хранения Rect платформ
Platform_rect_list_image = [] #Список хранящий координаты изображений платформ

#Функция для генерации платформ, проверяющая что платформы не соприкосаются
def Generation_platform(Platform_cnt):
    for i in range(1, Platform_cnt):
        x = random.randint(0, 297 - 60)
        y = random.randint(-60, 0)
        el = pygame.Surface((60, 20)).get_rect(topleft=(x, y))
        if len(Platform_rect_list_image) > 0:
            if el.collidelist(Platform_rect_list_image) == -1:
                print("Успешно!")
                Platform_rect_list.append(pygame.Surface((60, 5)).get_rect(topleft=(x, y)))
                Platform_rect_list_image.append(pygame.Surface((70, 30)).get_rect(topleft=(x, y)))
            else:
                print("Ошибка!")
                print("Перемекается с ", el.collidelist(Platform_rect_list_image))
        else:
            print("Добавили первый элемент в генерации")
            Platform_rect_list.append(pygame.Surface((60, 5)).get_rect(topleft=(x, y)))
            Platform_rect_list_image.append(pygame.Surface((70, 30)).get_rect(topleft=(x, y)))


#Пока костыль первые 2 платформы зараненее на экране
#платформа
Platform = pygame.Surface((60, 20))
Platform_y = 110
Platform_x = 0

Platform1 = pygame.Surface((60, 20))
Platform1_y = 140
Platform1_x = 200


#изображения
name_game = pygame.image.load("img/Name_Game1.png").convert()
name_game.set_colorkey("Red")
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
is_exit = False



#Функция, реализация главного меню
def main_menu():
    global is_exit

    #Подгрузка изображений
    button_play = (pygame.image.load("img/Button_Play.png"))
    button_play.set_colorkey("Red")
    button_play_rect = button_play.get_rect(topleft = (42, 350))

    button_exit = (pygame.image.load("img/Button_Exit.png"))
    button_exit.set_colorkey("Red")
    button_exit_rect = button_exit.get_rect(topleft = (42, 420))

    button_play_click = (pygame.image.load("img/Button_Play_Click.png"))
    button_play_click.set_colorkey("Red")

    button_exit_click = (pygame.image.load("img/Button_Exit_Click.png"))
    button_exit_click.set_colorkey("Red")

    running1 = True
    main_menu_bg_y = 0
    while running1:

        screen.blit(background, (0, main_menu_bg_y))
        screen.blit(background, (0, main_menu_bg_y - 596))
        screen.blit(name_game, (2, 70))

        screen.blit(button_play, (42, 350))
        screen.blit(button_exit, (42, 420))

        print(pygame.mouse.get_pos())
        if button_play_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_play_click, (42, 350))
        elif button_exit_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_exit_click, (42, 420))

        if main_menu_bg_y == 596:
            main_menu_bg_y = 0
        else:
            main_menu_bg_y += 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_cord = event.pos
                #print(mouse_cord)
                if button_play_rect.collidepoint(mouse_cord):
                    print("нажатие по кнопке play")
                    Gameplay()
                    #вызываю функцию начала игры
                    return
                elif button_exit_rect.collidepoint(mouse_cord):
                    print("нажатие по кнопке exit")
                    running1 = False
                    sys.exit()

        clock.tick(FPS)
        pygame.display.update()
    return


#Функция игрового процесса
def Gameplay():

    # переменная для движения заднего фона
    bg_y = 0

    Platform_rect_list.clear()
    Platform_rect_list_image.clear()

    # изображения
    name_game = pygame.image.load("img/Name_Game1.png").convert()
    name_game.set_colorkey("Red")
    background = pygame.image.load("img/background.png").convert()  # задний фон
    background1 = pygame.image.load("img/background.png").convert()  # задний фон для движения
    PlatformImage = pygame.image.load("img/Platform.png")

    # Пока костыль первые 2 платформы зараненее на экране
    # платформа
    Platform = pygame.Surface((60, 20))
    Platform_y = 110
    Platform_x = 0

    Platform1 = pygame.Surface((60, 20))
    Platform1_y = 140
    Platform1_x = 200


    # Данные игрока
    player = [pygame.image.load("img/player/player_right.png").convert(),
              pygame.image.load("img/player/player_left.png").convert()]
    for i in range(2):
        player[i].set_colorkey((255, 255, 255))
    player_x = 200
    player_y = 60
    player_speed = 7
    is_jump = False
    jump_height = 14
    direction = True
    i = 0

    running = True
    while running:
        # обновление игры
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - 596))
        if direction:
            screen.blit(player[0], (player_x, player_y - 83))
            # screen.blit(pygame.Surface((60, 5)), (player_x, player_y))
            player_rect = pygame.Surface((60, 5)).get_rect(topleft=(player_x, player_y))
        else:
            screen.blit(player[1], (player_x, player_y - 83))
            # screen.blit(pygame.Surface((60, 5)), (player_x, player_y))
            player_rect = pygame.Surface((60, 5)).get_rect(topleft=(player_x, player_y))
        screen.blit(PlatformImage, (Platform_x, Platform_y))
        screen.blit(PlatformImage, (Platform1_x, Platform1_y))

        if Platform_rect_list:
            for el in Platform_rect_list:
                # screen.blit(pygame.Surface((60, 5)), el)
                screen.blit(PlatformImage, (el.x, el[1]))
                screen.blit(pygame.Surface((60, 20)), el)
                if el.y >= 596 + 150:
                    Platform_rect_list.remove(el)
                    print(f"Платформа {i} больше не нужна {el},)")
                    i += 1
                else:
                    el.y += 3

        # Господи пожалуйста помоги мне пусть оно заработает
        if Platform_rect_list_image:
            for el in Platform_rect_list_image:
                # screen.blit(pygame.Surface((60, 5)), el)
                screen.blit(PlatformImage, (el.x, el[1]))
                # screen.blit(pygame.Surface((60, 20)), el)
                if el.y >= 596 + 150:
                    Platform_rect_list_image.remove(el)
                    print(f"Платформа {i} больше не нужна {el},)")
                    i += 1
                else:
                    el.y += 3

        # обработка столкновений
        if player_rect.collidelist(Platform_rect_list) > -1:
            if not is_jump:
                is_jump = True
                jump_height = 10

        if bg_y == 596:
            bg_y = 0
        else:
            bg_y += 1

        # Для столкновений
        Platform_rect = Platform.get_rect(topleft=(Platform_x, Platform_y))
        Platform1_rect = Platform1.get_rect(topleft=(Platform1_x, Platform1_y))

        Platform_y += 1
        Platform1_y += 1

        # Соприкосновение с платформой
        if Platform_rect.colliderect(player_rect) or Platform1_rect.colliderect(player_rect):
            # print("Прыжок")
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

        # Управление игроком
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

        if player_y >= 596 + 15 + 83:
            is_GameOver = True
            print("Игра окнончена!")
            Menu_GameOver() #Если игрок проиграл, то вызываестя меню проигрыша
            break

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == Platform_timer:
                PlatformCnt = random.randint(2, 4)
                Generation_platform(PlatformCnt)

        # отрисовка

        clock.tick(FPS)
        pygame.display.flip()


#Функция для отображения проигрыша
def Menu_GameOver():

    button_again = pygame.image.load("img/Button_Again.png")
    button_again.set_colorkey("Red")
    button_again_rect = button_again.get_rect(topleft = (42, 350))

    button_again_click = pygame.image.load("img/Button_Again_Click.png")
    button_again_click.set_colorkey("Red")



    button_menu = pygame.image.load("img/Button_Menu.png")
    button_menu.set_colorkey("Red")
    button_menu_rect = button_again.get_rect(topleft=(42, 420))

    button_menu_click = pygame.image.load("img/Button_Menu_Click.png")
    button_menu_click.set_colorkey("Red")

    game_over = pygame.image.load("img/Game_Over.png")

    running2 = True

    while running2:
        screen.blit(game_over, (0, 0))
        screen.blit(button_again, (42, 350))
        screen.blit(button_menu, (42, 420))

        mous_pos = pygame.mouse.get_pos()
        if button_again_rect.collidepoint(mous_pos):
            print("Навели курсор на кнопку снова")
            screen.blit(button_again_click, (42, 350))

        elif button_menu_rect.collidepoint(mous_pos):
            print("Навели курсор на кнопку меню")
            screen.blit(button_menu_click, (42, 420))

        #Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_again_rect.collidepoint(mous_pos):
                    print("Нажали на кнопку снова")
                    Gameplay()

                elif button_menu_rect.collidepoint(mous_pos):
                    print("Нажали на кнопку меню")
                    main_menu()

        clock.tick(FPS)
        pygame.display.update()

main_menu()
pygame.quit()




