import math
import numpy as np 
from circle import Circle
import draw
from graph import Graph
import graph
from node import Node


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
    offset_x, offset_y = circle.center
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(theta)
    sin_rad = math.sin(theta)
    qx1 = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy1 = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    if math.dist( (qx1, qy1), point2) > math.dist( point1, point2):
        theta = -theta
        x, y = point1
        offset_x, offset_y = circle.center
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = math.cos(theta)
        sin_rad = math.sin(theta)
        qx1 = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy1 = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    
    d = circle.radius / math.cos(theta)  
    f = d/circle.radius

    qx1 = qx1
    qy1 = qy1

    x, y = qx1, qy1
    offset_x, offset_y = circle.center
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(2*theta)
    sin_rad = math.sin(2*theta)
    qx2 = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy2 = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y


    qx1 = f*(qx1-circle.center[0])
    qy1 = f*(qy1-circle.center[1])

    qx2 = f*(qx2-circle.center[0])
    qy2 = f*(qy2-circle.center[1])

    qx1 = circle.center[0] + qx1
    qy1 = circle.center[1] + qy1

    qx2 = circle.center[0] + qx2
    qy2 = circle.center[1] + qy2

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

    points = [B_1, B_2, B_3, B_4, B_5, B_6]
    # points = [ B_1, B_4]
    lines = []

    for i in range(len(points)):
        for j in range(i+1, len(points)):

            p1, p2 = get_circle_segment_path(c, points[i], points[j])

            line1 = [points[i], p1]
            line2 = [points[j], p2]
            connection = [p1,p2]
            lines.append(line1)
            lines.append(line2)
            lines.append(connection)
    
    
    draw.draw(lines, circles=[c])


    return



def stuff(start, end, circles:[Circle]):
    
    # tart = (0.0, 0.0)
    # end = (35.0, -20.0)
    # circle_1 = Circle((5.0, -5.0), 5.0)
    # circle_2 = Circle((20.0, -13.0), 4.0)
    # circle_3 = Circle((15.0, -7.0), 3.0)
    # circle_4 = Circle((30.0, -16.0), 2.0)
    # circle_5 = Circle((20.0, -16.0), 2.0)
    # circle_6 = Circle((21.0, -14.0), 6.0)
    # circles = [circle_1, circle_2, circle_3, circle_4,circle_5,circle_6]

    print(circles)
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
            try:
                inner_tangent1, inner_tangent2 = get_inner_tangents(circles[i], circles[j])
                if check_collisions(inner_tangent1, circles):
                    final_lines.append(inner_tangent1)
                    circles[i].points_on_circle.append(inner_tangent1[0])
                    circles[j].points_on_circle.append(inner_tangent1[1])
                if check_collisions(inner_tangent2, circles):
                    final_lines.append(inner_tangent2)
                    circles[i].points_on_circle.append(inner_tangent2[0])
                    circles[j].points_on_circle.append(inner_tangent2[1])
            except:
                print("no inner tangent")

            try:
                outer_tangent1, outer_tangent2 = get_outer_tangents(circles[i], circles[j])
                if check_collisions(outer_tangent1, circles):
                    final_lines.append(outer_tangent1)
                    circles[i].points_on_circle.append(outer_tangent1[0])
                    circles[j].points_on_circle.append(outer_tangent1[1])
                
                if check_collisions(outer_tangent2, circles):
                    final_lines.append(outer_tangent2)
                    circles[i].points_on_circle.append(outer_tangent2[0])
                    circles[j].points_on_circle.append(outer_tangent2[1])
            except:
                print("no inner tangent")

    for circle in circles:
        new_list = []
        for point in circle.points_on_circle:
            if point not in new_list:
                new_list.append(point)
        circle.points_on_circle = new_list

    
    for circle in circles:
        new_list = []
        for i in range(len(circle.points_on_circle)):
            for j in range(i+1, len(circle.points_on_circle)):
                p1, p2 = get_circle_segment_path(circle,circle.points_on_circle[i], circle.points_on_circle[j])

                line1 = [circle.points_on_circle[i], p1]
                line2 = [circle.points_on_circle[j], p2]
                connect_line = [p1,p2]
                if( check_collisions(line1, circles) and check_collisions(line2, circles) and check_collisions(connect_line, circles) ):
                    final_lines.append(line1)
                    new_list.append(line1)
                
                    new_list.append(line2)
                    final_lines.append(line2)

                    new_list.append(connect_line)
                    final_lines.append(connect_line)
    
    # show_answers(final_lines)
    draw.draw(final_lines, circles)
    return final_lines



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


def are_floats_the_same(x:float, a:float):
    if abs(x-a) < 0.01:
        return True
    return False

def main(start, end, circles):

    
    # start = (0.0, 0.0)
    # end = (35.0, -20.0)
    # circle_1 = Circle((5.0, -5.0), 5.0)
    # circle_2 = Circle((20.0, -13.0), 4.0)
    # circle_3 = Circle((15.0, -7.0), 3.0)
    # circle_4 = Circle((30.0, -16.0), 2.0)
    # circle_5 = Circle((31.0, -16.0), 2.0)
    # circle_6 = Circle((29.0, -16.0), 1.0)
    # circles = [circle_1, circle_2, circle_3, circle_4, circle_5, circle_6]

    
    lines = stuff(start, end, circles)
    points = []

    for line in lines:
        point1 = line[0]
        point2 = line[1]
        
        point1_index = -1
        point2_index = -1

        for i in range(len(points)):
            x = points[i][0]
            y = points[i][1]

            if are_floats_the_same(x, point1[0]) and are_floats_the_same(y, point1[1]):
                point1_index = i
        if point1_index == -1:
            points.append(point1)
            point1_index = len(points) -1

        for i in range(len(points)):
            x = points[i][0]
            y = points[i][1]
            if are_floats_the_same(x, point2[0]) and are_floats_the_same(y, point2[1]):
                point2_index = i

        if point2_index == -1:
            points.append(point2)
            point2_index = len(points) -1

    g = Graph(len(lines))

    for line in lines:
        point1 = line[0]
        point2 = line[1]
        
        point1_index = -1
        point2_index = -1

        for i in range(len(points)):
            x = points[i][0]
            y = points[i][1]

            if are_floats_the_same(x, point1[0]) and are_floats_the_same(y, point1[1]):
                point1_index = i

            if are_floats_the_same(x, point2[0]) and are_floats_the_same(y, point2[1]):
                point2_index = i

        if point1_index == -1 or point2_index == -1:
            print("whoosp, graph thing")
            return
        
        
        node1 = Node(point1[0], point1[1], point1_index)
        node2 = Node(point2[0], point2[1], point2_index)
        cost = math.dist(point1,point2)

        g.add_edge(node1, node2, cost)


    start_index = 0
    end_index = 0
    for i in range(len(points)):
        if are_floats_the_same(start[0], points[i][0]) and are_floats_the_same(start[1], points[i][1]):
            start_index = i
    
    for i in range(len(points)):
        if are_floats_the_same(end[0], points[i][0]) and are_floats_the_same(end[1], points[i][1]):
            end_index = i

    # print(points[0])


    shortest_path, shortest_distance = g.dijkstra(start_index,end_index)
    print("Shortest Path:", shortest_path)
    final_lines = []
    for i in range(1,len(shortest_path)):
        final_lines.append(  [(points[shortest_path[i]][0],points[shortest_path[i]][1]),(points[shortest_path[i-1]][0],points[shortest_path[i-1]][1])]  )
    print("Shortest Distance:", shortest_distance)

    draw.draw(final_lines, circles)
    return shortest_path
        





if __name__ == "__main__":
    main()

    
