import pygame as pg


def sex(final_lines):
    pg.init()
    screen = pg.display.set_mode((1000, 1000))

# Setting a white background
    screen.fill(pg.Color("white"))

    while True:
        for line in final_lines:
            start, end = line


            start = ( start[0] * 40,   start[1] * -40)
            end = (end[0] * 40, end[1] * -40)

            pg.draw.line(screen, pg.Color("red"), start, end, 5)
        
        # Refreshing screen, otherwise no changes will occur
        pg.display.update()
        
        # (can also use a pg.time.Clock to specify the framerate)
        pg.time.wait(5000)