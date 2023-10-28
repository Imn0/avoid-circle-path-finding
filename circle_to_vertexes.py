import math
import numpy as np 
from circle import Circle
import draw

def pc_calulate_tangent_points(point, circle: Circle):
    Cx, Cy = circle.center[0], circle.center[1]                
    r = circle.radius                              
    dx, dy = point[0]-Cx, point[1] -Cy
    dxr, dyr = -dy, dx
    d = math.sqrt(dx**2+dy**2)
    if d >= r :
        rho = r/d
        ad = rho**2
        bd = rho*math.sqrt(1-rho**2)
        T1x = Cx + ad*dx + bd*dxr
        T2x = Cx + ad*dx - bd*dxr

        T1y = Cy + ad*dy + bd*dyr
        T2y = Cy + ad*dy - bd*dyr

        return [(T1x,T1y),(T2x,T2y)]
    return []


def check_collisions(line, circles):
    for circle in circles: 
        if not is_line_free_to_go(line[0], line[1], circle):
            return False
    return True


def is_line_free_to_go(a, b, circle: Circle):

    u = ( np.dot([circle.center[0]-a[0],circle.center[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) /  (  np.dot([b[0]-a[0], b[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) 

    E = [a[0] + np.clip(u,0.0,1.0) * (b[0] - a[0]) , a[1] + np.clip(u,0.0,1.0) * (b[1] - a[1])]

    d = math.dist(E, circle.center)

    if d >= circle.radius - 0.1: 
        return True
    else:
        return False
        

def get_circle_segment_path(circle :Circle, point1: tuple, point2: tuple):

    #no worky
    """
    B_1=(0, -5.0)
    B_2=(5.0, 0)
    B_3=(5.0, -10.0)
    B_4=(8.238023526890697, -8.809882365546517)
    B_5=(6.9230769230769225, -0.38461538461538414)
    B_6=(9.454284165416997, -2.7285791729150204)
    c = Circle((5.0, -5.0), 5.0)

    point1 = B_3
    point2 = B_6
    
    
    """


    flip = False

    # going on circle first point should be first then going clokcwise second pont
    if point1[0] > point2[0]:
        tmp = point2
        point2 = point1
        point1 = tmp
        flip = True

    
    #first we get angle between point1 circle center and point2
    # theta = math.atan2(point2[1]-circle.center[1], point2[0]-circle.center[0]) - math.atan2(point1[1]-circle.center[1], point1[0]-circle.center[0])
    v1 = (circle.center[0] - point1[0], circle.center[1] - point1[1] )
    v2 = (circle.center[0] - point2[0], circle.center[1] - point2[1] )
    theta =  math.acos( np.dot(v1,v2) / ( math.sqrt(v1[0]**2 + v1[1]**2) * math.sqrt(v2[0]**2 + v2[1]**2)) )
    #we have four segments 
    theta /= 4
    x, y = point1
    ox, oy = circle.center

    #rotate to get first point 
    qx = ox + math.cos(theta) * (x - ox) + math.sin(theta) * (y - oy)
    qy = oy + -math.sin(theta) * (x - ox) + math.cos(theta) * (y - oy)

    
    f = 1 / math.cos(theta)  
    
    qx = qx * f
    qy = qy * f
    qx1 = qx
    qy1 = qy

    x, y = qx, qy
    qx2 = ox + math.cos(2*theta) * (x - ox) + math.sin(2*theta) * (y - oy)
    qy2 = oy + -math.sin(2* theta) * (x - ox) + math.cos(2*theta) * (y - oy)

    if flip:
        return [(qx2,qy2), (qx1,qy1)]
    return [(qx1,qy1),(qx2,qy2)]

def get_inner_tangents(circle1: Circle, circle2: Circle):
    
    try:
        hypotenuse = math.dist(circle1.center,circle2.center)
        short = circle1.radius + circle2.radius
        theta = math.asin(short/hypotenuse) - math.pi/2 + math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0])

        t1x = circle1.center[0] + circle1.radius * math.cos(theta)
        t1y = circle1.center[1] + circle1.radius * math.sin(theta)

        t2x = circle2.center[0] + circle2.radius * math.cos(theta + math.pi)
        t2y = circle2.center[1] + circle2.radius * math.sin(theta + math.pi)
        # print(f"K=({t1x},{t1y}) and F=({t2x},{t2y})")
        theta2 = - math.asin(short/hypotenuse) + math.pi/2 + math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0])
        s1x = circle1.center[0] + circle1.radius * math.cos(theta2)
        s1y = circle1.center[1] + circle1.radius * math.sin(theta2)

        s2x = circle2.center[0] + circle2.radius * math.cos(theta2 + math.pi)
        s2y = circle2.center[1] + circle2.radius * math.sin(theta2 + math.pi)
        # print(f"K=({s1x},{s1y}) and F=({s2x},{s2y})")
    except Exception as e:
        print(e)
        print("inner tangent")
        return []

    return [ [(t1x,t1y),(t2x,t2y)], [(s1x,s1y), (s2x,s2y)] ] 


def get_outer_tangents(circle1: Circle, circle2: Circle):
    try:
        theta = math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0]) + math.acos(abs(circle1.radius - circle2.radius)/math.dist(circle1.center,circle2.center))
        # first outer tangent
        t1x = circle1.center[0] + circle1.radius * math.cos(theta)
        t1y = circle1.center[1] + circle1.radius * math.sin(theta)
        
        t2x = circle2.center[0] + circle2.radius * math.cos(theta)
        t2y = circle2.center[1] + circle2.radius * math.sin(theta)

        # print(f"K=({t1x},{t1y}) and F=({t2x},{t2y})")

        theta2 = math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0]) - math.acos(abs(circle1.radius - circle2.radius)/math.dist(circle1.center,circle2.center))
        # second outer tangent
        s1x = circle1.center[0] + circle1.radius * math.cos(theta2)
        s1y = circle1.center[1] + circle1.radius * math.sin(theta2)
        
        s2x = circle2.center[0] + circle2.radius * math.cos(theta2)
        s2y = circle2.center[1] + circle2.radius * math.sin(theta2)
        # print(f"K=({s1x},{s1y}) and F=({s2x},{s2y})")
    except Exception as e:
        print(e)
        print("outer tangent")
        return []

    return [ [(t1x,t1y),(t2x,t2y)], [(s1x,s1y), (s2x,s2y)] ] 



def test():
    B_1=(0, -5.0)
    B_2=(5.0, 0)
    B_3=(5.0, -10.0)
    B_4=(8.238023526890697, -8.809882365546517)
    B_5=(6.9230769230769225, -0.38461538461538414)
    B_6=(9.454284165416997, -2.7285791729150204)
    c = Circle((5.0, -5.0), 5.0)

    point1 = B_3
    point2 = B_6

    point1 = B_2
    point2 = B_5


    p1, p2 = get_circle_segment_path(c, point2, point1)

    line1 = [point1, p1]
    line2 = [point2, p2]
    connection = [p1,p2]

    print(p1)
    print(p2)

    draw.sex([line1, line2, connection], circles=[c])


    return



def main():
    
    start = (0.0, 0.0)
    end = (20.0, -10.0)
    circle_1 = Circle((5.0, -5.0), 5.0)
    circle_2 = Circle((15.0, -7.0), 3.0)
    circles = [circle_1, circle_2]

    final_lines = []

    # check if we can go directly
    can_do = True
    for circle in circles:
        if not is_line_free_to_go(start, end, circle):
            can_do = False
    print(can_do)

    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(start, circle)
        tg1 = True
        tg2 = True
        for c in circles:
            if not is_line_free_to_go(start, tangent_end_points[0], c):
                tg1 = False
            if not is_line_free_to_go(start, tangent_end_points[1], c):
                tg2 = False
        
        if tg1:
            final_lines.append([start, tangent_end_points[0]])
            circle.points_on_circle.append(tangent_end_points[0])
    
        if tg2:
            final_lines.append([start, tangent_end_points[1]])
            circle.points_on_circle.append(tangent_end_points[1])

    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(end, circle)
        tg1 = True
        tg2 = True
        for c in circles:
            if not is_line_free_to_go(end, tangent_end_points[0], c):
                tg1 = False
            if not is_line_free_to_go(end, tangent_end_points[1], c):
                tg2 = False
        
        if tg1:
            final_lines.append([end, tangent_end_points[0]])
            circle.points_on_circle.append(tangent_end_points[0])
    
        if tg2:
            final_lines.append([end, tangent_end_points[1]])
            circle.points_on_circle.append(tangent_end_points[1])


    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            # print(get_outer_tangents(circles[i], circles[j]))
            outer_tangent1, outer_tangent2 = get_outer_tangents(circles[i], circles[j])
            # print( get_inner_tangents(circles[i], circles[j]) )
            inner_tangent1, inner_tangent2 = get_inner_tangents(circles[i], circles[j])
            if check_collisions(inner_tangent1, circles):
                final_lines.append(inner_tangent1)
                circles[i].points_on_circle.append(inner_tangent1[0])
                circles[j].points_on_circle.append(inner_tangent1[1])

            if check_collisions(outer_tangent1, circles):
                final_lines.append(outer_tangent1)
                circles[i].points_on_circle.append(outer_tangent1[0])
                circles[j].points_on_circle.append(outer_tangent1[1])
            
            if check_collisions(inner_tangent2, circles):
                final_lines.append(inner_tangent2)
                circles[i].points_on_circle.append(inner_tangent2[0])
                circles[j].points_on_circle.append(inner_tangent2[1])
            
            if check_collisions(outer_tangent2, circles):
                final_lines.append(outer_tangent2)
                circles[i].points_on_circle.append(outer_tangent2[0])
                circles[j].points_on_circle.append(outer_tangent2[1])


    for circle in circles:
        new_list = []
        for point in circle.points_on_circle:
            if point not in new_list:
                new_list.append(point)
        show_poitns(new_list)
        circle.points_on_circle = new_list

    for circle in circles:
        new_list = []
        for i in range(len(circle.points_on_circle)):
            for j in range(i+1, len(circle.points_on_circle)):
                p1, p2 = get_circle_segment_path(circle,circle.points_on_circle[i], circle.points_on_circle[j])

                line1 = [circle.points_on_circle[i], p1]
                if check_collisions(line1, circles):
                    final_lines.append(line1)
                    new_list.append(line1)
                line2 = [circle.points_on_circle[j], p2]
                if check_collisions(line2, circles):
                    new_list.append(line2)
                    final_lines.append(line2)

                connect_line = [circle.points_on_circle[i],circle.points_on_circle[j]]
                if check_collisions(connect_line, circles):
                    new_list.append(connect_line)
                    final_lines.append(connect_line)

    draw.sex(final_lines, circles)



def show_answers(final_lines):
    count = 1
    for line in final_lines:
        start, end = line
        print(f"A_{{{count}}}={start}")
        print(f"B_{{{count}}}={end}")
        print(f"a_{{{count}}}=Segment(A_{count}, B_{count})")
        count = count + 1

def show_poitns(points):
    count = 1
    for point in points:
        print(f"B_{{{count}}}={point}")
        count = count + 1




if __name__ == "__main__":
    test()

    
