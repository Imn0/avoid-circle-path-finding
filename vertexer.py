import math
import numpy as np 
from circle import Circle
import draw
from graph import Graph
from node import Node

def pc_calulate_tangent_points(point, circle: Circle):
    """
    calculates both tangent segments between point and a circle, doesnt check for collisons
    if there are no tangents returns empty list
    """
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


def check_collisions(segment, circles):
    """
    checks for collisons between segment and every cirle in circles
    returns True if segment is not coliding 
    """
    for circle in circles: 
        if not is_segment_free_to_go(segment[0], segment[1], circle):
            return False
    return True


def is_segment_free_to_go(a, b, circle: Circle):
    """
    checks wether segment between a and b colidees with given circle
    """
    if are_floats_the_same(a[0],b[0]) and are_floats_the_same(a[1],b[1]):
        return True

    u = ( np.dot([circle.center[0]-a[0],circle.center[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) 
    v =  (  np.dot([b[0]-a[0], b[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) 

    if v == 0.0:
        print("division by 0")
        print(f"circle={circle.center} line={(a,b)}")
        exit()

    u = u / v

    E = [a[0] + np.clip(u,0.0,1.0) * (b[0] - a[0]) , a[1] + np.clip(u,0.0,1.0) * (b[1] - a[1])]

    d = math.dist(E, circle.center)

    # 0.00001 coz float math  
    if d >= circle.radius - 0.00001: 
        return True
    else:
        return False
        

def get_circle_segment_path(circle :Circle, point1: tuple, point2: tuple):
    """
    calculates path between two points on the circle
    
    """

    #first we get angle between point1 circle center and point2
    # theta = math.atan2(point2[1]-circle.center[1], point2[0]-circle.center[0]) - math.atan2(point1[1]-circle.center[1], point1[0]-circle.center[0])
    v1 = (circle.center[0] - point1[0], circle.center[1] - point1[1] )
    v2 = (circle.center[0] - point2[0], circle.center[1] - point2[1] )
    try:
        theta =  math.acos( np.dot(v1,v2) / ( math.sqrt(v1[0]**2 + v1[1]**2) * math.sqrt(v2[0]**2 + v2[1]**2)) )
    except:
        #angle is 0
        return
    
    """
    Start with constructing angle between point1 cirle center and point2, theta.

    Now construct radius landing on circle at point r_l, such that 
    angle point1, cirlce center and r_l is equal to theta/2
    and point2, cirlce center and r_l is ealso qual to theta/2

    then construct tangent going through r_l, another going through point1 
    and last one going through point2 

    let p1_r be intersections between point1's tangent and r_l tangent and
    p2_r be intersections between point2's tangent and r_l tangent 

    note that angle point1(2) circle center and p1(2)_r is equal to theta/4 
    and also that p1_r is closer to point2 than point1
    """


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


    # scaling from circle diameter to tangent intersection
    qx1 = f*(qx1-circle.center[0])
    qy1 = f*(qy1-circle.center[1])

    qx2 = f*(qx2-circle.center[0])
    qy2 = f*(qy2-circle.center[1])

    qx1 = circle.center[0] + qx1
    qy1 = circle.center[1] + qy1

    qx2 = circle.center[0] + qx2
    qy2 = circle.center[1] + qy2


    return [(qx1,qy1),(qx2,qy2)]

def get_inner_tangents(circle1: Circle, circle2: Circle):
    
    """
    connect both centers and you will find triangles 
    """
    swap = False
    if circle2.radius > circle1.radius:
        t = circle1
        circle1 = circle2
        circle2 = t
        swap = True
    hypotenuse = math.dist(circle1.center,circle2.center)
    short = circle1.radius + circle2.radius
    try:
            #   relative angle                      to correct for circles not always being parallel to axis
        theta = math.asin(short/hypotenuse) - math.pi/2 
        theta += math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0])

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
    except Exception as e:
        print(e)
        print("innter tangent")
        return []

    if swap:
        return [  [(s1x,s1y), (s2x,s2y)], [(t1x,t1y),(t2x,t2y)] ] 

    return [ [(t1x,t1y),(t2x,t2y)], [(s1x,s1y), (s2x,s2y)] ] 


def get_outer_tangents(circle1: Circle, circle2: Circle):
    swap = False
    if circle2.radius > circle1.radius:
        t = circle1
        circle1 = circle2
        circle2 = t
        swap = True
    

    try:
        """
        pretty much same as inner tangent just different circles
        """
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

    if swap:
        return [  [(s1x,s1y), (s2x,s2y)], [(t1x,t1y),(t2x,t2y)] ] 

    return [ [(t1x,t1y),(t2x,t2y)], [(s1x,s1y), (s2x,s2y)] ] 


def vertexify(start, end, circles:[Circle], draw_answers=False):
   
    print(circles)
    final_segments = []

    # check if we can go directly
    can_do = True
    for circle in circles:
        if not is_segment_free_to_go(start, end, circle):
            can_do = False
    print(can_do)
    if can_do:
        return [(start, end)]

    points = []

    #get angents between starting point and all circles
    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(start, circle)
        if check_collisions((tangent_end_points[0], start), circles):
            final_segments.append([start, tangent_end_points[0]])
            points.append(tangent_end_points[0])

        if check_collisions((tangent_end_points[1], start), circles):
            final_segments.append([start, tangent_end_points[1]])
            points.append(tangent_end_points[1])
    
   
    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(end, circle)
        if check_collisions((tangent_end_points[0], end), circles):
            final_segments.append([end, tangent_end_points[0]])
            points.append(tangent_end_points[0])

        if check_collisions((tangent_end_points[1], end), circles):
            final_segments.append([end, tangent_end_points[1]])
            points.append(tangent_end_points[1])


    for i in range(len(circles)):
        for j in range(i+1, len(circles)):
            outer_tangent1, outer_tangent2 = get_outer_tangents(circles[i], circles[j])
            print(outer_tangent1)
            print(outer_tangent2)
            if check_collisions(outer_tangent1, circles):
                final_segments.append(outer_tangent1)
                points.append(outer_tangent1[0])
                points.append(outer_tangent1[1])
                
            if check_collisions(outer_tangent2, circles):
                final_segments.append(outer_tangent2)
                points.append(outer_tangent2[0])
                points.append(outer_tangent2[1])

            try:
                inner_tangent1, inner_tangent2 = get_inner_tangents(circles[i], circles[j])
            except:
                continue
            if check_collisions(inner_tangent1, circles):
                final_segments.append(inner_tangent1)
                points.append(inner_tangent1[0])
                points.append(inner_tangent1[1])
            if check_collisions(inner_tangent2, circles):
                final_segments.append(inner_tangent2)
                points.append(inner_tangent2[0])
                points.append(inner_tangent2[1])
                
            
    for point in points:
        for circle in circles:
            if are_floats_the_same( math.dist(point, circle.center), circle.radius):
                circle.points_on_circle.append(point) 



    # get paths for points around the circle  
    for circle in circles:
        new_list = []
        for i in range(len(circle.points_on_circle)):
            for j in range(i+1, len(circle.points_on_circle)):
                try:
                    p1, p2 = get_circle_segment_path(circle,circle.points_on_circle[i], circle.points_on_circle[j])
                except:
                    # we dint get a valid segment, prob angle was 0 
                    # geometry 
                    continue
                segment1 = [circle.points_on_circle[i], p1]
                segment2 = [circle.points_on_circle[j], p2]
                connect_segment = [p1,p2]
                if( check_collisions(segment1, circles) and check_collisions(segment2, circles) and check_collisions(connect_segment, circles) ):
                    final_segments.append(segment1)
                    new_list.append(segment1)
                
                    new_list.append(segment2)
                    final_segments.append(segment2)

                    new_list.append(connect_segment)
                    final_segments.append(connect_segment)
    
    if draw_answers:
        # show_answers(final_segments)
        draw.draw(final_segments, circles, [start, end])
    return final_segments



def show_answers(final_segments):
    count = 1
    for segment in final_segments:
        start, end = segment
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
    if abs(x-a) < 0.1:
        return True
    return False



def find_path(start, end, circles, draw_path = False):
    
    segments = vertexify(start, end, circles, draw_answers=draw_path)
    points = []

    for segment in segments:
        point1 = segment[0]
        point2 = segment[1]
        
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

    g = Graph(len(points)) 

    for segment in segments:
        point1 = segment[0]
        point2 = segment[1]
        
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



    shortest_path, shortest_distance = g.dijkstra(start_index,end_index)
    print("Shortest Path:", shortest_path)
    print("Shortest Distance:", shortest_distance)
    if draw_path:
        final_segments = []
        for i in range(1,len(shortest_path)):
            final_segments.append(  [(points[shortest_path[i]][0],points[shortest_path[i]][1]),(points[shortest_path[i-1]][0],points[shortest_path[i-1]][1])]  )

        draw.draw(final_segments, circles, [start, end])

    final_points = []
    for i in range(len(shortest_path)):
        final_points.append(  (points[shortest_path[i]][0],points[shortest_path[i]][1]) )
    return final_points
        


def test():
    start = (20.0, 200.0)
    end = (150.0,200.0)

    c1 = Circle((0.0, 250.0), 40.0)
    c2 = Circle((50.0, 250.0), 30.0)
    c3 = Circle((100.0, 260.0), 25.0)
    c4 = Circle((150.0, 250.0), 45.0)
    c5 = Circle((200.0, 250.0), 45.0)
    c6 = Circle((250.0, 250.0), 45.0)
    c7 = Circle((300.0, 250.0), 45.0)
    c8 = Circle((350.0, 250.0), 45.0)
    c9 = Circle((0.0, 150.0), 40.0)
    c10 = Circle((50.0, 150.0), 30.0)
    c11 = Circle((100.0, 120.0), 35.0)
    c12 = Circle((150.0, 150.0), 45.0)
    c13 = Circle((200.0, 150.0), 45.0)
    c14 = Circle((250.0, 150.0), 45.0)
    c15 = Circle((300.0, 150.0), 45.0)
    c16 = Circle((350.0, 150.0), 45.0)
    c17 = Circle((0.0, 200.0), 45.0)


    # circles = [c4, c3, c2]
    circles = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17 ]
    print()
    final_segments = []
    points = []
    #get angents between starting point and all circles
    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(start, circle)
        if check_collisions((tangent_end_points[0], start), circles):
            final_segments.append([start, tangent_end_points[0]])
            points.append(tangent_end_points[0])

        if check_collisions((tangent_end_points[1], start), circles):
            final_segments.append([start, tangent_end_points[1]])
            points.append(tangent_end_points[1])
    
   
    for circle in circles:
        tangent_end_points = pc_calulate_tangent_points(end, circle)
        if check_collisions((tangent_end_points[0], end), circles):
            final_segments.append([end, tangent_end_points[0]])
            points.append(tangent_end_points[0])

        if check_collisions((tangent_end_points[1], end), circles):
            final_segments.append([end, tangent_end_points[1]])
            points.append(tangent_end_points[1])



    draw.draw(final_segments,circles)

if __name__ == "__main__":
    # test()
    # exit()
    start = (250.0, 200.0)
    end = (100.0, 350.0)

    c1 = Circle((0.0, 250.0), 40.0)
    c2 = Circle((50.0, 275.0), 30.0)
    c3 = Circle((100.0, 300.0), 35.0)
    c4 = Circle((150.0, 340.0), 45.0)
    c5 = Circle((200.0, 380.0), 45.0)
    c6 = Circle((250.0, 420.0), 45.0)
    c7 = Circle((0.0, 150.0), 40.0)
    c8 = Circle((50.0, 110.0), 30.0)
    c9 = Circle((100.0, 80.0), 35.0)
    c10 = Circle((150.0, 50.0), 45.0)
    c11 = Circle((155.0, 200.0), 45.0)

    # circles = [c17, c2, c3]
    circles = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11]


    # p = permutations(circles)
    # print(list(p)[1])
    find_path(start, end, circles, draw_path=True)