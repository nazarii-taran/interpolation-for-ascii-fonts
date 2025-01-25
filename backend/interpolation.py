def _init_zero_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def nearest_neighbour_interpolation(matrix, scale_factor):
    rows, cols = len(matrix), len(matrix[0])
    scaled_rows = int(rows * scale_factor)
    scaled_cols = int(cols * scale_factor)
    scaled_matrix = _init_zero_matrix(scaled_rows, scaled_cols)

    for i in range(scaled_rows):
        for j in range(scaled_cols):
            x = int(i / scale_factor)
            y = int(j / scale_factor)

            scaled_matrix[i][j] = matrix[x][y]

    return scaled_matrix


def bilinear_interpolation(matrix, scale_factor):
    rows, cols = len(matrix), len(matrix[0])
    scaled_rows = int(rows * scale_factor)
    scaled_cols = int(cols * scale_factor)
    scaled_matrix = _init_zero_matrix(scaled_rows, scaled_cols)

    for i in range(scaled_rows):
        for j in range(scaled_cols):
            x = (i + 0.5) / scale_factor - 0.5
            y = (j + 0.5) / scale_factor - 0.5

            x = max(0, min(x, rows - 1))
            y = max(0, min(y, cols - 1))

            i1, i2 = int(x), min(int(x) + 1, rows - 1)
            j1, j2 = int(y), min(int(y) + 1, cols - 1)

            wi = x - i1 if i2 != i1 else 0
            wj = y - j1 if j2 != j1 else 0

            scaled_matrix[i][j] = (
                matrix[i1][j1] * (1 - wi) * (1 - wj) +
                matrix[i1][j2] * (1 - wi) * wj +
                matrix[i2][j1] * wi * (1 - wj) +
                matrix[i2][j2] * wi * wj
            )

    return scaled_matrix


def bicubic_interpolation(matrix, scale_factor):
    rows, cols = len(matrix), len(matrix[0])
    scaled_rows = int(rows * scale_factor)
    scaled_cols = int(cols * scale_factor)
    scaled_matrix = _init_zero_matrix(scaled_rows, scaled_cols)

    for i in range(scaled_rows):
        for j in range(scaled_cols):
            x = (i + 0.5) / scale_factor - 0.5
            y = (j + 0.5) / scale_factor - 0.5

            i1 = int(x)
            j1 = int(y)

            q1, q2, q3, q4 = _get_cubic_functions(x - i1)

            interpolation_by_rows = []
            for n in range(-1, 3):
                p1 = _get_cell_value(matrix, i1 - 1, j1 + n)
                p2 = _get_cell_value(matrix, i1, j1 + n)
                p3 = _get_cell_value(matrix, i1 + 1, j1 + n)
                p4 = _get_cell_value(matrix, i1 + 2, j1 + n)

                interpolated_value = p1 * q1 + p2 * q2 + p3 * q3 + p4 * q4
                interpolation_by_rows.append(interpolated_value)

            q1, q2, q3, q4 = _get_cubic_functions(y - j1)
            p1, p2, p3, p4 = interpolation_by_rows

            interpolated_value = p1 * q1 + p2 * q2 + p3 * q3 + p4 * q4
            scaled_matrix[i][j] = max(0, min(1, interpolated_value))

    return scaled_matrix


def _get_cell_value(matrix, x, y):
    # version with sharp edges
    # rows, cols = len(matrix), len(matrix[0])
    # x = max(0, min(int(x), rows - 1))
    # y = max(0, min(int(y), cols - 1))
    # return matrix[x][y]

    # version with smooth edges
    rows, cols = len(matrix), len(matrix[0])
    if 0 <= x < rows and 0 <= y < cols:
        return matrix[int(x)][int(y)]
    return 0


def _get_cubic_functions(t):
    return [
        (-t**3 + 2 * t**2 - t) / 2,
        (3 * t**3 - 5 * t**2 + 2) / 2,
        (-3 * t**3 + 4 * t**2 + t) / 2,
        (t**3 - t**2) / 2
    ]