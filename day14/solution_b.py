import numpy as np


def get_text() -> str:
    with open("input.txt") as f:
        return f.read()


def roll(array: np.array) -> np.array:
    empty_indicies = []

    for j, value in enumerate(array):
        if value == 0:
            empty_indicies.append(j)
        elif value == 1:
            empty_indicies = []
        elif value == 2:
            if empty_indicies:
                first_index = empty_indicies.pop(0)
                array[first_index], array[j] = value, 0
                empty_indicies.append(j)
        else:
            raise ValueError(f"Unknown value {value}")

    return array


def cycle(matrix: np.array) -> np.array:
    matrix = np.apply_along_axis(roll, 0, matrix)
    matrix = np.apply_along_axis(roll, 1, matrix)
    matrix = np.apply_along_axis(roll, 0, matrix[::-1, :])[::-1, :]
    matrix = np.apply_along_axis(roll, 1, matrix[:, ::-1])[:, ::-1]
    return matrix


def load(array: np.array) -> int:
    result = 0

    for i, value in enumerate(array[::-1]):
        if value == 2:
            result += (i + 1)

    return result


def main():
    text = get_text()

    rows = text.split("\n")
    n_rows = len(rows)
    n_cols = len(rows[0])

    mapping = {
        ".": 0,
        "#": 1,
        "O": 2,
    }

    matrix = np.zeros((n_rows, n_cols), dtype='i')
    for i in range(n_rows):
        for j in range(n_cols):
            matrix[i, j] = mapping[rows[i][j]]

    cache = {}

    total = 1000000000
    left = total
    while left > 0:
        key = matrix.data.tobytes()
        i = total - left

        if key in cache:
            last_i, last_matrix = cache[key]
            loop_delta = i - last_i
            left = left % loop_delta
            matrix = last_matrix
        else:
            matrix = cycle(matrix)
            cache[key] = (i, matrix.copy())

        print(i, np.apply_along_axis(load, 0, matrix).sum())

        left -= 1

    print(matrix)

    result = np.apply_along_axis(load, 0, matrix).sum()

    return result


if __name__ == "__main__":
    print(main())
