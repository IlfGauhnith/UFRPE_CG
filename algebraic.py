import math
from logger import logger

class Coordinate:
    
    def __init__(self, x:float, y:float, z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Coordinate<x:{self.x}, y:{self.y}, z:{self.z}>" 

    def __eq__(self, other) -> bool:
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y and self.z == other.z
        
        raise TypeError(f"Cannot compare equality between Coordinate with {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Coordinate):
            x_comp = self.x - other.x
            y_comp = self.y - other.y
            z_comp = self.z - other.z

            return Coordinate(x_comp, y_comp, z_comp)
        
        raise TypeError(f"Cannot subtract a vector Coordinate with {type(other)}")

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
    logger.debug(f"universal {p_univ} => projected {p_proj}")

    x_comp = (cam.d / cam.hx) * (p_proj.x / p_proj.z)
    y_comp = (cam.d / cam.hy) * (p_proj.y / p_proj.z)

    p_norm = Coordinate(x_comp, y_comp)
    logger.debug(f"projected {p_proj} => normalized {p_norm}")

    return p_norm

def screen_projection(view, p_view):
    i_comp = math.floor(((p_view.x + 1)/2) * view.WIDTH + 0.5)
    j_comp = math.floor(view.HEIGHT - ((p_view.y + 1)/2) * view.HEIGHT + 0.5)

    p_screen = Coordinate(i_comp, j_comp)
    logger.debug(f"normalized {p_view} => view {p_screen}")

    return p_screen

def calculate_surface_normal(triangle):
    U = triangle.pointB - triangle.pointA
    V = triangle.pointC - triangle.pointA

    x_comp = U.y * V.z - U.z * V.y
    y_comp = U.z * V.x - U.x * V.z
    z_comp = U.x * V.y - U.y * V.x

    return normalize(Coordinate(x_comp, y_comp, z_comp))