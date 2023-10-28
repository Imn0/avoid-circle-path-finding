import math
import numpy as np 
from circle import Circle

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

def is_line_free_to_go(a, b, circle: Circle):

    u = ( np.dot([circle.center[0]-a[0],circle.center[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) /  (  np.dot([b[0]-a[0], b[1]-a[1]], [b[0]-a[0], b[1]-a[1]])  ) 

    E = [a[0] + np.clip(u,0.0,1.0) * (b[0] - a[0]) , a[1] + np.clip(u,0.0,1.0) * (b[1] - a[1])]

    d = math.dist(E, circle.center)

    if d >= circle.radius: 
        return True
    else:
        return False
        


        
def get_circle_segment_path(circle :Circle, point1, point2):
    
    #first we get angle between point1 circle center and point2
    theta = abs(math.atan2(point2[1]-circle.center[1], point2[0]-circle.center[0]) - math.atan2(point1[1]-circle.center[1], point1[0]-circle.center[0]))

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

        theta2 = math.atan2(circle2.center[1] - circle1.center[1], circle2.center[0] - circle1.center[0]) - math.acos(abs(circle1.center - circle2.radius)/math.dist(circle1.center,circle2.center))
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
    p1 = (0.0, 5.0)
    p2 = (5.0, 0.0)

    c = Circle((0.0,0.0), 5.0)

    print(get_circle_segment_path(c,p1,p2))


def main1():
    
    start = (0.0, 0.0)
    end = (20.0, -10.0)
    circle_1 = Circle((5.0, -5.0), 5.0)
    circle_2 = Circle((15.0, -7.0), 3.0)
    circles = [circle_1, circle_2]

    final_points = []

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
            final_points.append([start, tangent_end_points[0]])
    
        if tg2:
            final_points.append([start, tangent_end_points[1]])




    print(final_points)




if __name__ == "__main__":
    test()

    
