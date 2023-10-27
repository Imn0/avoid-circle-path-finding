
import math

def pc_calulate_tangent_points(point, circle):
    Cx, Cy = circle[0], circle[1]                
    r = circle[2]                              
    Px, Py =  point[0], point[1]                   
    dx, dy = Px-Cx, Py-Cy
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

    
        
def get_circle_segment_path(circle1, point1, point2):
    
    #first we get angle between point1 circle center and point2
    theta = abs(math.atan2(point2[1]-circle1[1], point2[0]-circle1[0]) - math.atan2(point1[1]-circle1[1], point1[0]-circle1[0]))

    #we have four segments 
    theta /= 4
    
    x, y = point1
    ox, oy = circle1[0], circle1[1]

    qx = ox + math.cos(theta) * (x - ox) + math.sin(theta) * (y - oy)
    qy = oy + -math.sin(theta) * (x - ox) + math.cos(theta) * (y - oy)

    

    d = circle1[2] / math.cos(theta)  
    
    f = d/circle1[2]
    qx = qx * f
    qy = qy * f
    qx1 = qx * f
    qy1 = qy * f

    x, y = qx, qy
    ox, oy = circle1[0], circle1[1]
    qx2 = ox + math.cos(2*theta) * (x - ox) + math.sin(2*theta) * (y - oy)
    qy2 = oy + -math.sin(2* theta) * (x - ox) + math.cos(2*theta) * (y - oy)
    print(f"K=({qx2}, {qy2})")
    print(f"F=({qx1}, {qy1})")


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
    point1 = (0.0,5.0)
    point2 = (5.0,0.0)
    circle1 = (0.0, 0.0, 5.0)
    circle2 = (3.0, 12.0, 5.0)
    get_circle_segment_path(circle1,point1, point2)\
    
if __name__ == "__main__":
    main()

    
