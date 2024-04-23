# Задача о подсветке узлов сетки

![Python](https://img.shields.io/badge/Python-3.8-orange)
![Flask](https://img.shields.io/badge/Flask-orange)
![PyCairo](https://img.shields.io/badge/PyCairo-orange)
![HTML](https://img.shields.io/badge/HTML-orange)
![MySQL](https://img.shields.io/badge/MySQL-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-orange)

Этот проект представляет собой веб-приложение для рисования конечно-элементной сетки на основе данных из базы данных femdb. При указании мышью на узел сетка перерисовывается с выделением цветом этого узла.

## Установка и запуск

1. Запустите приложение, запустив файл `app.py`.

## Структура проекта

- **app.py**: Основной файл приложения Flask, который содержит обработчики маршрутов и запускает приложение.
- **dbcm.py**: Модуль для управления подключением к базе данных.
- **draw.py**: Модуль для отрисовки графики.
- **triangles.py**: Модуль для работы с треугольниками.
- **index.html**: HTML-шаблон для отображения интерфейса пользователя.

## Файловая структура

- **data_files**: Папка с файлами конфигурации базы данных и другими данными.
- **static**: Папка для статических файлов, таких как CSS, JavaScript и изображения.
- **templates**: Папка для HTML-шаблонов.

## Описание модулей

### app.py

Основной файл приложения Flask, который содержит обработчики маршрутов для отображения интерфейса и обработки запросов.

### dbcm.py

Модуль для управления подключением к базе данных с использованием контекстного менеджера.

### draw.py

Модуль для отрисовки графики, включая треугольники и узлы.

### triangles.py

Модуль для работы с треугольниками, включая установку цветов на основе соединений.

### index.html

HTML-шаблон для отображения интерфейса пользователя, включая SVG-контейнер и форму выбора цвета.

## JavaScript

JavaScript используется для управления интерактивностью пользовательского интерфейса, включая изменение цвета узлов и перерисовку сетки при выделении узла.

Для решения задачи будем воспринимать каждый треугольник как узел графа, где связь между узлами будет означать,
что два треугольника имеют общую грань.
Для хранения графа будем использовать классы(модуль <kbd>triangles.py</kbd>):

``` python
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
```

# Алгоритм работы

1. **Загрузка данных из базы данных**: При запуске приложения данные о узлах и треугольниках загружаются из базы данных femdb.

2. **Отрисовка сетки**: При загрузке главной страницы вызывается функция `draw_graph()`, которая рассчитывает масштаб и сдвиг для отображения сетки и создает SVG-файл с треугольниками и узлами.

3. **Обработка выделения узла**: При клике на узел на странице отправляется запрос на сервер с информацией о выбранном узле. Сервер сбрасывает выделение всех треугольников и выделяет треугольники, содержащие указанный узел.

4. **Установка цветов**: Для каждого треугольника определяется цвет на основе соединений с другими треугольниками. Используются доступные цвета, чтобы минимизировать количество конфликтов цветов.

5. **Изменение цвета узлов (JavaScript)**: Пользователь может выбрать цвет для узлов из предоставленных в форме. При наведении мыши на узел, он окрашивается выбранным цветом.

6. **Перерисовка сетки**: После обработки запроса о выделении узла или изменении цвета узлов, сетка перерисовывается с учетом всех изменений.

7. **Обновление интерфейса**: Интерфейс пользователя автоматически обновляется с учетом всех изменений, чтобы отобразить актуальное состояние сетки и узлов.


Для создания тестовой БД femdb можно использовать следующую последовательность SQL-запросов:

``` MySQL
DROP TABLE IF EXISTS elements;
CREATE TABLE elements (
  id smallint(6) NOT NULL default '0',
  n1 smallint(6) NOT NULL default '0',
  n2 smallint(6) NOT NULL default '0',
  n3 smallint(6) NOT NULL default '0',
  props char(12) NOT NULL default 'steel',
  PRIMARY KEY  (id)
);

LOCK TABLES elements WRITE;
INSERT INTO elements VALUES (1,2,3,5,'steel'),(2,1,2,4,'steel'),(3,2,5,4,'steel'),
	(4,5,6,4,'steel'),(5,5,7,6,'steel'),(6,5,8,7,'steel'),(7,8,9,7,'steel'),(8,8,10,9,'steel'),
	(9,10,11,9,'steel'),(10,10,12,11,'steel'),(11,12,13,11,'steel'),(12,12,14,13,'steel'),
	(13,12,15,14,'steel'),(14,14,18,13,'steel'),(15,15,16,14,'steel'),(16,16,17,14,'steel'),
	(17,14,17,18,'steel'),(18,16,20,17,'steel'),(19,17,19,18,'steel'),(20,20,19,17,'steel'),
	(21,20,21,19,'steel'),(22,19,21,23,'steel'),(23,20,22,21,'steel'),(24,22,24,21,'steel'),
	(25,21,24,23,'steel'),(26,28,27,22,'steel'),(27,27,29,26,'steel'),(28,27,26,22,'steel'),
	(29,24,26,25,'steel'),(30,24,25,23,'steel');
UNLOCK TABLES;

DROP TABLE IF EXISTS loadings;
CREATE TABLE loadings (
  type char(1) NOT NULL default '',
  direction char(1) default NULL,
  node smallint(6) NOT NULL default '0',
  value float default NULL,
  KEY key_node (node)
);

LOCK TABLES loadings WRITE;
INSERT INTO loadings VALUES ('r','x',1,NULL),('r','x',2,NULL),('r','x',3,NULL),
	('h',NULL,14,NULL),('f','x',27,-10),('f','y',27,-50);
UNLOCK TABLES;

DROP TABLE IF EXISTS materials;
CREATE TABLE materials (
  name char(12) NOT NULL default '',
  density float NOT NULL default '0',
  elastics float NOT NULL default '0',
  poisson float NOT NULL default '0',
  strength float NOT NULL default '0',
  PRIMARY KEY  (name)
);

LOCK TABLES materials WRITE;
INSERT INTO materials VALUES ('steel',7.8,200,0.25,1000),
	('aluminium',2.7,65,0.34,600),('concrete',5.6,25,0.12,300),
	('duraluminium',2.8,70,0.31,700),('titanium',4.5,116,0.32,950),
	('brass',8.5,93,0.37,300);
UNLOCK TABLES;

DROP TABLE IF EXISTS nodes;
CREATE TABLE nodes (
  id smallint(6) NOT NULL default '0',
  x float NOT NULL default '0',
  y float NOT NULL default '0',
  PRIMARY KEY  (id)
);

LOCK TABLES nodes WRITE;
INSERT INTO nodes VALUES (1,-95,20),(2,-87.5,20),(3,-80,20),(4,-95,10),
	(5,-80,15),(6,-85,-1),(7,-75,-3),(8,-65,15),(9,-55,-6),(10,-40,15),(11,-35,-10),
	(12,-15,15),(13,-15,-14),(14,0,0),(15,5,20),(16,20,8),(17,20,-10),(18,10,-20),
	(19,30,-27),(20,40,-3),(21,50,-25),(22,60,-15),(23,60,-39),(24,65,-25),(25,75,-35),
	(26,80,-20),(27,75,-7),(28,65,-5),(29,83,-9);
UNLOCK TABLES;
```