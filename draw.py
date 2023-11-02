import pygame as pg
import sys

def draw(final_segments = [], circles= [], points = []):
    """
    basic pygame function to display the path, doesnt always fit
    """
    pg.init()
    screen = pg.display.set_mode((1000, 1000))

    screen.fill(pg.Color("white"))

    while True:
        try:
            for segment in final_segments:
                start, end = segment

                # move and scale a bit
                start = (start[0] * 2 + 200,   start[1] *2+ 60)
                end = (end[0] * 2 +200, end[1] *2 + 60)

                pg.draw.line(screen, pg.Color("red"), start, end, 5)

            for point in points:
                pg.draw.circle(screen, pg.Color("green"), (point[0]*2+200, point[1]*2+60), 10, width=3)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            
            for cirlce in circles:
                pg.draw.circle(screen, pg.Color("black"), (cirlce.center[0]*2+200, cirlce.center[1]*2+60), cirlce.radius*2, width=1)

            pg.display.update()
        except:
            return