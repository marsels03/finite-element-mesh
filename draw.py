from triangles import triangles

# Увеличенные размеры изображения
width = 1100
height = 600


# Цвета
gray = '#bfbfbf'  # Серый цвет для всех элементов изначально
red = '#ff0000'  # Красный цвет для выделенных элементов

# Расчет коэффициентов масштабирования и сдвига
def calculate_scale_and_offset():
    # Получение минимальных и максимальных координат
    min_x = min(min(triangle.p1.x, triangle.p2.x, triangle.p3.x) for triangle in triangles)
    max_x = max(max(triangle.p1.x, triangle.p2.x, triangle.p3.x) for triangle in triangles)
    min_y = min(min(triangle.p1.y, triangle.p2.y, triangle.p3.y) for triangle in triangles)
    max_y = max(max(triangle.p1.y, triangle.p2.y, triangle.p3.y) for triangle in triangles)

    # Вычисление масштабов для каждой оси
    scale_x = width / (max_x - min_x)
    scale_y = height / (max_y - min_y)
    scale = min(scale_x, scale_y)  # Используем минимальный масштаб для сохранения пропорций

    # Уменьшение размеров изображения для центрирования и сохранения отступов
    scale *= 0.9  # Уменьшение масштаба на 10% для обеспечения отступов

    # Вычисление смещения для центрирования сетки
    offset_x = (width - (max_x - min_x) * scale) / 2
    offset_y = (height - (max_y - min_y) * scale) / 2

    return scale, offset_x, offset_y, min_x, min_y


def draw_graph():
    # Путь к файлу SVG
    svg_path = 'static/mesh.svg'

    # Расчет коэффициентов масштабирования и сдвига
    scale, offset_x, offset_y, min_x, min_y = calculate_scale_and_offset()

    # Начинаем создание SVG файла с его открытия и добавления начального тега SVG
    with open(svg_path, 'w') as svg_file:
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')

        # Отрисовка треугольников
        for triangle in triangles:
            # Масштабирование координат точек
            p1_x = (triangle.p1.x - min_x) * scale + offset_x
            p1_y = (triangle.p1.y - min_y) * scale + offset_y
            p2_x = (triangle.p2.x - min_x) * scale + offset_x
            p2_y = (triangle.p2.y - min_y) * scale + offset_y
            p3_x = (triangle.p3.x - min_x) * scale + offset_x
            p3_y = (triangle.p3.y - min_y) * scale + offset_y

            # Формирование тега <path> для треугольников
            path_d = f'M {p1_x},{height - p1_y} L {p2_x},{height - p2_y} L {p3_x},{height - p3_y} Z'
            svg_file.write(f'<path d="{path_d}" fill="{gray}"/>\n')

        # Отрисовка узлов
        for triangle in triangles:
            # Отрисовка узлов треугольника как кругов
            for point in [triangle.p1, triangle.p2, triangle.p3]:
                x = (point.x - min_x) * scale + offset_x
                y = (point.y - min_y) * scale + offset_y

                # Формирование тега <circle> для узлов с радиусом 8
                svg_file.write(f'<circle cx="{x}" cy="{height - y}" r="8" fill="{gray}" />\n')

        # Завершаем SVG файл закрывающим тегом </svg>
        svg_file.write('</svg>')

    # Возвращение пути к файлу SVG
    return svg_path
