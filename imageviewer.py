import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def reset_screen(res) :
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("press q or esc to exit")
    return screen


def render_img(S = None):
    if S == None:
        return

    scale = 500 / S.get_height()

    screen = reset_screen((int(S.get_width() * scale), int(S.get_height() * scale)))
    S = S.convert()
    C = S.copy()
    state_changed = 1
    sample_original = 1
    while True :

        for e in pygame.event.get() :
            if e.type == pygame.QUIT :
                return

            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                    return
                if e.key == pygame.K_MINUS and S.get_height() * scale > 200.0 and S.get_width() * scale > 200.0:
                    scale *= 0.5
                    state_changed = 1
                if e.key == pygame.K_EQUALS and S.get_height() * scale < 5000.0 and S.get_width() * scale < 5000.0:
                    scale *= 2.0
                    state_changed = 1
                    if C.get_width() < S.get_width():
                        sample_original = 1
                if e.key == pygame.K_0:
                    scale = 1.0
                    state_changed = 1
                    sample_original = 1
                
        if state_changed == 1:
            if sample_original == 1:
                C = pygame.transform.scale(C, (int(S.get_width()), int(S.get_height())))
                C.blit(S, (0, 0))
            C = pygame.transform.scale(C, (int(S.get_width() * scale), int(S.get_height() * scale)))
            screen = reset_screen((C.get_width(), C.get_height()))
            screen.fill((0,0,0))
            screen.blit(C, (0,0))
            pygame.display.flip()
            state_changed = 0
            sample_original = 0
        pygame.time.wait(500)

def view_image_object(imgobject, size, mode):
    S = pygame.image.fromstring(imgobject, size, mode)
    render_img(S)

def view_file(imgfile = ""):
    if os.path.exists(imgfile):
        S = pygame.image.load(imgfile)
        render_img(S)

if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("USAGE: %s [FILENAME]" % sys.argv[0])
        sys.exit()
    imgfile = sys.argv[1]
    if not os.path.exists(imgfile):
        print("USAGE: %s [FILENAME]" % sys.argv[0])
        sys.exit()
    view_file(imgfile)