#__Thêm thư viện
import pygame
from pygame.locals import *
from pygame.sprite import Group
import random
pygame.init
pygame.font.init()
#__Title + Icon
hinh_nen = pygame.image.load('PNG/LLL.png')
hinh_nen = pygame.transform.scale(hinh_nen,(500,600))
pygame.display.set_caption('Đua xeee')
icon = pygame.image.load("PNG/Icon.png")
pygame.display.set_icon(icon)
#__Tạo cửa sổ game
width = 500
height = 600
screen_size = (width,height)
screen = pygame.display.set_mode(screen_size)
#__Đặt biến
game_state = "start_menu"
gameplay = False
gameover = False
speed = 2
score = 0
road_width = 300
vien_rong = 10
vien_cao = 50
lan_trai = 200
lan_giua = 300
lan_phai = 400
phanlan = [lan_trai,lan_giua,lan_phai]
lan_move_y=0
road = (100,0,road_width,height)
vien_trai = (90,0,vien_rong,height)
vien_phai = (400,0,vien_rong,height)
top = [0,0,0,0,0]
count = 0
#__Vị trí người chơi ban đầu
car_x = 250
car_y = 520
#__Chướng ngại vật
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 45/image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_heigth = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image,(new_width,new_heigth))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
#__Xe của người chơi
class PlayVehicle(Vehicle):
    count = 0
    def __init__(self, x, y):
        image = pygame.image.load('PNG/car.png')
        super().__init__(image,x,y)
#__Nhom doi tuong
player_group = pygame.sprite.Group()
Vehicle_group = pygame.sprite.Group()
#__Tạo Player Car
player = PlayVehicle(car_x,car_y)
player_group.add(player)
#__Load xe chướng ngại vật
image_name = ['PNG/pickup_truck.png','PNG/semi_trailer.png','PNG/Taxi.png','PNG/Van.png']
Vehicle_images = []
for name in image_name:
    image = pygame.image.load(name)
    Vehicle_images.append(image)
#__Load va cham
crash = pygame.image.load('PNG/crash.png')
carsh_rect = crash.get_rect()
#__Màu
xam_dam = (78,73,73)
gray = (100,100,100)
green = (76,208,56)
yellow = (255,232,0)
red = (200,0,0)
white = (255,255,255)
#__Background random
random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#__Cài đặt FPS
clock = pygame.time.Clock()
fps = 120
#__Start screen
def draw_start_menu():
    font = pygame.font.SysFont('arial', 36)
    title = font.render('Car Game', True, (0, 0, 0))
    start_button = font.render('S_Start', True, (0, 0, 0))
    skin_button = font.render('K_Skin', True, (0,0,0))
    hs_button = font.render('H_High Score',True,(0,0,0))
    screen.blit(title, (width/2 - title.get_width()/2, height/3.4 - title.get_height()/2))
    screen.blit(start_button, (width/2 - start_button.get_width()/2, height/2.75 + start_button.get_height()/2))
    screen.blit(hs_button, (width/2.35 - skin_button.get_width()/2, height/2 + skin_button.get_height()/2))
    pygame.display.update()
#__HighScore Screen
def draw_hs_menu():
    screen.fill((0,0,0))
    font = pygame.font.SysFont('arial',40)
    font1 = pygame.font.SysFont('arial',36)
    font2 = pygame.font.SysFont('arial',32)
    font3 = pygame.font.SysFont('arial',28)
    font4 = pygame.font.SysFont('arial',24)
    font5 = pygame.font.SysFont('arial',24)
    menu_button = font.render('M_Menu', True,(255,255,255))
    title2 = font.render('High Score Board:',True,(255,255,255))
    hs1 = font1.render('Top 1.  ' + str(top[0]),True,(255,255,255))
    hs2 = font2.render('Top 2.  ' + str(top[1]),True,(255,255,255))
    hs3 = font3.render('Top 3.  ' + str(top[2]),True,(255,255,255))
    hs4 = font4.render('Top 4.  ' + str(top[3]),True,(255,255,255))
    hs5 = font5.render('Top 5.  ' + str(top[4]),True,(255,255,255))
    screen.blit(menu_button, (width/2 - menu_button.get_width()/2, height/1.1 - menu_button.get_height()/2))
    screen.blit(title2,(width/2 - title2.get_width()/2, height/8 - title2.get_height()/2))
    screen.blit(hs1,(width/2 - hs1.get_width()/2, height/4 - hs1.get_height()/2))
    screen.blit(hs2,(width/2 - hs2.get_width()/2, height/2.5 - hs2.get_height()/2))
    screen.blit(hs3,(width/2 - hs3.get_width()/2, height/1.87 - hs3.get_height()/2))
    screen.blit(hs4,(width/2 - hs4.get_width()/2, height/1.53 - hs4.get_height()/2))
    screen.blit(hs5,(width/2 - hs5.get_width()/2, height/1.3 - hs5.get_height()/2))
    pygame.display.update()
#__Nhac nen
pygame.mixer.init(44100, -16,2,2048)
music = pygame.mixer.music.load("MP3/Bbackground.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
#__Vòng lặp game
running = True
while True:
    #Chỉnh FPS
    clock.tick(fps)
    #__Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #__Điều khiển xe:
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lan_trai:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < lan_phai-100:
                player.rect.x += 100
            elif event.key == K_UP:
                player.rect.y -= 50
            elif event.key == K_DOWN and player.rect.center[0] > 0:
                player.rect.y += 50
        #__Kiểm tra va chạm
        for vehiclee in Vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover=True
    #__Quản lí trạng thái trò chơi
    if pygame.sprite.spritecollide(player,Vehicle_group,True):
        gameover = True
        carsh_rect.center = [player.rect.center[0],player.rect.top]
    if game_state == "start_menu":
        screen.blit(hinh_nen,(0,0))
        draw_start_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            game_state = "game"
            game_over = False
        if(keys[pygame.K_h]):
            game_state = "highscore_menu"
            game_over = False
    elif game_state == "highscore_menu":
        draw_hs_menu()
        key1 = pygame.key.get_pressed()
        if key1[pygame.K_m]:
            game_state = "start_menu"
            game_over = False
    elif game_state == "game":
        #__Vẽ nền
        screen.fill(random_color)
        #__Vẽ đường chạy
        pygame.draw.rect(screen,xam_dam,road)
        #__Vẽ lề đường
        pygame.draw.rect(screen,white,vien_trai)
        pygame.draw.rect(screen,white,vien_phai)
        #__Vẽ làn đường
        lan_move_y += speed
        if lan_move_y >= vien_cao*2:
            lan_move_y=0
        for y in range(vien_cao* -2,height,vien_cao*2):
            pygame.draw.rect(screen,white,(lan_trai-10,y+lan_move_y,vien_rong,vien_cao))
            pygame.draw.rect(screen,white,(lan_phai-100,y+lan_move_y,vien_rong,vien_cao))
        #__Vẽ xe người chơi
        player_group.draw(screen)
        #__Vẽ chướng ngại vật
        if len(Vehicle_group) < 2 :
            add_vehicle = True
            for vhc in Vehicle_group:
                if vhc.rect.top < vhc.rect.height * 0.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice([lan_trai-50,lan_giua-50,lan_phai-50])
                image = random.choice(Vehicle_images)
                vhc = Vehicle(image,lane,height/-2)
                Vehicle_group.add(vhc)
        for vehicle in Vehicle_group:
            vehicle.rect.y += speed

            #__Xóa đối tượng chạy hết màn hình
            if vehicle.rect.top >= height:
                vehicle.kill()
                score+=1
                if score > 0 and score % 5 == 0:
                    speed += 1
        Vehicle_group.draw(screen)
        #__Điểm
        font = pygame.font.SysFont('arial',20)
        text = font.render('Score: ' + str(int(score)), True, white)
        text_rect = text.get_rect()
        text_rect.center=(42,40)
        screen.blit(text,text_rect)
        if gameover:
            screen.blit(crash,carsh_rect)
            pygame.draw.rect(screen,red,(0,50,width,150))
            font = pygame.font.SysFont('arial',22)
            text = font.render(f'Your Score: {int(score)}', True, white)
            text_rect = text.get_rect()
            text_rect.center=(width/2,85)
            screen.blit(text,text_rect)
            text = font.render('Game Over! Play again?', True, white)
            text_rect = text.get_rect()
            text_rect.center=(width/2,125)
            screen.blit(text,text_rect)
            text = font.render('Y_Yes    N_No    M_Menu', True, white)
            text_rect = text.get_rect()
            text_rect.center=(width/2,165)
            screen.blit(text,text_rect)
            if score > top[4]:
                top[4] = score
                top.sort(reverse=True)
        pygame.display.update()
    while gameover:
            clock.tick(fps)
            #__Set Background
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        #__Reset game
                        gameover = False
                        screen.fill(random_color)
                        score = 0
                        speed = 2
                        Vehicle_group.empty()
                        player.rect.center = [car_x,car_y]
                    elif event.key == K_n:
                        gameover = False
                        pygame.quit()
                        quit()
                    elif event.key == K_m:
                        gameover = False
                        score = 0
                        speed = 2
                        Vehicle_group.empty()
                        player.rect.center = [car_x,car_y]
                        game_state = 'start_menu'
                    elif event.key == K_h:
                        gameover = False
                        game_state = 'highscore_menu'