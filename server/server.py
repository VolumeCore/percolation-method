import random
from flask import Flask

app = Flask(__name__)


@app.route("/generateMatrix/<int:size>/<int:concentration>", methods=['GET'])
def generate_matrix(concentration, size):
    return [[
        1 if (random.random() * 100 < concentration) else 0 for i in range(size)
    ] for j in range(size)]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)
