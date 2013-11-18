#Test pygame script, just a basic shell of a game.

import pygame, pygame.mixer, random
black = (0, 0, 0)

pygame.init()

font = pygame.font.Font(None, 20)
score = font.render("Zero Fish", True, black)

slidesound = pygame.mixer.Sound("sliding.wav")
callsound = pygame.mixer.Sound("call.wav")

try:
	winder = pygame.joystick.Joystick(0)
exception:
	usemouse = true

winder.init()

screensize = 600

size = [1400, screensize]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Penguin Quest V.1")

done = False
speed = 10
playedslide = False 
playedcall = False
herringx = 0
herringy = 300
herringspeed = 2 
fish = 0


bg = pygame.image.load("c:\Users\Billy\desktop\python\pq\iceberg.jpg").convert()
bg = pygame.transform.scale(bg, (1400, 600))

herring = pygame.image.load("herring.png").convert_alpha()
herringright = pygame.transform.scale(herring, (50, 15))
herringleft = pygame.transform.flip(herringright, True, False)

pengo = pygame.image.load("pengstand.png").convert_alpha()

pengoregular = pygame.transform.scale(pengo, (60,100))
pengoflipped = pygame.transform.flip(pengoregular, False, True)

pengoright = pygame.image.load("pengside.png").convert_alpha()
pengoright = pygame.transform.scale(pengoright, (75, 100))
pengoleft = pygame.transform.flip(pengoright, True, False)

pengoslideright = pygame.image.load("pengslide.png").convert_alpha()
pengoslideright = pygame.transform.scale(pengoslideright, (100, 75))
pengoslideleft = pygame.transform.flip(pengoslideright, True, False)



x = 800 
y = 400 

clock = pygame.time.Clock()

while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	#Event processing above this comment
	#pos = pygame.mouse.get_pos()
	#x = pos[0] - 20 
	#y = pos[1] - 30 

	a = winder.get_axis(0)
	b = winder.get_axis(1)

	button1 = winder.get_button(0)

	if button1 == 1: 
		speed = 1
		playedcall = False
		if playedslide == False: 
			slidesound.play()
			playedslide = True
		if a > 0:
			pengo = pengoslideright
		elif a < 0:
			pengo = pengoslideleft
	elif button1 == 0:
		speed = 5 
		playedslide = False
		if a > .1:
			pengo = pengoright
		elif a < -.1:
			pengo = pengoleft
		else:   
			if playedcall == False:
				callsound.play()
				playedcall = True
			pengo = pengoregular


	x += (3*a/speed)
	y += (2*b/speed)


	herringy += random.randint(-5,5)
	herringx += herringspeed

	if herringx > 1400:
		herringx = 0
		herringy = random.randint(50, 650)

	pengorect = pengo.get_rect()
	pengorect.inflate_ip(-40, -20)
	pengorect.right = x
	pengorect.top = y

	herringrect = herringright.get_rect()
	herringrect.right = herringx
	herringrect.top = herringy

	if pengorect.colliderect(herringrect):
		fish += 1
		score = font.render(str(fish) + " fish", True, black)
		herringx = -100 


	#Game logic above this comment

	#Drawing code below this comment
	screen.blit(bg, (0,0))
	screen.blit(herringright, (herringx, herringy))
	screen.blit(pengo, (x,y))
	screen.blit(score, (10, 10))
	pygame.display.flip()

pygame.quit()
