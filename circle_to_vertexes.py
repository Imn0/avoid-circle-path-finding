
import math


def get_circle_segment_path(circle1, point1, point2):

    

    return

def get_inner_tangents(circle1, circle2):
    
    C1 = (circle1[0],circle1[1])
    C2 = (circle2[0],circle2[1])
    hypotenuse = math.dist(C1,C2)
    short = circle1[2] + circle2[2]
    theta = math.asin(short/hypotenuse) - math.pi/2 + math.atan2(circle2[1] - circle1[1], circle2[0] - circle1[0])

    t1x = circle1[0] + circle1[2] * math.cos(theta)
    t1y = circle1[1] + circle1[2] * math.sin(theta)

    t2x = circle2[0] + circle2[2] * math.cos(theta + math.pi)
    t2y = circle2[1] + circle2[2] * math.sin(theta + math.pi)
    print(f"K=({t1x},{t1y}) and F=({t2x},{t2y})")
    theta2 = - math.asin(short/hypotenuse) + math.pi/2 + math.atan2(circle2[1] - circle1[1], circle2[0] - circle1[0])
    s1x = circle1[0] + circle1[2] * math.cos(theta2)
    s1y = circle1[1] + circle1[2] * math.sin(theta2)

    s2x = circle2[0] + circle2[2] * math.cos(theta2 + math.pi)
    s2y = circle2[1] + circle2[2] * math.sin(theta2 + math.pi)
    print(f"K=({s1x},{s1y}) and F=({s2x},{s2y})")



    return

def get_outer_tangents(circle1, circle2):
    C1 = (circle1[0],circle1[1])
    C2 = (circle2[0],circle2[1])
    theta = math.atan2(circle2[1] - circle1[1], circle2[0] - circle1[0]) + math.acos(abs(circle1[2] - circle2[2])/math.dist(C1,C2))
    # first outer tangent
    t1x = circle1[0] + circle1[2] * math.cos(theta)
    t1y = circle1[1] + circle1[2] * math.sin(theta)
    
    t2x = circle2[0] + circle2[2] * math.cos(theta)
    t2y = circle2[1] + circle2[2] * math.sin(theta)

    print(f"K=({t1x},{t1y}) and F=({t2x},{t2y})")

    theta2 = math.atan2(circle2[1] - circle1[1], circle2[0] - circle1[0]) - math.acos(abs(circle1[2] - circle2[2])/math.dist(C1,C2))
    # second outer tangent
    s1x = circle1[0] + circle1[2] * math.cos(theta2)
    s1y = circle1[1] + circle1[2] * math.sin(theta2)
    
    s2x = circle2[0] + circle2[2] * math.cos(theta2)
    s2y = circle2[1] + circle2[2] * math.sin(theta2)
    print(f"K=({s1x},{s1y}) and F=({s2x},{s2y})")


    return

def main():
    circle1 = (0.0, 0.0, 5.0)
    circle2 = (3.0, 12.0, 5.0)
    get_inner_tangents(circle2, circle1)

if __name__ == "__main__":
    main()

    