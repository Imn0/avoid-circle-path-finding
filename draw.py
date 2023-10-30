import pygame as pg
import sys

def draw(final_lines, circles):
    pg.init()
    screen = pg.display.set_mode((1000, 1000))

# Setting a white background
    screen.fill(pg.Color("white"))

    while True:
        try:
            for line in final_lines:
                start, end = line


                start = (start[0] * 20 + 200,   start[1] * -20 +200)
                end = (end[0] * 20+200, end[1] * -20 + 200)

                pg.draw.line(screen, pg.Color("red"), start, end, 5)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            #circle_1 = Circle((5.0, -5.0), 5.0)
            # pg.draw.circle(screen, pg.Color("black"), (5.0*20+200, -5.0*-20+200), 5.0*20, width=1)
            
            for cirlce in circles:
                pg.draw.circle(screen, pg.Color("black"), (cirlce.center[0]*20+200, cirlce.center[1]*-20+200), cirlce.radius*20, width=1)

            # Refreshing screen, otherwise no changes will occur
            pg.display.update()
        except:
            return