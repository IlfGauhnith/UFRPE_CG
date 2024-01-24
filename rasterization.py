import algebraic as alg
from model import Triangle
import math

def bresenham(triangle: Triangle) -> list[alg.Coordinate]:
    # Sort vertices using y coordinate as key. 
    vertices = sorted([triangle.screen_pointA, triangle.screen_pointB, triangle.screen_pointC], key=lambda p: p.y)

    # Drawing lines
    # Vertex A - B
    AB = bresenham_line(vertices[0], vertices[1])
    # Vertex B - C
    BC = bresenham_line(vertices[1], vertices[2])
    # Vertex C - A
    AC = bresenham_line(vertices[0], vertices[2])
    
    return [AB, BC, AC]

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

def _scan_sides(side_1, side_2):
    points = []

    for coordinateA in side_1:
        for coordinateB in side_2:
            if coordinateA == coordinateB:
                continue

            x0, y0 = coordinateA.x, coordinateA.y
            x1, y1 = coordinateB.x, coordinateB.y

            if y1 > y0:
                break
            elif y1 < y0:
                continue

            if x0 > x1:
                x0, x1 = x1, x0

            for x in range(x0, x1 + 1):
                point = alg.Coordinate(x, y0)
                points.append(point)

    return points

def scan_line_conversion(triangle: Triangle) -> list[alg.Coordinate]:
    sides = bresenham(triangle)


    AB = sides[0]
    AB.sort(key=lambda x: x.y)

    BC = sides[1]
    BC.sort(key=lambda x: x.y)

    AC = sides[2]
    AC.sort(key=lambda x: x.y)

    points = []
    points.extend(_scan_sides(AB, AC))

    if BC[-1] == AC[0]:
        BC = BC[::-1]

    points.extend(_scan_sides(BC, AC))

    return points
