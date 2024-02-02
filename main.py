from util import read_triangle_mesh, read_camera_properties, read_light_properties, camera_project_mesh, screen_project_mesh
from rasterization import bresenham, scan_line_conversion
from shading import phong_shading, compute_normal
import pygame
from model import View
from logger import logger
import os
import sys

def draw_phong_shaded_mesh(screen, mesh, tonalization_model, light):
    for triangle in mesh:
        scan_line_conversion(triangle)
        phong_shading(triangle, tonalization_model, light)

        for pixel in triangle.pixels:
            pygame.draw.line(screen, pixel.color, (pixel.x, pixel.y), (pixel.x, pixel.y))

def draw_solid_mesh(screen, mesh):
    for triangle in mesh:
        scan_line_conversion(triangle)

        for pixel in triangle.pixels:
            pygame.draw.line(screen, (255, 255, 255), (pixel.x, pixel.y), (pixel.x, pixel.y))

def draw_line_mesh(screen, mesh):
    for triangle in mesh:
        draw_coordinates = bresenham(triangle)
        draw_coordinates = [c for row in draw_coordinates for c in row]

        for coordinate in draw_coordinates:
            pygame.draw.line(screen, (255, 255, 255), (coordinate.x, coordinate.y), (coordinate.x, coordinate.y))

def draw_vertex_mesh(screen, mesh):
    for triangle in mesh:
        pygame.draw.line(screen, (255, 255, 255), (triangle.screen_pointA.x, triangle.screen_pointA.y), (triangle.screen_pointA.x, triangle.screen_pointA.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.screen_pointB.x, triangle.screen_pointB.y), (triangle.screen_pointB.x, triangle.screen_pointB.y))
        pygame.draw.line(screen, (255, 255, 255), (triangle.screen_pointC.x, triangle.screen_pointC.y), (triangle.screen_pointC.x, triangle.screen_pointC.y))
 
DATA_DIR = "./data"
TONAL_MODES = ["--flat", "--gouraud"]

if __name__ == '__main__':
    filename = sys.argv[1]
    tonal_mode = sys.argv[2]

    if filename not in os.listdir("./data"):
        print(f"{filename} not found inside /data.")
        exit()
    
    if tonal_mode not in TONAL_MODES:
        print(f"Incorrect tonalization model flag: {tonal_mode}.\n Please use one of these flags instead: {TONAL_MODES}")
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
    compute_normal(camera_projected_mesh, tonal_mode)
    screen_mesh = screen_project_mesh(view, camera, camera_projected_mesh)

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

            elif event.key == pygame.K_4:
                screen.fill((0, 0, 0))
                draw_phong_shaded_mesh(screen, screen_mesh, tonal_mode, light)                
                pygame.display.update()
                
    pygame.quit()
