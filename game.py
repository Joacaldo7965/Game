from Files.Sprites.Skeleton import Skeleton
import pygame as pg

if not pg.init():
    exit()


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 544


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
myfont = pg.font.SysFont("Comic Sans MS", 30)
clock = pg.time.Clock()

c_white = (255, 255, 255)
c_red = (255, 0, 0)

skeli = Skeleton(464, 397)
bg = pg.image.load("Images/background.png")

clicked_pos = None


def drawScreen(DEBUG):
    screen.blit(bg, (0, 0))
    skeli.display(screen)
    skeli.animate()

    if DEBUG:
        # Show the skeli position
        pg.draw.circle(screen, c_red, (skeli.x, skeli.y), 4)
        pg.draw.circle(screen, c_red, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 4)

        # Show FPS
        FPS = round(clock.get_fps(), 1)
        label = myfont.render(f"FPS: {FPS}", 1, (255, 255, 255))
        screen.blit(label, (10, 10))

        # Show where is facing
        label = myfont.render(f"Moving right: {skeli.facing_right}", 1, (255, 255, 255))
        screen.blit(label, (10, 50))

        # Show what action is doing
        label = myfont.render(f"Status: {skeli.state}", 1, (255, 255, 255))
        screen.blit(label, (10, 90))

        # Show if its in action
        label = myfont.render(f"Action: {skeli.isInAction()}", 1, (255, 255, 255))
        screen.blit(label, (10, 130))

        # Show the scale of the skeli
        label = myfont.render(f"Scale: {skeli.scale}", 1, (255, 255, 255))
        screen.blit(label, (10, 170))

        # Show the position
        label = myfont.render(f"Coords: ({skeli.x}, {skeli.y})", 1, (255, 255, 255))
        screen.blit(label, (10, 210))

        # Show the current action
        label = myfont.render(f"Action: {skeli.currentAction()}", 1, (255, 255, 255))
        screen.blit(label, (10, 250))

        # Show the left click pos
        # label = myfont.render(f"Click: {clicked_pos}", 1, (255, 255, 255))
        # screen.blit(label, (10, 290))

    clock.tick(30)
    pg.display.flip()


def mainLoop():
    running = True
    DEBUG = False

    while running:

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                # Movement
                elif event.key == pg.K_a and not skeli.isInAction():   # Left
                    skeli.Walk()
                    pass
                elif event.key == pg.K_d and not skeli.isInAction():   # Right
                    skeli.Walk()
                    pass
                # Buttons
                elif event.key == pg.K_s:   # Show Hitbox
                    DEBUG = not DEBUG
                    skeli.showHitbox()
                    pass
                elif event.key == pg.K_e:
                    skeli.React()
                elif event.key == pg.K_f:
                    skeli.Attack()
                elif event.key == pg.K_DOWN:
                    skeli.scale -= 1
                elif event.key == pg.K_UP:
                    skeli.scale += 1
                elif event.key == pg.K_i:
                    skeli.y -= 10
                elif event.key == pg.K_k:
                    skeli.y += 10
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = event.pos
            elif event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        if not skeli.isInAction():
            # Movement
            if keys[pg.K_a] and keys[pg.K_d]:
                if skeli.currentAction() != "Idle":
                    skeli.Idle()
            elif keys[pg.K_a]:
                skeli.moveLeft()
            elif keys[pg.K_d]:
                skeli.moveRight()
            elif skeli.currentAction() == "Walk":
                skeli.Idle()   

        drawScreen(DEBUG)

    pg.quit()


if __name__ == "__main__":
    mainLoop()