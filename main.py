#connecting libraries
import pygame
import sys
import random

#initialisation pygame
pygame.init()

#general parameters for game

FPS = 30

#main screen
size = (297, 596) #size main screen
screen = pygame.display.set_mode(size) #creating screen
pygame.display.set_caption("Jumppick") #name for game

#icon for game
icon = pygame.image.load("img/game_icon.png").convert()
pygame.display.set_icon(icon)

clock = pygame.time.Clock() #limitation FPS
score_counter = 0

#creating a timer for generating platforms and scoring points
game_timer = pygame.USEREVENT + 1
pygame.time.set_timer(game_timer, 1500) # 1,5 seconds

#lists for platform

#list for storage rect platforms for check collision with player
platform_rect_list = []

#list for storage rect platforms for check collision with other platforms
platform_rect_list_image = []

#image
name_game = pygame.image.load("img/Name_Game.png").convert() #name for game
name_game.set_colorkey("White") #remove white color with image

#two image for movementing backgroun
background = pygame.image.load("img/background.png").convert()
background1 = pygame.image.load("img/background.png").convert()

platform_image = pygame.image.load("img/Platform.png").convert() #image platform

#variables for main menu

#button play image and rect
button_play = (pygame.image.load("img/Button_Play.png")).convert()
button_play.set_colorkey("Red") #remove red color with image
button_play_rect = button_play.get_rect(topleft = (42, 350))

#button play image click
button_play_click = (pygame.image.load("img/Button_Play_Click.png")).convert()
button_play_click.set_colorkey("Red")

#button exit image and rect
button_exit = (pygame.image.load("img/Button_Exit.png")).convert()
button_exit.set_colorkey("Red")
button_exit_rect = button_exit.get_rect(topleft = (42, 420))

#button exit image click
button_exit_click = (pygame.image.load("img/Button_Exit_Click.png")).convert()
button_exit_click.set_colorkey("Red")

#sounds for click on button
button_click = pygame.mixer.Sound("sound/button_click.wav")
button_click.set_volume(0.1) #set volume on 0.1

#variables for gameplay

#font for display score (for function gameplay and menu_game_over)
font_current_score = pygame.font.Font(None, 40)

#sound for jump
sound_jump = pygame.mixer.Sound("sound/jump_sound.wav")
sound_jump.set_volume(0.1) #set volume on 0.1

#image score for screen
score = pygame.image.load("img/image_score.png").convert()

score.set_colorkey("White") #remove white color with image

#variables for function menu game over

game_over_sound = pygame.mixer.Sound("sound/game_over_sound.wav") #load sounds for game over
game_over_sound.set_volume(0.1) #set volume for sounds


button_again = pygame.image.load("img/Button_Again.png").convert()
button_again.set_colorkey("Red")
button_again_rect = button_again.get_rect(topleft = (42, 350))

button_again_click = pygame.image.load("img/Button_Again_Click.png").convert()
button_again_click.set_colorkey("Red")

button_menu = pygame.image.load("img/Button_Menu.png").convert()
button_menu.set_colorkey("Red")
button_menu_rect = button_again.get_rect(topleft=(42, 420))

button_menu_click = pygame.image.load("img/Button_Menu_Click.png").convert()
button_menu_click.set_colorkey("Red")

game_over = pygame.image.load("img/Game_Over.png").convert()
new_record = pygame.image.load("img/new_record.png").convert()
new_record.set_colorkey(("White"))


#functions for game

#function for generation platform, with platforms no collision
#platform_cnt - random quantity platform (2-4)
def generation_platform(platform_cnt):
    for i in range(platform_cnt):
        x = random.randint(0, 267)
        y = random.randint(-80, -60)
        el = pygame.Surface((60, 20)).get_rect(topleft=(x, y))
        # check platform with coordinates (x, y)
        # no collision with platforms from list Platform_rect_list_image
        if el.collidelist(platform_rect_list_image) == -1:
            platform_rect_list.append(pygame.Surface((60, 5)).get_rect(topleft=(x, y)))
            platform_rect_list_image.append(pygame.Surface((70, 40)).get_rect(topleft=(x, y)))


#function for main menu
def main_menu():
    running_main_menu = True
    main_menu_bg_y = 0

    #cycle main menu
    while running_main_menu:

        #draw elements on screen
        screen.blit(background, (0, main_menu_bg_y))
        screen.blit(background, (0, main_menu_bg_y - 596))
        screen.blit(name_game, (15, 70))
        screen.blit(button_play, (42, 350))
        screen.blit(button_exit, (42, 420))

        #check click on button play
        if button_play_rect.collidepoint(pygame.mouse.get_pos()):
            #draw highlighted button play
            screen.blit(button_play_click, (42, 350))
        # check click on button exit
        elif button_exit_rect.collidepoint(pygame.mouse.get_pos()):
            # draw highlighted button exit
            screen.blit(button_exit_click, (42, 420))

        #movement background
        if main_menu_bg_y == 596:
            main_menu_bg_y = 0
        else:
            main_menu_bg_y += 4

        #processing events
        for event in pygame.event.get():
            #check click cross
            if event.type == pygame.QUIT:
                running_main_menu = False #exit from cycle
                sys.exit() #exit from program

            #check click mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_cord = event.pos #get coordinates click mouse

                #check click mouse on button play
                if button_play_rect.collidepoint(mouse_cord):
                    button_click.play() #play sound click button
                    gameplay() #call function start game

                # check click mouse on button exit
                elif button_exit_rect.collidepoint(mouse_cord):
                    running_main_menu = False #exit from cycle
                    sys.exit() #exit from program

        clock.tick(FPS) #limitation FPS
        pygame.display.update() #screen update

#function gameplay
def gameplay():
    running_gameplay = True
    global score_counter  # announce global variable for scoring points
    score_counter = 0  # start value
    bg_y_gameplay = 0 # variable for movement background

    # three start platform set no random
    # create rect for three platforms for check collision with player

    Platform_1 = pygame.Surface((60, 5))
    Platform_y_1 = 70
    Platform_x_1 = 149
    Platform_rect_1 = Platform_1.get_rect(topleft=(Platform_x_1, Platform_y_1))

    Platform_2 = pygame.Surface((60, 5))
    Platform_y_2 = -20
    Platform_x_2 = 240
    Platform_rect_2 = Platform_2.get_rect(topleft=(Platform_x_2, Platform_y_2))

    Platform_3 = pygame.Surface((60, 5))
    Platform_y_3 = -50
    Platform_x_3 = 20
    Platform_rect_3 = Platform_3.get_rect(topleft=(Platform_x_3, Platform_y_3))


    # clear lists for new game
    platform_rect_list.clear()
    platform_rect_list_image.clear()

    #add first platforms in list
    platform_rect_list.append(Platform_rect_1)
    platform_rect_list.append(Platform_rect_2)
    platform_rect_list.append(Platform_rect_3)

    # player info

    # list player image
    player = [pygame.image.load("img/player/player_right.png").convert(),
                    pygame.image.load("img/player/player_left.png").convert()]
    for i in range(2):  # for all image in list remove white color
        player[i].set_colorkey(("White"))

    # start coordinates player
    player_x = 149 # - x
    player_y = 20 # - y
    player_speed = 7  # speed player when moving right or left
    jump_height = 10 # variable for check end player's jump
    is_jump = False  # flag for check jump player's
    direction = True  # flag for definition directions player

    while running_gameplay:
        #text for display current score
        #create in cycle, because need often update score
        text_num_score = font_current_score.render(f"{score_counter}", True, (107, 107, 107))

        #draw elements on screen

        #draw background
        screen.blit(background, (0, bg_y_gameplay))
        screen.blit(background, (0, bg_y_gameplay - 596))

        #draw player
        #check flag, if flag == True, then draw player left, else draw player right
        if direction:
            screen.blit(player[0], (player_x, player_y - 83))
        else:
            screen.blit(player[1], (player_x, player_y - 83))

        #draw all platforms from list Platform_rect_list


        for el in platform_rect_list:
            screen.blit(platform_image, (el))
            if el.y >= 596 + 350:
                platform_rect_list.remove(el)
            else:
                el.y += 3

        #check list not empty
        if platform_rect_list_image:
            for el in platform_rect_list_image:
                screen.blit(platform_image, (el))
                if el.y >= 596 + 350:
                    platform_rect_list_image.remove(el)
                else:
                    el.y += 3

        # draw current score
        # draw now becuse must over platform
        screen.blit(score, (-20, 555))
        screen.blit(text_num_score, (95, 565))

        # movement coordinates background
        if bg_y_gameplay == 596:
            bg_y_gameplay = 0
        else:
            bg_y_gameplay += 2

        # get player's rect for check collision with platforms
        player_rect = pygame.Surface((60, 5)).get_rect(topleft=(player_x, player_y))

        # check collision with platforms from list Platform_rect_list with check player not up screen
        if player_rect.collidelist(platform_rect_list) > -1 and player_y >= 20:
            if not is_jump: #if player not jump
                sound_jump.play() #play sound jump
                is_jump = True #set flag jump
                jump_height = 10 #set quantity player's jump

        #player's jump

        #lift's player
        if is_jump:
            if jump_height > 0:
                player_y -= (jump_height ** 2) / 1.6
            if jump_height <= 0:
                is_jump = False
            jump_height -= 1

        #if player not lift, thin he descent
        player_y += (player_speed ** 2) / 5

        # Player controller
        keys = pygame.key.get_pressed() #in variable get list all press keys
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:     #check key right press
            player_x += player_speed #movement player right
            direction = True         #set direction player right

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:      #check key left press
            player_x -= player_speed #movement player left
            direction = False        #set direction player left

        #to player no go beyond screen right or left
        #if player go beyond screen, thin dropping coordinates on x
        if player_x >= 297:
            player_x = -60
        elif player_x < -60:
            player_x = 297


        #check player lost
        #if player beyond screen down, thin game over
        if player_y >= 596 + 83: #screen size on y + player's + height
            menu_game_over() #call function game over

        # processing events
        for event in pygame.event.get():
            # check click cross
            if event.type == pygame.QUIT:
                running_main_menu = False  # exit from cycle
                sys.exit()  # exit from program

            #event's timer
            elif event.type == game_timer:
                score_counter += 15 #scoring points
                PlatformCnt = random.randint(1, 4) #generating a random number of platforms
                generation_platform(PlatformCnt) #call function generation platform

        clock.tick(FPS)  # limitation FPS
        pygame.display.update()  # screen update


#function for check new record
def check_new_record(score_counter, best_score):
    # if current score more best score
    if score_counter > best_score:
        # open in directory with game file-txt that stores best's record
        # clear old value and write current score in file
        # set flag new record
        # r+ - open file for write and read
        with open("best_score.txt", "r+") as file_best_record:
            file_best_record.truncate(0)
            file_best_record.write(str(score_counter))
            return True
    else:
        return False

#function for menu game over
def menu_game_over():
    running_menu_game_over = True
    is_new_record = False #flag for check player set new record
    global score_counter #global variable for schore

    game_over_sound.play() #play sounds game over

    #open in directory with game, file-txt that stores best record and
    # save from there num in variables best_score
    #importantly! file-txt store information in strigs-type,
    # so need conversion to int
    #r+ - open file for write and read
    with open("best_score.txt", "r+") as file_best_record:
        best_score = int(file_best_record.readline()) #readline - method read all string

    #value flag result call function check_new_record
    is_new_record = check_new_record(score_counter, best_score)

    while running_menu_game_over:

        # variable for display summary score in game over
        text_current_score = font_current_score.render(f"{score_counter}", True, (107, 107, 107))

        #draw elements on screen
        screen.blit(game_over, (0, 0)) #window game over
        screen.blit(button_again, (42, 350)) #button again
        screen.blit(button_menu, (42, 420)) #button menu
        screen.blit(score, (55, 270)) #word schore
        screen.blit(text_current_score, (170, 280)) # summary score for game

        #if flag set, draw on screen phrase new record
        if is_new_record:
            screen.blit(new_record,(45, 180))

        mous_pos = pygame.mouse.get_pos() #get position mouse

        # check click on button again
        if button_again_rect.collidepoint(mous_pos):
            # draw highlighted button again
            screen.blit(button_again_click, (42, 350))

        # check click on button menu
        elif button_menu_rect.collidepoint(mous_pos):
            # draw highlighted button menu
            screen.blit(button_menu_click, (42, 420))

        # processing events
        for event in pygame.event.get():
            # check click cross
            if event.type == pygame.QUIT:
                running_menu_game_over = False  # exit from cycle
                sys.exit()  # exit from program

            # check click mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # check click mouse on button again
                if button_again_rect.collidepoint(mous_pos):
                    button_click.play() # play sound click button
                    gameplay() #call function gameplay

                # check click mouse on button menu
                elif button_menu_rect.collidepoint(mous_pos):
                    button_click.play() # play sound click button
                    main_menu() #call function main menu


        clock.tick(FPS)  # limitation FPS
        pygame.display.update()  # screen update

main_menu() #call function main menu
pygame.quit() #quit from module pygame




