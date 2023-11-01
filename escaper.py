from circle import Circle
import math
import draw



def find_intersection_points(circle1, circle2):
    x1, y1 = circle1.center
    x2, y2 = circle2.center
    r1 = circle1.radius
    r2 = circle2.radius
    
    # Calculate the distance between the centers of the two circles
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Check if the circles are completely separate or one is contained within the other
    if d >= r1 + r2 or d <= abs(r1 - r2):
        return None  # No intersection
    
    # Calculate the intersection points
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)

    #todo: check if coordinates are OK
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d
    
    x4 = x3 + h * (y2 - y1) / d
    y4 = y3 - h * (x2 - x1) / d
    
    x5 = x3 - h * (y2 - y1) / d
    y5 = y3 + h * (x2 - x1) / d
    
    return (x4, y4), (x5, y5)

def find_intersections(circles):
    intersections = []
    
    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            if do_circles_intersect(circles[i], circles[j]):
                intersection = find_intersection_points(circles[i], circles[j])
                if intersection:
                    intersections.extend(intersection)
    
    return intersections

def do_circles_intersect(circle1, circle2):
     # Check if the distance is less than the sum of the radii
    return math.dist(circle1.center, circle2.center) < (circle1.radius + circle2.radius)

def are_floats_the_same(x:float, a:float):
    if abs(x-a) < 0.01:
        return True
    return False


def find_a_way_out_of_cirlce(point, circle: Circle):
    if point[0] == circle.center[0] and point[1] == circle.center[1]:
        point = (point[0] + 0.01, point[1] + 0.01)
    
    d = math.dist(point, circle.center)

    v_x = point[0] - circle.center[0]
    v_y = point[1] - circle.center[1]

    f = circle.radius / d
    v_x = v_x * f
    v_y = v_y * f

    return v_x + circle.center[0], v_y + circle.center[1]

def find_closest_point_im_frei(point, circles: [Circle],circle_point_is_in: Circle, do_draw = False):
    
    way_out = find_a_way_out_of_cirlce(point, circle_point_is_in)
    if not is_point_in_any_circle(way_out, circles):
        return way_out


    intersections = find_intersections(circles)
    intersections.append(way_out)
    if do_draw:
        draw.draw(points=intersections, circles=circles)

    for point in intersections:
        for circle in circles:
            if math.dist(point, circle.center) < circle.radius - 0.01:
                intersections.remove(point)

    min_dist = float('inf')
    x_out = 0
    y_out = 0

    for intersection in intersections:
        if math.dist(point,intersection) < min_dist:
            min_dist = math.dist(point,intersection)
            x_out = intersection[0]
            y_out = intersection[1]

    return (x_out, y_out)

def is_point_in_any_circle(point, circles):
    for circle in circles:
        if math.dist(point, circle.center) < circle.radius:
            return True
    return False

def weg_zur_Freiheit(point, circles, do_draw):
    for circle in circles:
        if math.dist(point, circle.center) < circle.radius:
            return find_closest_point_im_frei(point, circles, circle, do_draw)
    return point 


if __name__ == "__main__":
    start = (60.0, 200.0)
    end = (50.0, 140.0)

    circle_1 = Circle((100.0, 150.0), 70.0)
    circle_2 = Circle((50.0, 195.0), 30.0)
    circle_3 = Circle((1.0, 200.0), 25.0)
    circle_4 = Circle((-30.0, 150.0), 45.0)
    circles = [circle_1, circle_2, circle_3, circle_4]

    p = weg_zur_Freiheit(start, circles, do_draw=True)
    line = [start, p]
    lines = [line]
    print(line)
    draw.draw(lines, circles)

    # find_closest_point_im_frei(point, circles, circle_1)