import algebraic as alg


class Triangle:
    
    def __init__(self, pointA:alg.Coordinate, pointB:alg.Coordinate, pointC:alg.Coordinate) -> None:
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC

    def __str__(self) -> str:
        return f"Triangle<A:{self.pointA}, B:{self.pointB}, C:{self.pointC}>"

class Camera:

    def __init__(self, N:alg.Coordinate, V:alg.Coordinate, d:float, hx:float, hy:float, C:alg.Coordinate) -> None:
        self.N = N
        self.V = V
        self.d = d
        self.hx = hx
        self.hy = hy
        self.C = C

        # orthoganizing V with respect to N.
        self.V = alg.orthogonalize(self.V, self.N)

        # normalizing V and N.
        self.V = alg.normalize(self.V)
        self.N = alg.normalize(self.N)

        # Calculating U, an perpendicular axle to NxV.
        self.U = self._calculate_U()

    def _calculate_U(self):
        unit = alg.Coordinate(1.0, 1.0, 1.0)
        V_norm = alg.norm(self.V)
        N_norm = alg.norm(self.N)

        return unit * (V_norm*N_norm) # sin 90 omitted

    
    def __str__(self) -> str:
        return f"Camera<C:{self.C}, N:{self.N}, V:{self.V}, U:{self.U}, d:{self.d}, hx:{self.hx}, hy:{self.hy}>"
