from util import read_triangle_mesh, read_camera_properties, input_mesh_filename, project_mesh
import pygame
from model import View
from logger import logger
import os

def draw_mesh(screen, mesh):
    for triangle in mesh:
        pygame.draw.rect(screen,(255, 255, 255), (triangle.pointA.x, triangle.pointA.y, 2, 2))
        pygame.draw.rect(screen,(255, 255, 255), (triangle.pointB.x, triangle.pointB.y, 2, 2))
        pygame.draw.rect(screen,(255, 255, 255), (triangle.pointC.x, triangle.pointC.y, 2, 2))

DATA_DIR = "./data"

if __name__ == '__main__':
    camera = read_camera_properties()
    view = View(1366, 768)

    pygame.init()
    screen = pygame.display.set_mode((view.WIDTH, view.HEIGHT))
    pygame.display.set_caption("Wintermute 3D")

    running = True
    while running:
        screen.fill((0, 0, 0))
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                filename = input_mesh_filename()
                mesh = read_triangle_mesh(input_filename=os.path.join(DATA_DIR, filename))
                mesh = project_mesh(camera, view, mesh)
                draw_mesh(screen, mesh)
                pygame.display.update()

    pygame.quit()
