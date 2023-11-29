from util import read_triangle_mesh, read_camera_properties, input_mesh_filename, project_mesh
from rasterization import bresenham, scan_line_conversion
import pygame
from model import View
from logger import logger
import os

def draw_solid_mesh(screen, mesh):
    for triangle in mesh:
        draw_coordinates = scan_line_conversion(triangle)

        for coordinate in draw_coordinates:
            pygame.draw.line(screen, (255, 255, 255), (coordinate.x, coordinate.y), (coordinate.x, coordinate.y))

def draw_line_mesh(screen, mesh):
    for triangle in mesh:
        draw_coordinates = bresenham(triangle)
        draw_coordinates = [c for row in draw_coordinates for c in row]

        for coordinate in draw_coordinates:
            pygame.draw.line(screen, (255, 255, 255), (coordinate.x, coordinate.y), (coordinate.x, coordinate.y))

def draw_vertex_mesh(screen, mesh):
    for triangle in mesh:
        pygame.draw.line(screen, (255, 255, 255), (triangle.pointA.x, triangle.pointA.y), (triangle.pointA.x, triangle.pointA.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.pointB.x, triangle.pointB.y), (triangle.pointB.x, triangle.pointB.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.pointC.x, triangle.pointC.y), (triangle.pointC.x, triangle.pointC.y))
 
DATA_DIR = "./data"

if __name__ == '__main__':
    camera = read_camera_properties(config_name="VINICIUS-SUGGESTION")
    view = View(1044, 1044)

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
                draw_solid_mesh(screen, mesh)
                pygame.display.update()

            elif event.key == pygame.K_1:
                if mesh == None:
                    print("There's no mesh loaded. Please first press 'l' and enter a mesh filename.")
                else:
                    draw_vertex_mesh(screen, mesh)
                    pygame.display.update()

            elif event.key == pygame.K_2:
                if mesh == None:
                    print("There's no mesh loaded. Please first press 'l' and enter a mesh filename.")
                else:
                    draw_line_mesh(screen, mesh)
                    pygame.display.update()
            
            elif event.key == pygame.K_3:
                if mesh == None:
                    print("There's no mesh loaded. Please first press 'l' and enter a mesh filename.")
                else:
                    draw_solid_mesh(screen, mesh)
                    pygame.display.update()
                
    pygame.quit()
