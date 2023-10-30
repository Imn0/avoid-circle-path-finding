

import math

class Circle:
    def __init__(self, center, radius: float) -> None:
        self.center = center
        self.radius = radius

def do_circles_intersect(circle1, circle2):
    # Calculate the distance between the centers of the two circles
    distance = math.sqrt((circle1.center[0] - circle2.center[0]) ** 2 + (circle1.center[1] - circle2.center[1]) ** 2)
    
    # Check if the distance is less than the sum of the radii
    return distance < (circle1.radius + circle2.radius)

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

# Example usage
circle1 = Circle((0, 0), 2)
circle2 = Circle((3, 0), 2)
circle3 = Circle((1, 1), 1.5)

circles = [circle1, circle2, circle3]

intersections = find_intersections(circles)
for intersection in intersections:
    print(f"Intersection : ({intersection})")
