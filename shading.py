import algebraic as alg
import model as model

def phong_shading(triangle,  tonalization_model:str, light:model.Light):
    if tonalization_model == "--flat":
        alg.find_barycenter(triangle)
        flat(triangle, light)
    
    elif tonalization_model == "--gouraud":
        gouraud(triangle, light)
        
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

def calculate_V_vector(point: alg.Coordinate):
    V = -1 * point
    aux = 1.0 / alg.norm(V)
    V = aux * V
    return V

def find_original_point(triangle, point:alg.Coordinate):
    barycentric_coordinates = alg.calculate_barycentric_coordinates_screen(triangle, point)
    
    alpha = barycentric_coordinates.alpha
    beta = barycentric_coordinates.beta
    gamma = barycentric_coordinates.gamma

    vertex_A = triangle.projection_pointA
    vertex_B = triangle.projection_pointB
    vertex_C = triangle.projection_pointC

    x_comp = alpha * vertex_A.x + beta * vertex_B.x + gamma * vertex_C.x
    y_comp = alpha * vertex_A.y + beta * vertex_B.y + gamma * vertex_C.y
    z_comp = alpha * vertex_A.z + beta * vertex_B.z + gamma * vertex_C.z

    return alg.Coordinate(x_comp, y_comp, z_comp)

def calculate_L_vector(light_location, point):
    return alg.normalize(light_location - point)

def calculate_R_vector(N, L):
    prod = 2 * (N * L)
    return (N * prod) - L

def flat(triangle, light:model.Light):
    Ia = tuple((rgb_component * light.ambiental_coef for rgb_component in light.ambiental))
    Id = None
    Is = None

    N = triangle.normal
    ogb = find_original_point(triangle, triangle.barycenter)
    V = calculate_V_vector(ogb)
    L = calculate_L_vector(light.location, ogb)
    R = calculate_R_vector(N, L)

    if N * L < 0:
        if N * V < 0:
            N = -1 * N
        else:
            Is = alg.Coordinate(0, 0, 0)
            Id = alg.Coordinate(0, 0, 0)
    if V * R < 0:
        Is = alg.Coordinate(0, 0, 0)

    if Id is None:   
        Id = ((N * L) * alg.Coordinate(*light.diffuse_coef))
        Id = Id.multiply(alg.Coordinate(*light.diffuse_color))
        Id = Id.multiply(alg.Coordinate(*light.light_color))

    if Is is None:
        Is = (alg.Coordinate(*light.light_color) * (((R * V) ** light.theta) * light.specular_coef))

    Id = (Id.x, Id.y, Id.z)
    Is = (Is.x, Is.y, Is.z)

    I_final = [round(Ia[0] + Id[0] + Is[0]), round(Ia[1] + Id[1] + Is[1]), round(Ia[2] + Id[2] + Is[2])]
    I_final = tuple([255 if v > 255 else v for v in I_final])

    for pixel in triangle.pixels:
        pixel.color = I_final

def gouraud(triangle, light:model.Light):
    Ia = tuple((rgb_component * light.ambiental_coef for rgb_component in light.ambiental))
    
    p_a = triangle.projection_pointA
    p_b = triangle.projection_pointB
    p_c = triangle.projection_pointC

    s_a = triangle.screen_pointA
    s_b = triangle.screen_pointB
    s_c = triangle.screen_pointC

    v_colors = []
    for p_vertex, s_vertex in zip([p_a, p_b, p_c], [s_a, s_b, s_c]):
        Id = None
        Is = None

        N = p_vertex.normal
        V = calculate_V_vector(p_vertex)
        L = calculate_L_vector(light.location, p_vertex)
        R = calculate_R_vector(N, L)

        if N * L < 0:
            if N * V < 0:
                N = -1 * N
            else:
                Is = alg.Coordinate(0, 0, 0)
                Id = alg.Coordinate(0, 0, 0)
        if V * R < 0:
            Is = alg.Coordinate(0, 0, 0)

        if Id is None:   
            Id = ((N * L) * alg.Coordinate(*light.diffuse_coef))
            Id = Id.multiply(alg.Coordinate(*light.diffuse_color))
            Id = Id.multiply(alg.Coordinate(*light.light_color))

        if Is is None:
            Is = (alg.Coordinate(*light.light_color) * (((R * V) ** light.theta) * light.specular_coef))

        Id = (Id.x, Id.y, Id.z)
        Is = (Is.x, Is.y, Is.z)

        I_final = [round(Ia[0] + Id[0] + Is[0]), round(Ia[1] + Id[1] + Is[1]), round(Ia[2] + Id[2] + Is[2])]
        I_final = tuple([255 if v > 255 else v for v in I_final])
        
        v_colors.append(I_final)

    for pixel in triangle.pixels:
        barycentric_coordinates = alg.calculate_barycentric_coordinates_screen(triangle, pixel)
        I1 = [barycentric_coordinates.alpha * v_colors[0][0], barycentric_coordinates.alpha * v_colors[0][1], barycentric_coordinates.alpha * v_colors[0][2]]
        I2 = [barycentric_coordinates.beta * v_colors[1][0], barycentric_coordinates.beta * v_colors[1][1], barycentric_coordinates.alpha * v_colors[1][2]]
        I3 = [barycentric_coordinates.alpha * v_colors[2][0], barycentric_coordinates.alpha * v_colors[2][1], barycentric_coordinates.alpha * v_colors[2][2]]

        I_final = [round(I1[0] + I2[0] + I3[0]), round(I1[1] + I2[1] + I3[1]), round(I1[2] + I2[2] + I3[2])]
        I_final = [255 if v > 255 else v for v in I_final]
        I_final = tuple([0 if v <= 0 else v for v in I_final])
        pixel.color = I_final

def phong(pixel, triangle):
    pass