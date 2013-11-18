#Test pygame script, just a basic shell of a game.
#  Import modules that I need
import pygame, pygame.mixer, random, os.path 

#Define the color black for font usage
black = (0, 0, 0)

#Initialize pygame
pygame.init()

#Setup the pyinstaller resource path detection.  Hugely simplifies the build
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = "."
	return os.path.join(base_path, relative_path)


#Initialize the font resource
font = pygame.font.Font(resource_path("BUBBLEBATH.ttf"), 30)
msgfont = pygame.font.Font(resource_path("BUBBLEBATH.ttf"), 30)

#Set the score to it's initial value
score = font.render("Zero Fish", True, black)

#Import the sounds
slidesound = pygame.mixer.Sound(resource_path("sliding.wav"))
callsound = pygame.mixer.Sound(resource_path("call.wav"))


#Test for the control device, initialize if joystick found
try:
	winder = pygame.joystick.Joystick(0)
	usejoystick = True
	winder.init()
except Exception:
	usejoystick = False

#Setup the start text
if usejoystick == True:
	msg = "You have a joystick use it to"
	msg1 = "control the Penguin to catch fish"
	msg2 = "button 1 will make the penguin slide"
else:
	msg = "Use the mouse to control" 
	msg1 = "the penguin and catch herring"
	msg2 = "left click will make the penguin slide"

startmsg = font.render(msg, True, black)
startmsg1 = font.render(msg1, True, black)
startmsg2 = font.render(msg2, True, black)

warnmsg = font.render("As you catch more fish", True, black)
warnmsg1 = font.render("they become scared and", True, black)
warnmsg2 = font.render("swim faster and more erratically", True, black)

#set the screen height
screensize = 600

#setup the screen (I hardcoded the screen width)
size = [1400, screensize]
screen = pygame.display.set_mode(size)

#Set the message at the top of the scrren
pygame.display.set_caption("Penguin Quest V.1.3")

#Initialize a bunch of the values
done = False
speed = 10
playedslide = False 
playedcall = False
herringx = 0
herringy = 300
herringspeed = 2 
herringspazlow = -5
herringspazhigh = 5
fish = 0


#Bring in my image resources and scale them to match the game's needed size
bg = pygame.image.load(resource_path("iceberg.jpg")).convert()
bg = pygame.transform.scale(bg, (1400, 600))

herring = pygame.image.load(resource_path("herring.png")).convert_alpha()
herringright = pygame.transform.scale(herring, (50, 15))
herringleft = pygame.transform.flip(herringright, True, False)

pengo = pygame.image.load(resource_path("pengstand.png")).convert_alpha()

pengoregular = pygame.transform.scale(pengo, (60,100))
pengoflipped = pygame.transform.flip(pengoregular, False, True)

pengoright = pygame.image.load(resource_path("pengside.png")).convert_alpha()
pengoright = pygame.transform.scale(pengoright, (75, 100))
pengoleft = pygame.transform.flip(pengoright, True, False)

pengoslideright = pygame.image.load(resource_path("pengslide.png")).convert_alpha()
pengoslideright = pygame.transform.scale(pengoslideright, (100, 75))
pengoslideleft = pygame.transform.flip(pengoslideright, True, False)


#Set the start position of the penguin
x = 800 
y = 400 

#Initialize the clock
clock = pygame.time.Clock()

#show the start message
screen.blit(bg, (0,0))
screen.blit(startmsg, (300,210))
screen.blit(startmsg1, (300,310))
screen.blit(startmsg2, (300,410))
pygame.display.flip()
pygame.time.delay(5000)
screen.blit(bg, (0,0))
screen.blit(warnmsg, (300, 210))
screen.blit(warnmsg1, (300, 310))
screen.blit(warnmsg2, (300, 410))
pygame.display.flip()
pygame.time.delay(5000)


#Start the game loop
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	#Get our velocity based on the joystick position of the mouseposition depending on which is being used
	if usejoystick == True:
		a = winder.get_axis(0)
	        b = winder.get_axis(1)
	        button1 = winder.get_button(0)
		print a, b, button1
	else:
		mouseposition = pygame.mouse.get_pos()
		ma = mouseposition[0]
		mb = mouseposition[1]
		mousepress = pygame.mouse.get_pressed()
		button1 = mousepress[0]
		if (ma - x) > 100:
			a = .99 
		elif (ma -x) > 0:
			a = (ma - x)/100
		elif (ma - x) < -100:
			a = -.99
		elif (ma - x) < 0:
			a = (ma - x)/100

		if (mb - y) > 100:
			b = .99 
		elif (mb -y) > 0:
			b = (mb - y)/100
		elif (mb - y) < -100:
			b = -.99
		elif (mb - y) < 0:
			b = (mb - y)/100

	#Setup sliding by the penguin including the wav files that are played during slides.  Also adjust speed.		
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

	#Calculate the updated position of the penguin based on the a, b and speed variables.  Also, don't let the penguin go off screen
	x += (3*a/speed)
	if x < 0:
		x = 0
	if x > 1350:
		x = 1350 
	
	y += (2*b/speed)
	if y < 0:
		y = 0
	if y > 550:
		y = 550 

	#Setup the herring swimming across the screen.  Make the x and y for the herring change randomly
	herringy += random.randint(herringspazlow, herringspazhigh)
	herringx += (herringspeed + random.randint(herringspazlow, herringspazhigh))

	#Start the herring over if he makes it to the other side
	if herringx > 1400:
		herringx = 0
		herringy = random.randint(50, 650)

        #Setup the penguin and herring rectangles
	pengorect = pengo.get_rect()
	pengorect.inflate_ip(-40, -20)
	pengorect.right = x
	pengorect.top = y

	herringrect = herringright.get_rect()
	herringrect.right = herringx
	herringrect.top = herringy
	
	#Check for collision, increment the score if we scored a fish!  
	#Start the herring over, also make the herrign get faster and 
	#more erratic
	if pengorect.colliderect(herringrect):
		fish += 1
		score = font.render(str(fish) + " Fish", True, black)
		herringx = -100 
		if herringspeed < 5:
			herringspeed += (fish/40)
		elif herringspazhigh < 15:
			herringspazhigh += 1
			herringspazlow +=-1



	#Drawing code below this comment
	screen.blit(bg, (0,0))
	screen.blit(herringright, (herringx, herringy))
	screen.blit(pengo, (x,y))
	screen.blit(score, (10, 10))
	pygame.display.flip()

pygame.quit()
