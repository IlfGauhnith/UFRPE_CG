import algebraic as alg


class Triangle:
    
    def __init__(self, pointA:alg.Coordinate, pointB:alg.Coordinate, pointC:alg.Coordinate) -> None:
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC

    def __str__(self) -> str:
        return f"Triangle<A:{self.pointA}, B:{self.pointB}, C:{self.pointC}>"

class Light:
    
    def __init__(self, ambiental:tuple[int, int, int], ambiental_coef:float, light_color:tuple[int, int, int], location:alg.Coordinate, diffuse_coef:tuple[float, float, float], diffuse_color:tuple[float, float, float], specular_coef:float, theta:int):
        self.ambiental = ambiental              # Iamb
        self.ambiental_coef = ambiental_coef    # Ka
        self.light_color = light_color          # Il
        self.location = location                # Pl
        self.diffuse_coef = diffuse_coef        # Kd
        self.diffuse_color = diffuse_color      # Od
        self.specular_coef = specular_coef      # Ks
        self.theta = theta                      # η

    def __str__(self) -> str:
        return f"Camera<ambiental:{self.ambiental}, ambiental_coef:{self.ambiental_coef}, light_color:{self.light_color}, location:{self.location}, diffuse_coef:{self.diffuse_coef}, diffuse_color:{self.diffuse_color}, specular_coef:{self.specular_coef}, theta:{self.theta}>"

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

        # Calculating U, an perpendicular axle to NxV.
        self.U = self._calculate_U()

        # normalizing.
        self.V = alg.normalize(self.V)
        self.N = alg.normalize(self.N)
        self.U = alg.normalize(self.U)
        
    def _calculate_U(self):
        #unit = alg.Coordinate(1.0, 1.0, 1.0)
        #V_norm = alg.norm(self.V)
        #N_norm = alg.norm(self.N)

        #return unit * (V_norm*N_norm) # sin 90 omitted
        x_comp = self.V.y * self.N.z - self.V.z * self.N.y
        y_comp = self.V.z * self.N.x - self.V.x * self.N.z
        z_comp = self.V.x * self.N.y - self.V.y * self.N.x

        return alg.Coordinate(x_comp, y_comp, z_comp)
    
    def __str__(self) -> str:
        return f"Camera<C:{self.C}, N:{self.N}, V:{self.V}, U:{self.U}, d:{self.d}, hx:{self.hx}, hy:{self.hy}>"

class View:

    def __init__(self, WIDTH, HEIGHT) -> None:
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
