import os


def read_fonts():
    font_files = [file for file in os.listdir("fonts")]

    fonts = {}
    for font_file in font_files:
        filename = os.path.basename(font_file)
        fonts[filename.split(".")[0]] = _parse_font_file(f"fonts/{font_file}")

    return fonts


def _parse_font_file(filename):
    ascii_art_map = {}

    with open(filename, "r") as file:
        current_char = None
        current_art = []

        for line in file:
            line = line.strip("\r\n")

            if len(line) == 1:
                if current_char is not None:
                    ascii_art_map[current_char] = current_art

                current_char = line
                current_art = []
            else:
                chars = list(line)
                current_art.append(list(map(int, chars)))

        if current_char is not None:
            ascii_art_map[current_char] = current_art

    return ascii_art_map


def matrix_to_ascii(matrix):
    shades = " ░▒▓█"
    factor = len(shades) - 1
    return [[shades[int(factor * col)] for col in row] for row in matrix]
    # if you want to display matrix values - use this
    # return [["%.3f " % col for col in row] for row in matrix] 


def ascii_matrix_to_ascii_lines(ascii):
    return ["".join(map(str, row)) for row in ascii]