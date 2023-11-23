import math

class Coordinate:
    
    def __init__(self, x:float, y:float, z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Coordinate<x:{self.x}, y:{self.y}, z:{self.z}>" 

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

        assert is_orthogonal(V, U), "Gram-Schmidt not working. V is not Orthogonal with U."

    return V

def norm(V):
    return math.sqrt(V*V)

def normalize(V):
    V_norm = norm(V)
    return V/V_norm

def is_orthogonal(V:Coordinate, U:Coordinate) -> bool:
    return V * U == 0