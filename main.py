# Импортируем необходимые модули
import math

import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QPointF
import sys


# Создаем класс для нашего окна
class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Устанавливаем размер и заголовок окна
        self.resize(800, 600)
        self.setWindowTitle("Карта")

        # Создаем кнопки для импорта карты, поиска кратчайшего пути, выбора транспортного средства и расчета времени пути
        self.import_button = QPushButton("Импорт карты", self)
        self.import_button.move(10, 10)
        self.import_button.clicked.connect(self.import_map)

        self.path_button = QPushButton("Поиск кратчайшего пути", self)
        self.path_button.move(10, 60)
        self.path_button.clicked.connect(self.find_path)

        self.vehicle_button = QPushButton("Выбор транспортного средства", self)
        self.vehicle_button.move(10, 110)
        self.vehicle_button.clicked.connect(self.choose_vehicle)

        self.time_button = QPushButton("Расчет времени пути", self)
        self.time_button.move(10, 160)
        self.time_button.clicked.connect(self.calculate_time)

        self.vehicle_button = QPushButton("Очистить карту", self)
        self.vehicle_button.move(10, 210)
        self.vehicle_button.clicked.connect(self.reset_map)

        # Создаем метку для вывода информации о пути
        self.info_label = QLabel(self)
        self.info_label.move(10, 260)
        self.info_label.resize(180, 180)
        self.info_label.setWordWrap(True)

        # Создаем графический виджет для отображения карты
        self.map_view = QGraphicsView(self)
        self.map_view.move(200, 10)
        self.map_view.resize(580, 580)

        # Создаем графическую сцену для размещения элементов на карте
        self.map_scene = QGraphicsScene()
        self.map_view.setScene(self.map_scene)

        # Создаем переменные для хранения изображения карты, точек пути и транспортного средства
        self.map_pixmap = None
        self.from_xy = None
        self.to_xy = None
        self.vehicle = None
        self.points_path = []

        self.min_dist_list = []  # Список минимальных точек
        self.min_dist = 0  # Минимальное расстояние

    # Определяем метод для импорта карты из файла
    def import_map(self):
        # Открываем диалоговое окно для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл карты", "", "Изображения (*.png *.jpg *.bmp)")
        # Если файл выбран, загружаем его в пиксмап и добавляем на сцену
        if file_name:
            self.map_pixmap = QPixmap(file_name)
            self.map_scene.clear()
            self.map_scene.addPixmap(self.map_pixmap)
            # Сбрасываем точки пути и информацию о пути
            self.from_xy = None
            self.to_xy = None
            self.info_label.clear()

    # Определяем метод find_path(self)
    def find_path(self):
        if self.map_pixmap and self.from_xy and self.to_xy:
            # Создаем пустой список для хранения возможных путей
            paths = []
            # Перебираем все точки из списка points
            for point in self.points_path:
                # Вычисляем расстояние от начальной точки до текущей точки
                dist_from = math.sqrt((point[0] - self.from_xy[0]) ** 2 + (point[1] - self.from_xy[1]) ** 2)
                # Вычисляем расстояние от текущей точки до конечной точки
                dist_to = math.sqrt((point[0] - self.to_xy[0]) ** 2 + (point[1] - self.to_xy[1]) ** 2)
                # Суммируем оба расстояния
                dist_total = dist_from + dist_to
                # Добавляем в список paths кортеж из расстояния и точки
                paths.append((dist_total, point))
            # Сортируем список paths по возрастанию расстояния
            paths.sort()
            # Берем первый элемент из списка paths, который содержит минимальное расстояние и точку
            self.min_dist, min_point = paths[0]
            # Создаем пустой список для хранения результата
            self.min_dist_list = []
            # Добавляем в результат начальную точку
            self.min_dist_list.append(self.from_xy)
            # Добавляем в результат точку с минимальным расстоянием
            self.min_dist_list.append(min_point)
            # Добавляем в результат конечную точку
            self.min_dist_list.append(self.to_xy)
            # Возвращаем результат и минимальное расстояние

            self.info_label.setText(
                f"Кратчайший путь:\nНачальная точка: ({self.from_xy[0]}, {self.from_xy[1]})\nКонечная точка: ({self.to_xy[0]}, {self.to_xy[0]})\nДлина пути: {self.min_dist} пикселей")
            return self.min_dist
        else:
            # Если карта не загружена или точки пути не выбраны, выводим сообщение об ошибке
            self.info_label.setText("Ошибка: Необходимо загрузить карту и выбрать точки пути")

    # Определяем метод для выбора транспортного средства
    def choose_vehicle(self):
        # Здесь должен быть диалоговый виджет для выбора транспортного средства из списка
        # Для простоты примера мы просто присваиваем переменной vehicle случайное значение из списка
        import random
        vehicles = ["Пешком", "Велосипед", "Автомобиль", "Общественный транспорт"]
        self.vehicle = random.choice(vehicles)
        # Выводим информацию о выбранном транспортном средстве на метку
        self.info_label.setText(f"Выбрано транспортное средство: {self.vehicle}")

    # Определяем метод для расчета времени пути
    def calculate_time(self):
        # Проверяем, что карта загружена, точки пути выбраны и транспортное средство выбрано
        if self.map_pixmap and self.from_xy and self.to_xy and self.vehicle:
            # Здесь должен быть алгоритм расчета времени пути в зависимости от длины пути и скорости транспортного средства
            # Для простоты примера мы просто присваиваем скорости транспортных средств фиксированные значения в пикселях в секунду
            speeds = {"Пешком": 10, "Велосипед": 20, "Автомобиль": 40, "Общественный транспорт": 30}
            speed = speeds[self.vehicle]
            # Рассчитываем время пути по формуле: время = длина / скорость
            time = self.distance(self.from_xy, self.to_xy) / speed
            # Выводим информацию о времени пути на метку
            self.info_label.setText(
                f"Время пути:\nТранспортное средство: {self.vehicle}\nСкорость: {speed} пикселей в секунду\nДлина пути: {self.distance(self.from_xy, self.to_xy):.2f} пикселей\nВремя пути: {time:.2f} секунд")
        else:
            # Если карта не загружена, точки пути не выбраны или транспортное средство не выбрано, выводим сообщение об ошибке
            self.info_label.setText("Ошибка: Необходимо загрузить карту, выбрать точки пути и транспортное средство")

    # Определяем метод для обработки кликов мыши на карте
    def mousePressEvent(self, event):
        # Проверяем, что карта загружена и клик был левой кнопкой мыши
        if self.map_pixmap and event.button() == Qt.MouseButton.LeftButton:
            # Получаем координаты клика относительно графического виджета
            x = event.position().x() - self.map_view.x()
            y = event.position().y() - self.map_view.y()

            # Проверяем, что координаты в пределах карты
            if 0 <= x < self.map_pixmap.width() and 0 <= y < self.map_pixmap.height():
                # Создаем точку с координатами клика
                point = QPointF(x, y)
                # Проверяем, что это первая точка пути
                if not self.from_xy:
                    # Сохраняем точку в переменную self.from_xy
                    self.from_xy = [point.x(), point.x()]
                    # Добавляем эллипс на сцену с красным цветом и радиусом 5 пикселей
                    self.map_scene.addEllipse(point.x() - 5, point.y() - 5, 10, 10, QPen(QColor("red")),
                                              QBrush(QColor("red")))
                # Проверяем, что это вторая точка пути
                elif not self.to_xy:
                    # Сохраняем точку в переменную self.to_xy
                    self.to_xy = [point.x(), point.x()]
                    # Добавляем эллипс на сцену с красным цветом и радиусом 5 пикселей
                    self.map_scene.addEllipse(point.x() - 5, point.y() - 5, 10, 10, QPen(QColor("red")),
                                              QBrush(QColor("green")))
                # Иначе игнорируем клик
                else:
                    self.points_path.append([point.x(), point.y()])
                    self.map_scene.addEllipse(self.points_path[-1][0] - 5, self.points_path[-1][1] - 5, 10, 10,
                                              QPen(QColor("red")),
                                              QBrush(QColor("purple")))
                    QBrush(QColor("purple"))
                    print(self.points_path)

                    # Определяем метод для сброса карты и переменных

    def reset_map(self):
        # Удаляем точки пути из графической сцены
        if self.from_xy:
            self.map_scene.removeItem(self.from_xy)
        if self.to_xy:
            self.map_scene.removeItem(self.to_xy)
        # Обнуляем переменные
        self.from_xy = None
        self.to_xy = None
        self.vehicle = None
        # Очищаем метку с информацией о пути
        self.info_label.setText("")

    # Определяем метод для расчета расстояния между двумя точками

    def distance(self, p1, p2):
        # Импортируем модуль math для использования квадратного корня
        import math
        # Рассчитываем разницу по x и y координатам
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        # Возвращаем расстояние по формуле
        return math.sqrt(dx ** 2 + dy ** 2)

    # Определяем метод для сброса карты и точек пути
    def reset_map(self):
        # Очищаем графическую сцену
        self.map_scene.clear()
        # Обнуляем координаты точек пути
        self.from_xy = None
        self.to_xy = None


app = QApplication(sys.argv)
window = MapWindow()
window.show()
sys.exit(app.exec())
