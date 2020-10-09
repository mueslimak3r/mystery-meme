import os
import sys
import pygame

def reset_screen(res) :
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("image viewer")
    return screen

imgfile = ""
if len(sys.argv) < 2 :
    print("USAGE: %s [FILENAME]" % sys.argv[0])
    sys.exit()
imgfile = sys.argv[1]
if not os.path.exists(imgfile):
    print("USAGE: %s [FILENAME]" % sys.argv[0])
    sys.exit()

S = pygame.image.load(imgfile)

width_scale = 1.0
height_scale = 1.0

screen = reset_screen((int(S.get_width() * width_scale), int(S.get_height() * height_scale)))
S = S.convert()
C = S.copy()

while True :

    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()

        if e.type == pygame.KEYDOWN :
            if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                sys.exit()
            if e.key == pygame.K_MINUS and width_scale > 0.125:
                width_scale *= 0.5
                height_scale *= 0.5
            if e.key == pygame.K_EQUALS and width_scale < 8.0:
                width_scale *= 2.0
                height_scale *= 2.0
            if e.key == pygame.K_0:
                width_scale = 1.0
                height_scale = 1.0

    C = pygame.transform.scale(C, (int(S.get_width()), int(S.get_height())))
    C.blit(S, (0, 0))
    C = pygame.transform.scale(C, (int(C.get_width() * width_scale), int(C.get_height() * height_scale)))
    screen = reset_screen((C.get_width(), C.get_height()))
    screen.fill((0,0,0))
    screen.blit(C, (0,0))
    pygame.display.flip()
    pygame.time.delay(25)