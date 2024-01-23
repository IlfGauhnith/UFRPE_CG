import algebraic as alg
from model import Camera, Triangle, Light
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

def read_light_properties(config_name):
    light_configs = configparser.ConfigParser()
    light_configs.read("light.properties")

    ambiental = (int(light_configs[config_name]["Iambr"]),
                int(light_configs[config_name]["Iambg"]),
                int(light_configs[config_name]["Iambb"]))
    
    ambiental_coef = float(light_configs[config_name]["Ka"])

    light_color = (int(light_configs[config_name]["Ilr"]),
                int(light_configs[config_name]["Ilg"]),
                int(light_configs[config_name]["Ilb"]))

    location = alg.Coordinate(float(light_configs[config_name]["Plx"]),
                float(light_configs[config_name]["Ply"]),
                float(light_configs[config_name]["Plz"]))
    
    diffuse_coef = (float(light_configs[config_name]["Kdr"]),
                float(light_configs[config_name]["Kdg"]),
                float(light_configs[config_name]["Kdb"]))

    diffuse_color = (float(light_configs[config_name]["Odr"]),
                float(light_configs[config_name]["Odg"]),
                float(light_configs[config_name]["Odb"]))

    specular_coef = float(light_configs[config_name]["Ks"])

    theta = int(light_configs[config_name]["Theta"])

    return Light(ambiental, ambiental_coef, light_color, location, diffuse_coef, diffuse_color, specular_coef, theta)

def input_mesh_filename():
    while True:
        user = input("Mesh filename with extension: ")

        if user not in os.listdir("./data"):
            print(f"{user} not found inside /data.")
        else:
            return user

def camera_project_mesh(camera, mesh):
    for idx, triangle in enumerate(mesh):
        pointA = alg.camera_perspective_projection(camera, triangle.pointA)
        pointB = alg.camera_perspective_projection(camera, triangle.pointB)
        pointC = alg.camera_perspective_projection(camera, triangle.pointC)
        
        pp_triangle = Triangle(pointA, pointB, pointC) 
        logger.debug(f"{triangle} => {pp_triangle}")
        mesh[idx] = pp_triangle
    
    return mesh

def screen_project_mesh(view, cam, mesh):
    for idx, triangle in enumerate(mesh):
        pointA = alg.screen_projection(view, cam, triangle.pointA)
        pointB = alg.screen_projection(view, cam, triangle.pointB)
        pointC = alg.screen_projection(view, cam, triangle.pointC)
        
        pp_triangle = Triangle(pointA, pointB, pointC, triangle.normal) 
        logger.debug(f"{triangle} => {pp_triangle}")
        mesh[idx] = pp_triangle
    
    return mesh

def compute_normal(mesh, tonalization_model:str):
    if tonalization_model == "--flat":
        for idx, triangle in enumerate(mesh):
            triangle.normal = alg.calculate_surface_normal(triangle)
            logger.debug(f"normal computed: {triangle}")