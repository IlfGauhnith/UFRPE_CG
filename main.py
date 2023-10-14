

INPUT_FILENAME = "/home/lucas.burle/BCC/CG/triangle_mesh.txt"
VERBOSE = False

def read_triangle_mesh(input_filename:str):
    """
    Returns:
        list of tuples (a, b, c) representing a triangle. 
        Each of these tuples elements a, b and c is a tuple (x, y, z).
        x, y and z assumes integer values representing a 3d coordinate each.
        
        i.e. that list contains 3 triangles:
            [((1, 1, 1), (1, 30, 1), (30, 30, 1)),
            ((1, 1, 1), (1, 30, 1), (1, 1, 30)),
            ((1, 30, 1), (30, 30, 1), (1, 1, 30))]
    """
    if VERBOSE:
        print("read_triangle_mesh")
        print(f"input_filename: {input_filename}")

    with open(input_filename, "r") as f:
        lines = f.readlines()
        
        # first line is formatted as <vertex_amount> <triangles_amount>
        n_vertex, n_triangles = lines[0].strip().split(" ")
        n_vertex, n_triangles = int(n_vertex), int(n_triangles)

        if VERBOSE:
            print(f"n_vertex: {n_vertex}")
            print(f"n_triangles: {n_triangles}")

        lines = lines[1:] # slicing out first line.
        
        vertex = [( int(line[0]), int(line[1]), int(line[2]) ) 
                  for line in 
                  [line.strip().split(" ") for line in lines[0:n_vertex]]]
        lines = lines[n_vertex:] # slicing out vertex data

        triangles = [(vertex[coordinate_index[0] - 1], vertex[coordinate_index[1] - 1], vertex[coordinate_index[2] - 1])
                     for coordinate_index in 
                     [( int(line[0]), int(line[1]), int(line[2]) )
                     for line in
                     [line.strip().split(" ") for line in lines]]]

        if VERBOSE:
            print(f"vertex: {vertex}")
            print(f"triangle: {triangles}")
        
    return triangles

if __name__ == '__main__':
    mesh = read_triangle_mesh(input_filename=INPUT_FILENAME)
    for triangle in mesh:
        print(triangle)
