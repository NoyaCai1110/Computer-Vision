from tkinter import *
from math import log, sin, cos, pi
import random

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
IMAGE_ENLARGE = 8


class Heart:
    def __init__(self):
        self._points = set()    # the points exactly on the heart shape
        self._extra_points = set()  # the points near the heart shape
        self._inside_points = set() # the points inside the heart which far from the heart shape
        self.all_points = {}    # all the points of the heart at each given frame
        self.build(2000)

    # given angle t, return the canvas coordinates of the point on the heart shape in the direction of this angle
    @staticmethod
    def heart_function(t: float):
        x = 16 * (sin(t) ** 3) * IMAGE_ENLARGE + CANVAS_WIDTH / 2
        y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)) * IMAGE_ENLARGE + CANVAS_HEIGHT / 2
        return int(x), int(y)

    # rescale the heart at each frame and give some random jitter to the position of the points
    @staticmethod
    def calc_position(x: int, y: int, ratio: float):
        distance = ((x - CANVAS_WIDTH / 2) ** 2 + (y - CANVAS_HEIGHT / 2) ** 2) ** 0.5
        dx = int((x - CANVAS_WIDTH / 2) / distance * ratio) + random.randint(-1, 1)
        dy = int((y - CANVAS_HEIGHT / 2) / distance * ratio) + random.randint(-1, 1)
        return x - dx, y - dy

    # scatter a point on the heart shape into the inside of the heart
    @staticmethod
    def scatter_inside_points(x: int, y: int, ratio: float = 0.15):
        dx = int(- ratio * log(random.random()) * (x - CANVAS_WIDTH / 2))
        dy = int(- ratio * log(random.random()) * (y - CANVAS_HEIGHT / 2))
        return x - dx, y - dy

    # calculate the position of all points of the original heart shape
    def build(self, number: int):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = self.heart_function(t)
            self._points.add((x, y))
        for point_x, point_y in list(self._points):
            for _ in range(3):
                x, y = self.scatter_inside_points(point_x, point_y, 0.05)
                self._extra_points.add((x, y))
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = self.scatter_inside_points(x, y)
            self._inside_points.add((x, y))

    # calculate the position and the size of the points at each frame
    def calc(self, frame):
        ratio = 10 * sin(frame / 10 * pi)
        all_points = []
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._extra_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._inside_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[frame] = all_points

    # draw all the points in the given frame on the canvas
    def render(self, canvas: Canvas, frame: int):
        for x, y, size in self.all_points[frame % 20]:
            canvas.create_rectangle(x, y, x + size, y + size, width=0, fill="#ff7171")


# render the given frame on the canvas
def draw(window: Tk, canvas: Canvas, heart: Heart, frame: int = 0):
    canvas.delete('all')
    heart.render(canvas, frame)
    window.after(30, draw, window, canvas, heart, frame + 1)


if __name__ == '__main__':
    window = Tk()
    window.title('Shrinking Heart')
    canvas = Canvas(window, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    for frame in range(20):
        heart.calc(frame)
    draw(window, canvas, heart)
    window.mainloop()
