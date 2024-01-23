from util import read_triangle_mesh, read_camera_properties, read_light_properties, input_mesh_filename, camera_project_mesh, screen_project_mesh
from rasterization import bresenham, scan_line_conversion
import pygame
from model import View
from logger import logger
import os
import sys

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
    filename = sys.argv[1]

    if filename not in os.listdir("./data"):
        print(f"{filename} not found inside /data.")
        exit()
    
    camera = read_camera_properties(config_name="2VA")
    light = read_light_properties("2VA")
    view = View(600, 600)

    pygame.init()
    screen = pygame.display.set_mode((view.WIDTH, view.HEIGHT))
    pygame.display.set_caption(f"Wintermute 3D {view.WIDTH}x{view.HEIGHT}")
    
    screen.fill((0, 0, 0))

    mesh = read_triangle_mesh(input_filename=os.path.join(DATA_DIR, filename))
    camera_projected_mesh = camera_project_mesh(camera, mesh)
    screen_mesh = screen_project_mesh(view, mesh)

    draw_solid_mesh(screen, screen_mesh)
    pygame.display.update()

    logger.debug(f"camera: {camera}")
    logger.debug(f"light: {light}")
    logger.debug(f"resolution: {view.WIDTH}x{view.HEIGHT}")
    running = True
    while running:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:       
                screen.fill((0, 0, 0))     
                draw_vertex_mesh(screen, screen_mesh)
                pygame.display.update()

            elif event.key == pygame.K_2:
                screen.fill((0, 0, 0))
                draw_line_mesh(screen, screen_mesh)
                pygame.display.update()

            elif event.key == pygame.K_3:
                screen.fill((0, 0, 0))
                draw_solid_mesh(screen, screen_mesh)
                pygame.display.update()
                
    pygame.quit()
