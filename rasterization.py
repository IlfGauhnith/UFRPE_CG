import algebraic as alg
from model import Triangle
import math

def bresenham(triangle: Triangle) -> list[alg.Coordinate]:
    # Sort vertices using y coordinate as key. 
    vertices = sorted([triangle.pointA, triangle.pointB, triangle.pointC], key=lambda p: p.y)

    # Drawing lines
    # Vertex A - B
    AB = bresenham_line(vertices[0], vertices[1])
    # Vertex B - C
    BC = bresenham_line(vertices[1], vertices[2])
    # Vertex C - A
    AC = bresenham_line(vertices[0], vertices[2])
    
    return [*AB, *BC, *AC]

def _plot_line_low(x0, y0, x1, y1):
    draw_coordinates = []

    dx = x1 - x0
    dy = y1 - y0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy
    
    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1 + 1):
        draw_coordinates.append(alg.Coordinate(x, y))
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2*dy
    
    return draw_coordinates

def _plot_line_high(x0, y0, x1, y1):
    draw_coordinates = []

    dx = x1 - x0
    dy = y1 - y0
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx
    
    D = (2 * dx) - dy
    x = x0

    for y in range(y0, y1 + 1):
        draw_coordinates.append(alg.Coordinate(x, y))
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2*dx

    return draw_coordinates

def bresenham_line(pointA, pointB) -> list[alg.Coordinate]:
    x0, y0 = pointA.x, pointA.y
    x1, y1 = pointB.x, pointB.y

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            return _plot_line_low(x1, y1, x0, y0)
        else:
            return _plot_line_low(x0, y0, x1, y1)

    else:
        if y0 > y1:
            return _plot_line_high(x1, y1, x0, y0)
        else:
            return _plot_line_high(x0, y0, x1, y1)

def rasterize_flat_triangle(A, B, C):
    print(A, B, C)

    if B.y == A.y or C.y == A.y:
        return [alg.Coordinate(0, 0)]
    
    # y is descending or ascending
    ydir = math.copysign(1, B.y - A.y) # copysign returns 1 with (B.y - A.y)'s signal 
    ydir = int(ydir)

    # B is at a rightmost position than C.
    if B.x > C.x:
        B.x, C.x = C.x, B.x # Swaping. Note that y is the same.

    # Find the inverse slope (dx/dy) for the two non-horizontal edges
    invslope1 = ydir * (B.x - A.x) / (B.y - A.y)
    invslope2 = ydir * (C.x - A.x) / (C.y - A.y)

    curx1 = A.x + invslope1
    curx2 = A.x + invslope2
    points = []

    for y in range(A.y, B.y + ydir, ydir):
        for x in range(round(curx1), round(curx2) + 1):
            points.append(alg.Coordinate(x, y))
        curx1 += invslope1
        curx2 += invslope2
    
    return points

def scan_line_conversion(triangle: Triangle) -> list[alg.Coordinate]:
    points = []
    
    # Sort vertices using y coordinate as key. 
    A, B, C = sorted([triangle.pointA, triangle.pointB, triangle.pointC], key=lambda p: p.y)

    # Check for triangles with horizontal edge
    if B.y == C.y:
        # Bottom is horizontal
        print("bottom horizontal triangle")
        points.extend(rasterize_flat_triangle(A, B, C))
    elif A.y == B.y:
        # Top is horizontal
        print("top horizontal triangle")
        points.extend(rasterize_flat_triangle(C, A, B))
    else:
        # D is the (x, y) coordinates which intersects AC.
        D_x = round(A.x + (B.y - A.y) / (C.y - A.y) * (C.x - A.x))
        D_y = B.y
        D = alg.Coordinate(D_x, D_y)
        
        # Top triangle
        print("top triangle")
        points.extend(rasterize_flat_triangle(A, B, D))

        # Bottom triangle
        print("bottom triangle")
        points.extend(rasterize_flat_triangle(C, B, D))
    
    return points