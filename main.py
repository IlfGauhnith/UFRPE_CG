from util import read_triangle_mesh, read_camera_properties
import pygame
import algebraic as alg
from model import View, Triangle

MESH_FILENAME = "/home/lucas.burle/BCC/CG/data/calice2.byu"

if __name__ == '__main__':
    mesh = read_triangle_mesh(input_filename=MESH_FILENAME)
    camera = read_camera_properties()
    view = View(300, 300)

    for idx, triangle in enumerate(mesh):
        pointA = alg.camera_perspective_projection(camera, view, triangle.pointA)
        pointB = alg.camera_perspective_projection(camera, view, triangle.pointB)
        pointC = alg.camera_perspective_projection(camera, view, triangle.pointC)
        mesh[idx] = Triangle(pointA, pointB, pointC)
    
        