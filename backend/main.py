from flask import Flask, request, jsonify
from flask_cors import CORS

from helpers import read_fonts, matrix_to_ascii, ascii_matrix_to_ascii_lines
from interpolation import nearest_neighbour_interpolation, bilinear_interpolation, bicubic_interpolation


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

all_fonts = read_fonts()


@app.route("/api/fonts")
def get_available_fonts():
    return jsonify(list(sorted(all_fonts.keys())))


@app.route("/api/ascii-text")
def get_ascii_text():
    text = request.args.get("text")
    scale = float(request.args.get("scale"))
    font_type = request.args.get("fontType")
    algorithm = request.args.get("algorithm")

    target_font = all_fonts[font_type]

    original_ascii_matrices = [target_font[c] if c in target_font else target_font[" "] for c in text.upper()]

    interpolation_function = None
    match algorithm:
        case "nearest-neighbour":
            interpolation_function = nearest_neighbour_interpolation
        case "bilinear":
            interpolation_function = bilinear_interpolation
        case "bicubic":
            interpolation_function = bicubic_interpolation

    scaled_matrices = list(map(lambda m: interpolation_function(m, scale), original_ascii_matrices))

    scaled_ascii_chars = [matrix_to_ascii(m) for m in scaled_matrices]

    return jsonify([ascii_matrix_to_ascii_lines(c) for c in scaled_ascii_chars])


@app.route("/")
def greeting():
    greeting = request.args.get("greeting")
    return jsonify({ "string": f"Hello {greeting}!" })


if __name__ == "__main__":
    app.run(debug=True)
