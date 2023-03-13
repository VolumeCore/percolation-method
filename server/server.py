import os
import random
from flask import Flask, render_template

project_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
client_dir = os.path.join(project_dir, 'client')
static_dir = os.path.join(client_dir, 'static')
template_dir = os.path.join(client_dir, 'templates')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/generateMatrix/<int:size>/<int:concentration>", methods=['GET'])
def generate_matrix(concentration, size):
    return [[
        1 if (random.random() * 100 < concentration) else 0 for i in range(size)
    ] for j in range(size)]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)
