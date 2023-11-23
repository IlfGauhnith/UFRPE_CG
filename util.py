from algebraic import Coordinate
from model import Camera, Triangle
import configparser

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
        
        vertex = [Coordinate( float(line[0]), float(line[1]), float(line[2]) ) 
                  for line in 
                  [line.strip().split(" ") for line in lines[0:n_vertex]]]
        lines = lines[n_vertex:] # slicing out vertex data

        triangles = [Triangle( vertex[coordinate_index[0] - 1], vertex[coordinate_index[1] - 1], vertex[coordinate_index[2] - 1] )
                     for coordinate_index in 
                     [( int(line[0]), int(line[1]), int(line[2]) )
                     for line in
                     [line.strip().split(" ") for line in lines]]]

    return triangles

def read_camera_properties():
    cam_configs = configparser.ConfigParser()
    cam_configs.read("cam.properties")

    N = Coordinate(float(cam_configs["DEFAULT"]["Nx"]), 
                   float(cam_configs["DEFAULT"]["Ny"]), 
                   float(cam_configs["DEFAULT"]["Nz"]))

    V = Coordinate(float(cam_configs["DEFAULT"]["Vx"]),
                   float(cam_configs["DEFAULT"]["Vy"]),
                   float(cam_configs["DEFAULT"]["Vz"]))
    
    C = Coordinate(float(cam_configs["DEFAULT"]["Cx"]),
                   float(cam_configs["DEFAULT"]["Cy"]),
                   float(cam_configs["DEFAULT"]["Cz"]))
    
    d = float(cam_configs["DEFAULT"]["d"])
    hx = float(cam_configs["DEFAULT"]["hx"])
    hy = float(cam_configs["DEFAULT"]["hy"])

    return Camera(N, V, d, hx, hy, C)
    