import math
from logger import logger

class Coordinate:
    
    def __init__(self, x:float, y:float, z=0.0, normal=None, color=(255, 255, 255)) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.triangles = []
        self.normal = normal
        self.color = color

    def __str__(self) -> str:
        return f"Coordinate<x:{self.x}, y:{self.y}, z:{self.z}, normal:{self.normal}>" 

    def __eq__(self, other) -> bool:
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y and self.z == other.z
        
        raise TypeError(f"Cannot compare equality between Coordinate and {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Coordinate):
            x_comp = self.x - other.x
            y_comp = self.y - other.y
            z_comp = self.z - other.z

            return Coordinate(x_comp, y_comp, z_comp)
        
        raise TypeError(f"Cannot subtract a vector Coordinate with {type(other)}")

    def __add__(self, other):
        if isinstance(other, Coordinate):
            x_comp = self.x + other.x
            y_comp = self.y + other.y
            z_comp = self.z + other.z

            return Coordinate(x_comp, y_comp, z_comp)
        
        raise TypeError(f"Cannot add a vector Coordinate with {type(other)}")
    
    def __mul__(self, other):
        
        if isinstance(other, Coordinate):
            return self.x * other.x + self.y * other.y + self.z * other.z

        elif isinstance(other, float) or isinstance(other, int):
            x_comp = self.x * other
            y_comp = self.y * other
            z_comp = self.z * other
            return Coordinate(x_comp, y_comp, z_comp)

        raise TypeError(f"Cannot multiply a vector Coordinate with {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            x_comp = self.x / other
            y_comp = self.y / other
            z_comp = self.z / other

            return Coordinate(x_comp, y_comp, z_comp)
        
        raise TypeError(f"Cannot divide a vector Coordinate with {type(other)}")

    __rtruediv__ = __truediv__
    __rmul__ = __mul__
    __rsub__ = __sub__

def orthogonalize(V:Coordinate, U:Coordinate) -> Coordinate:
    if not is_orthogonal(V, U):
        # Gram–Schmidt process
        projV_U = ((V*U)/(U*U)) * U
        V = V - projV_U

        assert is_orthogonal(V, U), f"Gram-Schmidt not working. V:{V} is not Orthogonal with U:{U}."

    return V

def norm(V):
    return math.sqrt(V*V)

def normalize(V):
    V_norm = norm(V)
    return V/V_norm

def is_orthogonal(V:Coordinate, U:Coordinate) -> bool:
    prod = abs(V * U)
    return 0 <= prod <= 1e-10

def camera_perspective_projection(cam, p_univ:Coordinate):
    p_c_distance = p_univ - cam.C
    
    x_comp = cam.U * p_c_distance
    y_comp = cam.V * p_c_distance
    z_comp = cam.N * p_c_distance

    p_proj = Coordinate(x_comp, y_comp, z_comp)

    return p_proj

def screen_projection(view, cam, p_proj):
    x_comp = (cam.d / cam.hx) * (p_proj.x / p_proj.z)
    y_comp = (cam.d / cam.hy) * (p_proj.y / p_proj.z)

    p_norm = Coordinate(x_comp, y_comp)

    i_comp = math.floor(((p_norm.x + 1)/2) * view.WIDTH + 0.5)
    j_comp = math.floor(view.HEIGHT - ((p_norm.y + 1)/2) * view.HEIGHT + 0.5)

    p_screen = Coordinate(i_comp, j_comp)

    return p_screen

def calculate_surface_normal(triangle):
    U = triangle.projection_pointB - triangle.projection_pointA
    V = triangle.projection_pointC - triangle.projection_pointA

    x_comp = U.y * V.z - U.z * V.y
    y_comp = U.z * V.x - U.x * V.z
    z_comp = U.x * V.y - U.y * V.x
    
    return normalize(Coordinate(x_comp, y_comp, z_comp))

def calculate_vertex_normal(vertex:Coordinate):
    norm_triangles = [triangle.normal for triangle in vertex.triangles]
    
    sumup = Coordinate(0, 0, 0)
    for norm in norm_triangles:
        sumup += norm
    
    return normalize(sumup)

def calculate_barycentric_coordinates(triangle):
    vertex_A = triangle.projection_pointA
    vertex_B = triangle.projection_pointB
    vertex_C = triangle.projection_pointC

    alfa = (vertex_A.x + vertex_B.x + vertex_C.x) / 3
    beta = (vertex_A.y + vertex_B.y + vertex_C.y) / 3
    gama = (vertex_A.z + vertex_B.z + vertex_C.z) / 3

    triangle.baricentric_coordinates = Coordinate(alfa, beta, gama)
