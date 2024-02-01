import algebraic as alg

def phong_shading(triangle,  tonalization_model:str):
    if tonalization_model == "--flat":
        for pixel in triangle.pixels:
            flat(pixel, triangle)
    
    elif tonalization_model == "--gouraud":
        for pixel in triangle.pixels:
            gouraud(pixel, triangle)
        
    elif tonalization_model == "--phong":
        for pixel in triangle.pixels:
            phong(pixel, triangle)

def compute_normal(mesh, tonalization_model:str):
    if tonalization_model == "--flat":
        for triangle in mesh:
            triangle.normal = alg.calculate_surface_normal(triangle)
    
    elif tonalization_model == "--gouraud":
        for triangle in mesh:
            triangle.normal = alg.calculate_surface_normal(triangle)

        for triangle in mesh:    
            triangle.projection_pointA.normal = alg.calculate_vertex_normal(triangle.projection_pointA)
            triangle.projection_pointB.normal = alg.calculate_vertex_normal(triangle.projection_pointB)
            triangle.projection_pointC.normal = alg.calculate_vertex_normal(triangle.projection_pointC)

def flat(pixel, triangle):
    pass

def gouraud(pixel, triangle):
    pass

def phong(pixel, triangle):
    pass