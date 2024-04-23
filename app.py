from flask import Flask, render_template, request, jsonify
from draw import draw_graph
from triangles import triangles, reset_colors, set_highlight, load_data
from dbcm import UseDatabase
import json




app = Flask(__name__)

# Загрузка конфигурации базы данных из файла config.json
with open('data_files/config.json') as config_file:
    db_config = json.load(config_file)
load_data(db_config)

@app.route('/')
def index():
    # Перерисовка сетки при загрузке страницы
    draw_graph()
    return render_template('index.html')


@app.route('/highlight', methods=['POST'])
def highlight():
    # Получение данных из запроса
    data = request.get_json()
    node_id = data.get('node_id')

    # Сброс выделения всех треугольников
    reset_colors()
    # Выделение треугольников, содержащих указанный узел
    if node_id is not None:
        set_highlight(node_id)

    # Перерисовка сетки
    draw_graph()

    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True)
