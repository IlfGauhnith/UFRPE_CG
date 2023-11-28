from util import read_triangle_mesh, read_camera_properties, input_mesh_filename, project_mesh
import pygame
from model import View
from logger import logger
import os

def draw_mesh(screen, mesh):
    for triangle in mesh:
        #pygame.draw.rect(screen,(255, 255, 255), (triangle.pointA.x, triangle.pointA.y, 2, 2))
        #pygame.draw.rect(screen,(255, 255, 255), (triangle.pointB.x, triangle.pointB.y, 2, 2))
        #pygame.draw.rect(screen,(255, 255, 255), (triangle.pointC.x, triangle.pointC.y, 2, 2))

        pygame.draw.line(screen, (255, 255, 255), (triangle.pointA.x, triangle.pointA.y), (triangle.pointA.x, triangle.pointA.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.pointB.x, triangle.pointB.y), (triangle.pointB.x, triangle.pointB.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.pointC.x, triangle.pointC.y), (triangle.pointC.x, triangle.pointC.y))
        
DATA_DIR = "./data"

if __name__ == '__main__':
    camera = read_camera_properties(config_name="VINICIUS-SUGGESTION")
    view = View(1366, 768)

    pygame.init()
    screen = pygame.display.set_mode((view.WIDTH, view.HEIGHT))
    pygame.display.set_caption("Wintermute 3D")

    logger.debug(f"camera: {camera}")
    logger.debug(f"resolution: {view.WIDTH}x{view.HEIGHT}")
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
