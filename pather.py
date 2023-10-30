import vertexer
from circle import Circle


def main():

    start_x = float(input("start x pos: "))
    start_y = float(input("start y pos: "))


    end_x = float(input("end x pos: "))
    end_y = float(input("end y pos: "))

    start = (start_x, start_y)
    end = (end_x, end_y)

    zones = []

    add_zones = 1
    while(add_zones == 1):
        add_zones = int(input("do u want to add no-fly zone? [y/n] "))
        if add_zones == 1:
            center_x = float(input("zone center x pos: "))
            center_y = float(input("zone center y pos: "))
            radius = float(input("zone radius: "))
            zone = Circle((center_x, center_y),radius)
            zones.append(zone) 

    path = vertexer.main(start, end, zones)       




if __name__ == "__main__":
    main()
