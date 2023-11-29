import algebraic as alg
from model import Camera, Triangle
import configparser
import os
from logger import logger

def read_triangle_mesh(input_filename:str):
    """
    Returns:
        list of tuples (a, b, c) representing a triangle. 
        Each of these tuples elements a, b and c is a tuple (x, y, z).
        x, y and z assumes integer values representing a 3d coordinate each.
        
        i.e. that list contains 3 triangles:
            [((1, 1, 1), (1, 30, 1), (30, 30, 1)),
            ((1, 1, 1), (1, 30, 1), (1, 1, 30)),
            ((1, 30, 1), (30, 30, 1), (1, 1, 30))]
    """
   
    with open(input_filename, "r") as f:
        lines = f.readlines()
        
        # first line is formatted as <vertex_amount> <triangles_amount>
        n_vertex, n_triangles = lines[0].strip().split(" ")
        n_vertex, n_triangles = int(n_vertex), int(n_triangles)

        lines = lines[1:] # slicing out first line.
        
        vertex = [alg.Coordinate( float(line[0]), float(line[1]), float(line[2]) ) 
                  for line in 
                  [line.strip().split(" ") for line in lines[0:n_vertex]]]
        lines = lines[n_vertex:] # slicing out vertex data

        triangles = [Triangle( vertex[coordinate_index[0] - 1], vertex[coordinate_index[1] - 1], vertex[coordinate_index[2] - 1] )
                     for coordinate_index in 
                     [( int(line[0]), int(line[1]), int(line[2]) )
                     for line in
                     [line.strip().split(" ") for line in lines]]]

    return triangles

def read_camera_properties(config_name):
    cam_configs = configparser.ConfigParser()
    cam_configs.read("cam.properties")

    N = alg.Coordinate(float(cam_configs[config_name]["Nx"]), 
                   float(cam_configs[config_name]["Ny"]), 
                   float(cam_configs[config_name]["Nz"]))

    V = alg.Coordinate(float(cam_configs[config_name]["Vx"]),
                   float(cam_configs[config_name]["Vy"]),
                   float(cam_configs[config_name]["Vz"]))
    
    C = alg.Coordinate(float(cam_configs[config_name]["Cx"]),
                   float(cam_configs[config_name]["Cy"]),
                   float(cam_configs[config_name]["Cz"]))
    
    d = float(cam_configs[config_name]["d"])
    hx = float(cam_configs[config_name]["hx"])
    hy = float(cam_configs[config_name]["hy"])

    return Camera(N, V, d, hx, hy, C)
    
def input_mesh_filename():
    while True:
        user = input("Mesh filename with extension: ")

        if user not in os.listdir("./data"):
            print(f"{user} not found inside /data.")
        else:
            return user

def project_mesh(camera, view, mesh):
    for idx, triangle in enumerate(mesh):
        pointA = alg.camera_perspective_projection(camera, view, triangle.pointA)
        pointB = alg.camera_perspective_projection(camera, view, triangle.pointB)
        pointC = alg.camera_perspective_projection(camera, view, triangle.pointC)
        
        pp_triangle = Triangle(pointA, pointB, pointC) 
        logger.debug(f"{triangle} => {pp_triangle}")
        mesh[idx] = pp_triangle
    
    return mesh

def scan_line_conversion_triangle(triangle: Triangle) -> list[alg.Coordinate]:
    # Sort vertices using y coordinate as key. 
    vertices = sorted([triangle.pointA, triangle.pointB, triangle.pointC], key=lambda p: p.y)

    draw_coordinates = []

    # Drawing lines
    # Vertex A - B
    draw_coordinates.extend(bresenham(vertices[0], vertices[1]))
    # Vertex B - C
    draw_coordinates.extend(bresenham(vertices[1], vertices[2]))
    # Vertex C - A
    draw_coordinates.extend(bresenham(vertices[0], vertices[2]))
    
    return draw_coordinates

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

def bresenham(pointA, pointB) -> list[alg.Coordinate]:
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
