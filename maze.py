#создай игру "Лабиринт"!
from pygame import *
from time import sleep
win_width=700
win_height=500
window=display.set_mode((win_width,win_height))
display.set_caption("LABIRYNTH")
back=image.load('background.jpg')
back=transform.scale(back,(win_width,win_height))
clock=time.Clock()
FPS=60
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
class GameSprite(sprite.Sprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__()
		self.width = width
		self.height = height
		self.image= transform.scale(image.load(picture),(self.width,self.height)) 
		self.rect=self.image.get_rect() 
		self.rect.x=x
		self.rect.y=y
		self.speed=speed
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))
class Hero(GameSprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__(width,height,picture,x,y,speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_width:
			self.rect.x+=self.speed
		elif keys[K_UP] and self.rect.y>0:
			self.rect.y-=self.speed
		elif keys[K_DOWN] and self.rect.y+self.height<win_height:
			self.rect.y+=self.speed
class Enemy(GameSprite):
	def __init__(self, width,height,picture,x,y,speed):
		super().__init__(width,height,picture,x,y,speed)
		self.direction='left'
	def update(self):
		if self.direction=='left':
			self.rect.x-=self.speed
		elif self.direction=='right':
			self.rect.x+=self.speed
		#=====Касания стенок=======
		if self.rect.x<=0:
			self.direction='right'
		if self.rect.x+self.width>=win_width:
			self.direction='left'
class Wall(sprite.Sprite):
	def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
		super().__init__()
		self.color_1=color_1
		self.color_2=color_2
		self.color_3=color_3
		self.width = wall_width
		self.height = wall_height
		# картинка стены - прямоугольник нужных размеров и цвета
		self.image = Surface((self.width, self.height))
		self.image.fill((color_1, color_2, color_3))
		self.rect =self.image.get_rect()
		self.rect.x=wall_x
		self.rect.y=wall_y
	def draw_wall(self):
	   window.blit(self.image, (self.rect.x,self.rect.y))

treasure=GameSprite(width=50,height=50,picture='treasure.png',x=650,y=50,speed=0)
hero=Hero(width=50,height=50,picture='hero.png',x=250,y=250,speed=1)
enemy=Enemy(width=50,height=50,picture='cyborg.png',x=20,y=150,speed=1)
w1=Wall(154, 205, 50, 100, 20 , 450, 10)

kick=mixer.Sound('kick.ogg')
font.init()#Подключаем шрифты
font24=font.SysFont('Arial',24)#Задаем параметры шрифта
text_fail = font24.render("Проиграл!",True,(255,0,0))
text_win = font24.render("Победил!",True,(255,0,0))
while True:
	window.blit(back,(0,0))
	w1.draw_wall()
	treasure.reset()
	hero.reset()
	hero.update()
	enemy.reset()
	enemy.update()
	display.update()
	if sprite.collide_rect(hero,enemy) or sprite.collide_rect(hero,w1):
		window.blit(text_fail,(320,230))
		display.update()
		kick.play()
		sleep(3)
		quit()
	if sprite.collide_rect(hero,treasure):
		window.blit(text_win,(320,230))
		display.update()
		sleep(3)
		quit()

	for i in event.get():
		if i.type==QUIT:
			quit()
	clock.tick(FPS)
