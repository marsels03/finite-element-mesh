from dbcm import UseDatabase

triangles = []


class Point:
    def __init__(self, _id, x, y):
        self.id = _id
        self.x = x
        self.y = y


class Triangle:
    def __init__(self, _id, p1, p2, p3):
        self.id = _id
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.highlighted = False  # Изначально треугольник не выделен

        # Доступные цвета для треугольника
        self.allow_colors = [0, 1, 2, 3]
        self.connections = {}

        # Добавление связи с другими треугольниками
        self.establish_connections()

        # Установка цвета треугольника
        self.set_color()

    def establish_connections(self):
        # Установка связей с другими треугольниками
        for trian in triangles:
            if trian.id != self.id and self.check_connect(trian):
                self.connections[trian.id] = trian
                trian.connections[self.id] = self

    def check_connect(self, trian):
        # Проверка наличия двух общих точек между треугольниками
        common_points = 0
        for p in [self.p1, self.p2, self.p3]:
            for pt in [trian.p1, trian.p2, trian.p3]:
                if p.id == pt.id:
                    common_points += 1
        return common_points >= 2

    def set_color(self):
        # Установка цвета треугольника на основе соединений
        used_colors = set()
        for trian in self.connections.values():
            if trian.allow_colors:
                used_colors.add(trian.allow_colors)

        # Выбор первого доступного цвета, который не используется в соединениях
        for color in self.allow_colors:
            if color not in used_colors:
                self.allow_colors = color
                break

    def highlight(self, node_id):
        # Метод для выделения треугольника
        if node_id in [self.p1.id, self.p2.id, self.p3.id]:
            self.highlighted = True
        else:
            self.highlighted = False


def reset_colors():
    # Сброс выделения для всех треугольников
    for triangle in triangles:
        triangle.highlighted = False


def set_highlight(node_id):
    # Выделение треугольников, содержащих указанный узел
    for triangle in triangles:
        triangle.highlight(node_id)

def load_data(db_config):
    with UseDatabase(db_config) as cursor:
        # Загрузка данных об узлах
        cursor.execute('SELECT id, x, y FROM nodes')
        nodes = {row[0]: Point(row[0], row[1], row[2]) for row in cursor.fetchall()}

        # Загрузка данных о треугольниках
        cursor.execute('SELECT id, n1, n2, n3 FROM elements')
        for row in cursor.fetchall():
            # Получаем узлы по их идентификаторам
            p1 = nodes[row[1]]
            p2 = nodes[row[2]]
            p3 = nodes[row[3]]

            # Создаём объект Triangle и добавляем в список triangles
            triangles.append(Triangle(row[0], p1, p2, p3))
