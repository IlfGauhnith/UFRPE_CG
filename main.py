from util import read_triangle_mesh, read_camera_properties
import pygame

MESH_FILENAME = "/home/lucas.burle/BCC/CG/data/calice2.byu"

if __name__ == '__main__':
    mesh = read_triangle_mesh(input_filename=MESH_FILENAME)
    camera = read_camera_properties()

    print(camera)
